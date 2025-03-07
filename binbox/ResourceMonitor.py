import psutil
import time
import os
import statistics
import subprocess
import threading
import torch

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
        """停止监控并返回统计结果"""
        self.monitoring = False
        self.printing = False
        
        if hasattr(self, 'monitor_thread'):
            self.monitor_thread.join(timeout=5.0)
        
        if hasattr(self, 'print_thread'):
            self.print_thread.join(timeout=5.0)
        
        # 计算统计数据
        stats = {
            "cpu_mean": statistics.mean(self.status["cpu_percentages"]) if self.status["cpu_percentages"] else 0,
            "memory_mean_mb": statistics.mean(self.status["memory_usages"]) if self.status["memory_usages"] else 0,
            "memory_peak_mb": max(self.status["memory_usages"]) if self.status["memory_usages"] else 0,
            "gpu_util_mean": statistics.mean(self.status["gpu_utilizations"]) if self.status["gpu_utilizations"] else 0,
            "gpu_memory_peak_mb": max(self.status["gpu_memory_usages"]) if self.status["gpu_memory_usages"] else 0,
        }
        
        print("\n\nResourceMonitor:")
        print(f"\tCPU 平均使用率: {stats['cpu_mean']:.2f}%")
        print(f"\t内存平均使用量: {stats['memory_mean_mb']:.2f} MB")
        print(f"\t内存峰值使用量: {stats['memory_peak_mb']:.2f} MB")
        print(f"\tGPU 平均使用率: {stats['gpu_util_mean']:.2f}%")
        print(f"\tGPU 显存峰值使用量: {stats['gpu_memory_peak_mb']:.2f} MB")

        return self.status
        
    def _monitor_resources(self, interval):
        """
        资源监控线程，定期收集 CPU、内存和 GPU 使用情况
        
        参数:
            interval: 监控的时间间隔（秒）
        """
        current_pid = os.getpid()
        
        while self.monitoring:
            # CPU 使用率 (%)
            self.status["cpu_percentages"].append(self.process.cpu_percent(interval=0))
            
            # 内存使用 (MB)
            memory_info = self.process.memory_info()
            self.status["memory_usages"].append(memory_info.rss / (1024 * 1024))
            
            # GPU 资源
            try:
                # 通过 nvidia-smi 命令获取指定 GPU 的使用情况
                result = subprocess.check_output(
                    ['nvidia-smi', '--query-gpu=index,utilization.gpu,memory.used', 
                     '--format=csv,noheader,nounits', f'--id={self.gpu_id}'],
                    universal_newlines=True
                )
                
                parts = [p.strip() for p in result.strip().split(',')]
                if len(parts) >= 3:
                    self.status["gpu_utilizations"].append(float(parts[1]))   # GPU 利用率 (%)
                    self.status["gpu_memory_usages"].append(float(parts[2]))  # 显存使用量 (MB)
                    
            except (subprocess.SubprocessError, ValueError, IndexError) as e:
                print(f"GPU 监控错误: {e}")
                pass  # 忽略错误
            
            time.sleep(interval)
    
    def _print_status_loop(self, interval_print):
        """
        打印状态的循环线程，定期显示当前资源使用情况
        
        参数:
            interval_print: 打印状态的时间间隔（秒）
        """
        while self.printing:
            self._display_current_status()
            time.sleep(interval_print)

    def _display_current_status(self):
        """显示当前资源状态，包括 CPU、内存、GPU 利用率和 GPU 显存使用情况"""
        if not self.status["cpu_percentages"] or not self.status["memory_usages"]:
            return
            
        cpu = self.status["cpu_percentages"][-1]
        memory = self.status["memory_usages"][-1]
        gpu_util = self.status["gpu_utilizations"][-1] if self.status["gpu_utilizations"] else 0
        gpu_mem = self.status["gpu_memory_usages"][-1] if self.status["gpu_memory_usages"] else 0
        
        print(f"当前状态 - CPU: {cpu:.1f}% | 内存: {memory:.1f}MB | GPU: {gpu_util:.1f}% | GPU内存: {gpu_mem:.1f}MB")


if __name__ == "__main__":
    try:
        # 检查 CUDA 是否可用
        if not torch.cuda.is_available():
            print("CUDA 不可用，无法进行 GPU 测试")
            exit()
            
        print("\n开始 GPU 矩阵乘法测试...")
        
        # 创建监控器
        monitor = ResourceMonitor()
        
        # 开始监控
        monitor.start(interval=0.1, interval_print=0.5, gpu_id=0)
        
        # 在 GPU 上创建大矩阵
        size = 5000  # 矩阵大小
        a = torch.randn(size, size, device='cuda')
        b = torch.randn(size, size, device='cuda')
        
        # 执行多次矩阵乘法
        for i in range(1000):
            # print(f"执行第 {i+1} 次矩阵乘法...")
            c = torch.matmul(a, b)
            # 确保计算完成
            torch.cuda.synchronize()
            # time.sleep(1)
        
        # 停止监控并获取结果
        stats = monitor.stop()
        print(stats)
        # 清理 GPU 内存
        del a, b, c
        torch.cuda.empty_cache()
        

        
    except ImportError:
        print("未安装 PyTorch，无法进行 GPU 测试")
    except Exception as e:
        print(f"GPU 测试出错: {e}")
    