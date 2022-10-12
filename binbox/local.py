import subprocess

def local(command:str):
    ret = subprocess.run(command, shell=True,
                     stdin=subprocess.PIPE,
                     stdout=subprocess.PIPE,
                     stderr=subprocess.PIPE)
    if ret.returncode == 0:
        print(ret.stdout.decode("utf-8"))
    else:
        print(ret.stderr.decode("utf-8"))

    return ret.returncode

if __name__ == "__main__":
    local("ls test111")