# BinBox 测试说明

本目录包含 BinBox 库的测试用例，用于验证各个组件的功能正确性。

## 测试内容

测试用例包括以下几个部分：

1. `test_local.py` - 测试本地命令执行功能
2. `test_remote.py` - 测试远程命令执行和文件传输功能
3. `test_resource_monitor.py` - 测试资源监控功能

## 运行测试

### 运行所有测试

```bash
python run_tests.py
```

### 运行特定测试

```bash
# 运行本地命令测试
python run_tests.py local

# 运行远程命令测试
python run_tests.py remote

# 运行资源监控测试
python run_tests.py resource_monitor

# 运行资源监控演示
python run_tests.py resource_monitor_demo
```

### 直接运行单个测试文件

也可以直接运行单个测试文件：

```bash
python test_local.py
python test_remote.py
python test_resource_monitor.py
```

## 注意事项

1. 远程测试默认使用 `127.0.0.1` 作为测试主机，需要确保 SSH 服务已启动并且可以免密登录。

2. 资源监控测试需要安装 `psutil` 包，如果需要 GPU 监控功能，还需要安装 `torch` 包。

3. 运行测试前，请确保已安装所有依赖：
   ```bash
   pip install -r ../requirements.txt
   ```

4. 如果需要运行资源监控的演示，可以使用：
   ```bash
   python test_resource_monitor.py --demo
   ```
   或者
   ```bash
   python run_tests.py resource_monitor_demo
   ``` 