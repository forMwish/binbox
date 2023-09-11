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
    out_list = []
    print(f"[binbox] local:{command}")
    process = subprocess.Popen(command, shell=True,
                     stdin=subprocess.PIPE,
                     stdout=subprocess.PIPE,
                     stderr=subprocess.PIPE, universal_newlines=True, bufsize=0)
    while True:
        line = process.stdout.readline()
        if line == '' and process.poll() is not None: 
            break
        if logout:
            print(line.strip())
        out_list.append(line.strip())
        if log != None:
            fp.write(line)
            fp.flush()
    if log !=None:
        fp.close()
    if process.returncode != 0:
        for line in process.stderr:
            print(line.strip())
        raise Exception(f"[binbox][error] run \"{command}\" failed")
    else:
        return out_list


if __name__ == "__main__":
    command="ls -alh test1111"
    command="find / -name \"*.so\""

    ret = local(command)
    
    pass