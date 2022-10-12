# from binbox import remote
import binbox


if __name__ == "__main__":
    # 构建 ssh 连接
    host0 = binbox.remote("120.78.172.67", 22, "root")

    # 在远端执行命令
    ret = host0("ls")
    ret = host0("pwd")
    ret = host0("echo 1111 > tmp.log")
    ret = host0("cat tmp.log")

    # 从远端获取文件
    host0.get("tmp.log", "tmp111.log")
    
    # 将本地文件拷贝到远端
    host0.put("tmp111.log", "tmp2222.log")

    ret = host0("ls")
