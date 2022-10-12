# setup.py

import os
from setuptools import setup, find_packages

__version__ = '1.0' # 版本号
requirements = open('requirements.txt').readlines() # 依赖文件

setup(
    name = 'binbox', # 在pip中显示的项目名称
    version = __version__,
    author = 'muziwenwu',
    author_email = 'li296641798@gmail.com',
    url = '',
    description = 'personal tools',
    packages = find_packages(exclude=["test"]), # 项目中需要拷贝到指定路径的文件夹
    python_requires = '>=3.5.0',
    install_requires = requirements # 安装依赖
        )