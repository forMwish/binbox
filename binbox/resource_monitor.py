import psutil
import time
import os
import statistics
import subprocess
import threading

# 条件导入torch
try:
    import torch
    HAS_TORCH = True
except ImportError:
    HAS_TORCH = False

class ResourceMonitor:
    """
    资源监控类，用于跟踪程序运行时的 CPU、内存和 GPU 资源使用情况。
    可以实时监控并统计资源使用的平均值和峰值。
    """
    def __init__(self):
        """初始化资源监控器，获取当前进程并准备监控数据结构"""
        self.process = psutil.Process(os.getpid())
        self.monitoring = False
        self.status = {
            "cpu_percentages": [],  # 存储 CPU 使用率历史数据
            "memory_usages": [],    # 存储内存使用量历史数据 (MB)
            "gpu_utilizations": [],  # 存储 GPU 利用率历史数据
            "gpu_memory_usages": []  # 存储 GPU 显存使用量历史数据 (MB)
        }
        
    def start(self, interval=1.0, gpu_id=0, interval_print=1.0):
        """开始监控资源使用情况
        
        参数:
            interval: 监控间隔时间（秒）
            gpu_id: 要监控的 GPU ID
            interval_print: 打印状态的间隔时间（秒）
        """
        self.monitoring = True
        self.status = {
            "cpu_percentages": [],
            "memory_usages": [],
            "gpu_utilizations": [],
            "gpu_memory_usages": []
        }
        self.gpu_id = gpu_id
        self.printing = True
        
        # 启动监控线程
        self.monitor_thread = threading.Thread(target=self._monitor_resources, args=(interval,))
        self.monitor_thread.daemon = True
        self.monitor_thread.start()
        
        # 启动打印线程
        self.print_thread = threading.Thread(target=self._print_status_loop, args=(interval_print,))
        self.print_thread.daemon = True
        self.print_thread.start()
        
    def stop(self):
        """停止监控并返回资源使用统计信息"""
        self.monitoring = False
        self.printing = False
        
        # 等待线程结束
        if hasattr(self, 'monitor_thread') and self.monitor_thread.is_alive():
            self.monitor_thread.join(timeout=1.0)
        if hasattr(self, 'print_thread') and self.print_thread.is_alive():
            self.print_thread.join(timeout=1.0)
            
        # 计算统计数据
        stats = {}
        
        if self.status["cpu_percentages"]:
            stats["cpu"] = {
                "mean": statistics.mean(self.status["cpu_percentages"]),
                "max": max(self.status["cpu_percentages"]),
                "min": min(self.status["cpu_percentages"])
            }
            
        if self.status["memory_usages"]:
            stats["memory"] = {
                "mean": statistics.mean(self.status["memory_usages"]),
                "max": max(self.status["memory_usages"]),
                "min": min(self.status["memory_usages"])
            }
            
        if self.status["gpu_utilizations"] and HAS_TORCH:
            stats["gpu"] = {
                "utilization": {
                    "mean": statistics.mean(self.status["gpu_utilizations"]),
                    "max": max(self.status["gpu_utilizations"]),
                    "min": min(self.status["gpu_utilizations"])
                },
                "memory": {
                    "mean": statistics.mean(self.status["gpu_memory_usages"]),
                    "max": max(self.status["gpu_memory_usages"]),
                    "min": min(self.status["gpu_memory_usages"])
                }
            }
            
        return stats
    
    def _monitor_resources(self, interval):
        """监控资源使用情况的内部方法"""
        while self.monitoring:
            # 获取 CPU 使用率
            cpu_percent = self.process.cpu_percent()
            self.status["cpu_percentages"].append(cpu_percent)
            
            # 获取内存使用量 (MB)
            memory_info = self.process.memory_info()
            memory_mb = memory_info.rss / (1024 * 1024)
            self.status["memory_usages"].append(memory_mb)
            
            # 获取 GPU 使用情况 (如果可用)
            if HAS_TORCH and torch.cuda.is_available():
                try:
                    # 获取 GPU 利用率
                    gpu_util_output = subprocess.check_output(
                        ['nvidia-smi', '--query-gpu=utilization.gpu', '--format=csv,noheader,nounits', '-i', str(self.gpu_id)]
                    ).decode('utf-8').strip()
                    gpu_utilization = float(gpu_util_output)
                    self.status["gpu_utilizations"].append(gpu_utilization)
                    
                    # 获取 GPU 显存使用量 (MB)
                    gpu_mem_output = subprocess.check_output(
                        ['nvidia-smi', '--query-gpu=memory.used', '--format=csv,noheader,nounits', '-i', str(self.gpu_id)]
                    ).decode('utf-8').strip()
                    gpu_memory = float(gpu_mem_output)
                    self.status["gpu_memory_usages"].append(gpu_memory)
                except (subprocess.SubprocessError, ValueError):
                    # 如果无法获取 GPU 信息，添加 0 值
                    self.status["gpu_utilizations"].append(0)
                    self.status["gpu_memory_usages"].append(0)
            
            time.sleep(interval)
    
    def _print_status_loop(self, interval_print):
        """定期打印状态信息的内部方法"""
        while self.printing:
            self._display_current_status()
            time.sleep(interval_print)
    
    def _display_current_status(self):
        """显示当前资源使用状态"""
        print("\n--- 资源监控状态 ---")
        
        if self.status["cpu_percentages"]:
            print(f"CPU 使用率: {self.status['cpu_percentages'][-1]:.2f}%")
            
        if self.status["memory_usages"]:
            print(f"内存使用: {self.status['memory_usages'][-1]:.2f} MB")
            
        if self.status["gpu_utilizations"] and HAS_TORCH and torch.cuda.is_available():
            print(f"GPU {self.gpu_id} 利用率: {self.status['gpu_utilizations'][-1]:.2f}%")
            print(f"GPU {self.gpu_id} 显存使用: {self.status['gpu_memory_usages'][-1]:.2f} MB")
            
        print("-------------------") 