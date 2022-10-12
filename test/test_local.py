# from binbox import remote
import binbox

if __name__ == "__main__":
    ret = binbox.local("ls test111")
    assert(ret == 0)
