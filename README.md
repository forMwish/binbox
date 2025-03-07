# BinBox

这是一个个人 Python 工具仓库，包含各种实用工具和组件，用于简化日常开发和研究工作。

## 安装

### 基本安装

```bash
pip install .
```

这将安装基本功能，包括 `remote` 和 `local` 命令执行工具。

### 安装特定功能

BinBox 支持不同的安装选项，以满足不同的需求：

```bash
# 安装资源监控功能（CPU 和内存监控）
pip install .[monitor]

# 安装 GPU 监控功能
pip install .[gpu]

# 安装所有功能
pip install .[all]
```

### 开发环境安装

如果您想参与开发或运行测试，可以使用 `requirements.txt` 安装所有依赖（包括开发依赖）：

```bash
pip install -r requirements.txt
```

### 从 PyPI 安装（未发布）

```bash
# 基本安装
pip install binbox

# 安装特定功能
pip install binbox[monitor]
pip install binbox[gpu]
pip install binbox[all]
```

## 工具列表

### ResourceMonitor

资源监控工具，用于跟踪程序运行时的 CPU、内存和 GPU 资源使用情况。可以实时监控并统计资源使用的平均值和峰值。

#### 功能特点

- 实时监控 CPU 使用率
- 跟踪内存使用量（MB）
- 监控 GPU 利用率和显存使用情况
- 自动计算资源使用的平均值和峰值
- 支持多线程监控，不影响主程序执行
- 可配置的监控间隔和状态打印频率

#### 使用示例

```python
from binbox.ResourceMonitor import ResourceMonitor
# 或者
from binbox import ResourceMonitor

# 创建监控器
monitor = ResourceMonitor()

# 开始监控（interval: 监控间隔，gpu_id: GPU ID，interval_print: 打印状态间隔）
monitor.start(interval=1.0, gpu_id=0, interval_print=2.0)

# 执行需要监控的代码
# ...

# 停止监控并获取统计结果
stats = monitor.stop()
```

#### 输出示例

监控过程中会实时打印资源使用情况：
```
当前状态 - CPU: 45.2% | 内存: 1024.5MB | GPU: 78.3% | GPU内存: 3072.1MB
```

监控结束后会输出统计结果：
```
ResourceMonitor:
    CPU 平均使用率: 42.35%
    内存平均使用量: 1015.67 MB
    内存峰值使用量: 1256.89 MB
    GPU 平均使用率: 75.42%
    GPU 显存峰值使用量: 3584.25 MB
```

### local

用于在本地执行命令行命令，并处理输出结果。

#### 功能特点

- 执行本地命令并捕获输出
- 支持日志记录到文件
- 自动处理命令执行错误

#### 使用示例

```python
from binbox import local

# 执行本地命令并获取输出
output = local("ls -la")

# 执行命令并将输出保存到日志文件
output = local("find /path -name '*.py'", log="search_results.log")

# 执行命令但不打印输出到控制台
output = local("grep 'pattern' file.txt", logout=False)
```

### remote

用于在远程服务器上执行命令和传输文件。

#### 功能特点

- 远程命令执行
- 支持 SCP 文件传输（上传和下载）
- 自动处理 SSH 连接和认证

#### 使用示例

```python
from binbox import remote

# 创建远程连接
ssh = remote("example.com", 22, "username")

# 执行远程命令
ssh("ls -la")

# 从远程服务器下载文件
ssh.get("/remote/path/file.txt", "local/path/")

# 上传文件到远程服务器
ssh.put("local/file.txt", "/remote/path/")

# 递归下载目录
ssh.get("/remote/directory", "local/path/", recursive=True)

# 递归上传目录
ssh.put("local/directory", "/remote/path/", recursive=True)
```

## 环境要求

- Python 3.6+
- psutil
- torch (GPU 监控需要)
- paramiko (远程操作需要)
- scp (远程文件传输需要)