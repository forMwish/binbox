import binbox
import time
import os
import sys
import unittest

class TestResourceMonitor(unittest.TestCase):
    """测试 ResourceMonitor 类的功能"""
    
    def test_init(self):
        """测试初始化"""
        monitor = binbox.ResourceMonitor()
        self.assertFalse(monitor.monitoring)
        self.assertIsNotNone(monitor.process)
        self.assertIn("cpu_percentages", monitor.status)
        self.assertIn("memory_usages", monitor.status)
        self.assertIn("gpu_utilizations", monitor.status)
        self.assertIn("gpu_memory_usages", monitor.status)
    
    def test_start_stop(self):
        """测试启动和停止监控"""
        monitor = binbox.ResourceMonitor()
        
        # 启动监控
        monitor.start(interval=0.1, interval_print=1.0)
        self.assertTrue(monitor.monitoring)
        self.assertTrue(monitor.printing)
        self.assertTrue(monitor.monitor_thread.is_alive())
        self.assertTrue(monitor.print_thread.is_alive())
        
        # 执行一些操作以产生资源使用
        for _ in range(10):
            _ = [i * i for i in range(10000)]
            time.sleep(0.1)
        
        # 停止监控并获取统计信息
        stats = monitor.stop()
        self.assertFalse(monitor.monitoring)
        self.assertFalse(monitor.printing)
        
        # 验证统计信息
        self.assertIn("cpu", stats)
        self.assertIn("memory", stats)
        
        # 验证 CPU 统计信息
        self.assertIn("mean", stats["cpu"])
        self.assertIn("max", stats["cpu"])
        self.assertIn("min", stats["cpu"])
        
        # 验证内存统计信息
        self.assertIn("mean", stats["memory"])
        self.assertIn("max", stats["memory"])
        self.assertIn("min", stats["memory"])
        
        # 验证数据收集
        self.assertGreater(len(monitor.status["cpu_percentages"]), 0)
        self.assertGreater(len(monitor.status["memory_usages"]), 0)


if __name__ == "__main__":
    unittest.main() 