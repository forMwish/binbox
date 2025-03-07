# setup.py

import os
from setuptools import setup, find_packages

__version__ = '1.0' # 版本号

# 基本依赖
base_requirements = [
    'paramiko>=2.11.0',
    'scp>=0.14.4',
]

# 资源监控依赖
monitor_requirements = [
    'psutil>=5.9.0',
]

# GPU监控依赖
gpu_requirements = [
    'torch>=1.7.0',
]

# 所有依赖
all_requirements = base_requirements + monitor_requirements + gpu_requirements

setup(
    name = 'binbox', # 在pip中显示的项目名称
    version = __version__,
    author = 'muziwenwu',
    author_email = 'li296641798@gmail.com',
    url = 'https://github.com/forMwish/binbox',  # 可以替换为实际的GitHub仓库URL
    description = 'Personal Python toolbox for development and research',
    long_description = open('README.md').read(),
    long_description_content_type = 'text/markdown',
    packages = find_packages(exclude=["test"]), # 项目中需要拷贝到指定路径的文件夹
    python_requires = '>=3.6.0',
    install_requires = base_requirements, # 基本安装依赖
    extras_require = {
        'monitor': monitor_requirements,
        'gpu': gpu_requirements,
        'all': all_requirements,  # 所有依赖
    },
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
    ],
)