import subprocess
try:
    from . import _tool
except:
    import _tool


def local(command:str, log=None, logout=True):
    """ 在本地执行命令, 如果 stderr 非空, 则 raise 异常
            log: 指向打印的保存路径
            print: 是否打印到 stdout/stderr
        返回 stdout 
    """
    if log !=None:
        fp = open(log, "w")

    command=_tool.command_clear(command)
    out_list = ""
    print(f"[binbox] local:{command}")
    ret = subprocess.Popen(command, shell=True,
                     stdin=subprocess.PIPE,
                     stdout=subprocess.PIPE,
                     stderr=subprocess.PIPE, universal_newlines=True, bufsize=1)
    for line in ret.stdout:
        if logout:
            print(line, end="")
        out_list += line
        if log !=None:
            fp.write(line)
            fp.flush()
    ret.wait()
    if log !=None:
        fp.close()
    if ret.returncode != 0:
        for line in ret.stderr:
            print(line, end="")
        raise Exception(f"[binbox][error] run \"{command}\" failed")
    else:
        return out_list


if __name__ == "__main__":
    command="ls -alh test1111"
    command="find / -name \"*.so\""

    ret = local(command)
    
    pass