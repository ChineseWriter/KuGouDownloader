#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @FileName  :__init__.py
# @Time      :2021/8/19 9:29
# @Author    :Amundsen Severus Rubeus Bjaaland
"""包含该包的元信息(版本，作者，依赖包文件，Logo)，该包的常量(支持的网站)，
导入了部分功能(便捷下载接口，重新下载接口，音乐检查接口)和该包通用对象(Music，MusicList)"""

# 导入所需要的库
import os
import sys

# import logging  # 模块测试用

# 模块版本
Version = "1.0.3"
# 作者名称
Author = "Amundsen Severus Rubeus Bjaaland"


# 模块测试用
# logging.basicConfig(
#     format="[%(asctime)s](%(levelname)s)%(name)s: %(message)s",
#     datefmt="%Y/%m/%d %H:%M:%S",
#     level=logging.DEBUG
# )


# 模块的常量
class SUPPORTED(object):
    """支持的网站及其代号，由代号组成的列表"""
    KuGou = "KuGou"
    WangYiYun = "WangYiYun"
    QQ = "QQ"
    Himalaya = "Himalaya"

    ALL = [KuGou, WangYiYun, QQ, Himalaya]


# 尝试加载相关信息，使用try语句防止该包被PyInstaller打包后无法找到文件
try:
    # 找到该包的依赖包
    Require = os.path.abspath("./KuGou/KuGouRequirement.Text")
    # 找到该包的Logo(KuGou网站的Logo)
    Logo = os.path.abspath("./KuGou/logo.ico")
except FileNotFoundError:
    pass

# 加载该包的绝对路径
ModulePath = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# 将该包的路径加入搜索路径
if ModulePath not in sys.path:
    sys.path.append(ModulePath)
    RemoveFlag = True
else:
    RemoveFlag = False

# 导入该包的依赖
from .Tools import Music
from .Tools import MusicList

from .Tools import CheckMusic

from KuGou import Requirement
from KuGou import Tools

from .Controller import Download, ReDownload

# 在搜索路径中删除该包的路径
if RemoveFlag:
    sys.path.remove(ModulePath)
