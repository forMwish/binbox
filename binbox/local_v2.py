import subprocess, select, sys
try:
    from . import _tool
except:
    import _tool


def local_v2(command:str, log=None, log_to_screen=True):
    """ 在本地执行命令, 如果 stderr 非空, 则 raise 异常
            log: 指向打印的保存路径
            print: 是否打印到 stdout/stderr
        返回 stdout 
    """

    command=_tool.command_clear(command)
    print(command)
    print(f"[binbox] local:{command}")
    process = subprocess.Popen(command, shell=True,
                     stdin=subprocess.PIPE,
                     stdout=subprocess.PIPE,
                     stderr=subprocess.PIPE, universal_newlines=True, bufsize=0)

    log_list = []
    # 不断读取子进程的输出并打印,.以及监控 sys.stdin 以便传递给子进程
    while process.poll() is None:
        rlist, _, _ = select.select([process.stdout, process.stderr, sys.stdin], [], [])
        for src in rlist:
            data = None
            if src is process.stdout:
                data = src.readline()
                if not data:
                    break
                if log_to_screen:
                    print(data, end='')
                log_list.append(data)
            elif src is process.stderr:
                data = src.readline()
                if not data:
                    break
                if log_to_screen:
                    print(data, end='')
                log_list.append(data)
            elif src is sys.stdin:
                data = src.readline()
                process.stdin.write(data)
                process.stdin.flush()
                log_list.append(data)

    # 结束后读取剩余信息
    log_list.extend(process.stdout.readlines())
    log_list.extend(process.stderr.readlines())

    if log != None:
        fp = open(log, "w")
        fp.writelines(log_list)
        fp.close()
    

if __name__ == "__main__":
    import os
    cur_dir = os.path.dirname(os.path.abspath(__file__))
    os.system(f"mkdir {cur_dir}/../tmp")
    os.system(f"gcc {cur_dir}/../test/print_time.c -o {cur_dir}/../tmp/print_time -pthread")
    os.system(f"chmod +x {cur_dir}/../tmp/print_time")

    command=f"{cur_dir}/../tmp/print_time"
    print(command)
    ret = local_v2(command, log=f"{cur_dir}/../tmp/print_time.log", log_to_screen=True)
    pass
