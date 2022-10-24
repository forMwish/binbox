import subprocess
try:
    from . import _tool
except:
    import _tool


def local(command:str):
    """ 在本地执行命令，并把结果(stdout/stderr)打印
        返回 stdout 
    """
    command=_tool.command_clear(command)
    print(f"[binbox] local:{command}")
    ret = subprocess.run(command, shell=True,
                     stdin=subprocess.PIPE,
                     stdout=subprocess.PIPE,
                     stderr=subprocess.PIPE)
    if ret.returncode == 0:
        print(ret.stdout.decode("utf-8"))
    else:
        print(ret.stderr.decode("utf-8"))
        raise Exception(f"[binbox][error] run \"{command}\" failed")

    return ret.stdout

if __name__ == "__main__":
    ret = local("ls test111")
    pass