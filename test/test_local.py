# from binbox import remote
import binbox
import unittest
import os
import tempfile


class TestLocal(unittest.TestCase):
    """测试 local 函数的功能"""
    
    def setUp(self):
        """测试前的准备工作"""
        # 创建临时测试目录和文件
        self.temp_dir = tempfile.mkdtemp()
        self.test_file = os.path.join(self.temp_dir, "test_file.txt")
        
        with open(self.test_file, "w") as f:
            f.write("这是一个测试文件内容")
    
    def tearDown(self):
        """测试后的清理工作"""
        # 删除测试文件
        if os.path.exists(self.test_file):
            os.remove(self.test_file)
            
        # 删除临时目录
        if os.path.exists(self.temp_dir):
            os.rmdir(self.temp_dir)
    
    def test_basic_commands(self):
        """测试基本命令执行"""
        # 测试 ls 命令
        ret = binbox.local("ls")
        self.assertEqual(ret, 0)
        
        # 测试 pwd 命令
        ret = binbox.local("pwd")
        self.assertEqual(ret, 0)
        
        # 测试 echo 命令
        ret = binbox.local("echo 'test content'")
        self.assertEqual(ret, 0)
    
    def test_file_operations(self):
        """测试文件操作命令"""
        # 测试读取文件
        ret = binbox.local(f"cat {self.test_file}")
        self.assertEqual(ret, 0)
        
        # 测试写入文件
        test_output = os.path.join(self.temp_dir, "output.txt")
        ret = binbox.local(f"echo 'new content' > {test_output}")
        self.assertEqual(ret, 0)
        
        # 验证文件写入成功
        self.assertTrue(os.path.exists(test_output))
        
        # 清理创建的文件
        if os.path.exists(test_output):
            os.remove(test_output)


if __name__ == "__main__":
    unittest.main()
