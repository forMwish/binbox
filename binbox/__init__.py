"""
BinBox - 个人 Python 工具库
包含各种实用工具和组件，用于简化日常开发和研究工作。
"""

__version__ = '1.0'

# 基本工具
from .remote import remote
from .local import local
from .local_v2 import local_v2
from .color import *
from ._tool import command_clear

# 资源监控工具 - 条件导入
try:
    from .ResourceMonitor import ResourceMonitor
except ImportError:
    # 如果缺少依赖，提供一个占位符类
    class ResourceMonitor:
        def __init__(self):
            raise ImportError(
                "ResourceMonitor 需要额外的依赖。请使用 'pip install binbox[monitor]' 安装必要的依赖。"
                "如果需要GPU监控功能，请使用 'pip install binbox[gpu]' 或 'pip install binbox[all]'。"
            )

# 设置包的所有导出内容
__all__ = [
    'remote',
    'local',
    'local_v2',
    'ResourceMonitor',
    'command_clear',
    # 颜色常量
    'HEADER', 'OKBLUE', 'OKCYAN', 'OKGREEN', 
    'WARNING', 'FAIL', 'ENDC', 'BOLD', 'UNDERLINE'
]