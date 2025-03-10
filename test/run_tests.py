#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
运行所有测试用例的脚本
"""

import unittest
import sys
import os

# 添加项目根目录到 Python 路径
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# 导入测试模块
from test_local import TestLocal
from test_remote import TestRemote
from test_resource_monitor import TestResourceMonitor

def run_all_tests():
    """运行所有测试用例"""
    # 创建测试套件
    test_suite = unittest.TestSuite()
    
    # 添加测试类
    test_suite.addTest(unittest.makeSuite(TestLocal))
    test_suite.addTest(unittest.makeSuite(TestRemote))
    test_suite.addTest(unittest.makeSuite(TestResourceMonitor))
    
    # 运行测试
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(test_suite)
    
    # 返回测试结果
    return result.wasSuccessful()

def run_specific_test(test_name):
    """运行特定的测试模块"""
    if test_name == "local":
        test_suite = unittest.makeSuite(TestLocal)
    elif test_name == "remote":
        test_suite = unittest.makeSuite(TestRemote)
    elif test_name == "resource_monitor":
        test_suite = unittest.makeSuite(TestResourceMonitor)
    elif test_name == "resource_monitor_demo":
        # 运行资源监控演示
        from test_resource_monitor import run_cpu_intensive_task
        run_cpu_intensive_task()
        return True
    else:
        print(f"未知的测试名称: {test_name}")
        return False
    
    # 运行测试
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(test_suite)
    
    # 返回测试结果
    return result.wasSuccessful()

if __name__ == "__main__":
    # 检查命令行参数
    if len(sys.argv) > 1:
        # 运行特定测试
        success = run_specific_test(sys.argv[1])
    else:
        # 运行所有测试
        success = run_all_tests()
    
    # 设置退出码
    sys.exit(0 if success else 1) 