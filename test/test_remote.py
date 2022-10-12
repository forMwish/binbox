# from binbox import remote
import binbox


if __name__ == "__main__":
    # 构建 ssh 连接
    host0 = binbox.remote("120.78.172.67", 22, "root")

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
