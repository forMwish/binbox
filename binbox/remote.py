import paramiko
from scp import SCPClient
import getpass


class remote:
    """ 提供在远端执行命令，以及本地和远端之间通过 scp 进行文件拷贝的功能
    """
    def __init__(self, hostname, port, user):
        self._ssh = paramiko.SSHClient()
        self._ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

        try:
            self._ssh.connect(hostname, port, user)
        except:
            pw = getpass.getpass("please input passwd for ssh connect:")
            self._ssh.connect(hostname, port, user, pw)
        
        self._scp = SCPClient(self._ssh.get_transport())

    def __call__(self, command):
        ret = self._ssh.exec_command(command)
        stdout = ret[1].read().decode("utf-8")
        stderr = ret[2].read().decode("utf-8")
        if stdout !="":
            print(stdout)
        if stderr != "":
            print(stderr)
        return stdout, stderr

    def get(self, remote_path, local_path="", recursive=False):
        self._scp.get(remote_path, local_path, recursive)
    
    def put(self, files, remote_path=".", recursive=False):
        self._scp.put(files, remote_path, recursive)

