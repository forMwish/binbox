# from binbox import remote
import binbox
import unittest
import os
import tempfile


class TestRemote(unittest.TestCase):
    """测试 Remote 类的功能"""
    
    def setUp(self):
        """测试前的准备工作"""
        # 使用 127.0.0.1 作为测试主机
        self.host = binbox.Remote("127.0.0.1", 22, os.environ.get("USER", "root"))
        
        # 创建临时测试文件
        self.temp_dir = tempfile.mkdtemp()
        self.local_test_file = os.path.join(self.temp_dir, "local_test.txt")
        self.remote_test_file = os.path.join(self.temp_dir, "remote_test.txt")
        
        with open(self.local_test_file, "w") as f:
            f.write("这是一个测试文件内容")
    
    def tearDown(self):
        """测试后的清理工作"""
        # 删除测试文件
        if os.path.exists(self.local_test_file):
            os.remove(self.local_test_file)
        
        if os.path.exists(self.remote_test_file):
            os.remove(self.remote_test_file)
            
        # 删除临时目录
        if os.path.exists(self.temp_dir):
            os.rmdir(self.temp_dir)
    
    def test_command_execution(self):
        """测试远程命令执行"""
        # 测试基本命令
        ret = self.host("ls")
        self.assertEqual(ret, 0)
        
        ret = self.host("pwd")
        self.assertEqual(ret, 0)
        
        # 测试创建文件
        test_content = "测试内容123"
        ret = self.host(f"echo '{test_content}' > {self.remote_test_file}")
        self.assertEqual(ret, 0)
        
        # 测试读取文件
        ret = self.host(f"cat {self.remote_test_file}")
        self.assertEqual(ret, 0)
    
    def test_file_transfer(self):
        """测试文件传输功能"""
        # 测试上传文件
        ret = self.host.put(self.local_test_file, self.remote_test_file)
        self.assertEqual(ret, 0)
        
        # 验证文件上传成功
        ret = self.host(f"cat {self.remote_test_file}")
        self.assertEqual(ret, 0)
        
        # 测试下载文件
        local_download = os.path.join(self.temp_dir, "downloaded.txt")
        ret = self.host.get(self.remote_test_file, local_download)
        self.assertEqual(ret, 0)
        
        # 验证文件下载成功
        self.assertTrue(os.path.exists(local_download))
        
        # 清理下载的文件
        if os.path.exists(local_download):
            os.remove(local_download)
    
    def test_nonexistent_file(self):
        """测试处理不存在的文件"""
        # 测试获取不存在的文件
        nonexistent_file = os.path.join(self.temp_dir, "nonexistent.txt")
        ret = self.host.get(nonexistent_file, "tmp_download.txt")
        self.assertEqual(ret, 1)  # 应该返回错误码 1
        
        # 清理可能创建的文件
        if os.path.exists("tmp_download.txt"):
            os.remove("tmp_download.txt")


# 兼容旧的测试方式
def legacy_test():
    # 构建 ssh 连接
    host0 = binbox.Remote("127.0.0.1", 22, os.environ.get("USER", "root"))

    # 在远端执行命令
    ret = host0("ls")
    assert(ret == 0)
    ret = host0("pwd")
    assert(ret == 0)
    ret = host0("echo 1111 > tmp.log")
    assert(ret == 0)
    ret = host0("cat tmp.log")
    assert(ret == 0)

    # 从远端获取文件
    ret = host0.get("tmp.log", "tmp111.log")
    assert(ret == 0)
    ret = host0.get("tmp44444.log", "tmp111.log")
    assert(ret == 0)

    # 将本地文件拷贝到远端
    ret = host0.put("tmp111.log", "tmp2222.log")
    assert(ret == 0)

    ret = host0("ls")
    assert(ret == 0)
    
    # 清理测试文件
    host0("rm -f tmp.log tmp2222.log")
    if os.path.exists("tmp111.log"):
        os.remove("tmp111.log")


if __name__ == "__main__":
    unittest.main()
