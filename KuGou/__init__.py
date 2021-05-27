# coding = UTF-8


import os
import sys

Headers = [
    {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/84.0.4147.125 Safari/537.36',
        'referer': 'https://www.kugou.com/yy/html/search.html',
    },
    {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/84.0.4147.125 Safari/537.36',
    },
]
Supported = ["KuGou", "WangYiYun"]
try:
    Require = os.path.abspath("./KuGou/KuGouRequirement.txt")
    Logo = os.path.abspath("./KuGou/logo.ico")
except FileNotFoundError:
    pass
Version = "1.0.1"

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
