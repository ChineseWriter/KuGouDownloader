# coding = UTF-8


import os
import sys

Version = "1.0.2"
Author = "Amundsen Severus Rubeus Bjaaland"


class SUPPORTED(object):
    KuGou = "KuGou"
    WangYiYun = "WangYiYun"

    ALL = [KuGou, WangYiYun]


try:
    Require = os.path.abspath("./KuGou/KuGouRequirement.txt")
    Logo = os.path.abspath("./KuGou/logo.ico")
except FileNotFoundError:
    pass

try:
    with open("./KuGou/README.md", "r", encoding="UTF-8") as File:
        Describe = File.read()
    del File
except FileNotFoundError:
    pass

ModulePath = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

if ModulePath not in sys.path:
    sys.path.append(ModulePath)
    RemoveFlag = True
else:
    RemoveFlag = False

from .Tools import Music
from .Tools import MusicList

from .Tools import CheckMusic

from KuGou import Requirement
from KuGou import Tools

from .Controller import Download, ReDownload

if RemoveFlag:
    sys.path.remove(ModulePath)
