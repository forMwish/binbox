import paramiko
from scp import SCPClient
import getpass
try:
    from . import _tool
except:
    import _tool

class remote:
    """ 提供在远端执行命令，以及本地和远端之间通过 scp 进行文件拷贝的功能
        执行命令或者拷贝时，如果异常，则打印异常 log 并返回 1
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
        command=_tool.command_clear(command)
        print(f"[binbox] remote:{command}")
        ret = self._ssh.exec_command(command)
        stdout = ret[1].read().decode("utf-8")
        stderr = ret[2].read().decode("utf-8")
        if stdout !="":
            print(stdout)
        if stderr != "":
            print(stderr)
            raise Exception(f"[binbox][error] run \"{command}\" failed")

    def get(self, remote_path, local_path="", recursive=False):
        try:
            self._scp.get(remote_path, local_path, recursive)
        except Exception as err:
            print(f"[error] {err}")
            raise Exception(f"[binbox][error] get file from remote failed")
    
    def put(self, files, remote_path=".", recursive=False):
        try:
            self._scp.put(files, remote_path, recursive)
        except Exception as err:
            print("[error] {err}")
            raise Exception(f"[binbox][error] put file to remote failed")


