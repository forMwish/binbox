import subprocess
try:
    from . import _tool
except:
    import _tool


def local(command:str, log=None):
    """ 在本地执行命令，并把结果(stdout/stderr)打印
        返回 stdout 
    """
    if log !=None:
        fp = open(log, "w")

    command=_tool.command_clear(command)
    out_list = []
    print(f"[binbox] local:{command}")
    ret = subprocess.Popen(command, shell=True,
                     stdin=subprocess.PIPE,
                     stdout=subprocess.PIPE,
                     stderr=subprocess.PIPE, universal_newlines=True, bufsize=1)
    for line in ret.stdout:
        print(line, end="")
        out_list.append(line.strip())
        if log !=None:
            fp.write(line)
            fp.flush()
    ret.wait()
    if log !=None:
        fp.close()
    if ret.returncode == 0:
        return out_list
    else:
        for line in ret.stderr:
            print(line, end="")
        raise Exception(f"[binbox][error] run \"{command}\" failed")


if __name__ == "__main__":
    command="ls -alh test1111"
    command="find / -name \"*.so\""

    ret = local(command)
    
    pass