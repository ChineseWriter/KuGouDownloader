# coding = UTF-8


import os

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
Require = os.path.abspath("./KuGou/KuGouRequirement.txt")
Logo = os.path.abspath("./KuGou/logo.ico")
Version = "1.0.1"

with open("./KuGou/README.md", "r", encoding="UTF-8") as File:
    Describe = File.read()
del File

from KuGou.Exceptions import KuGouException

from KuGou.Tools import Music
from KuGou.Tools import MusicList

from KuGou import Requirement
from KuGou import Tools

from KuGou.Controller import Download, ReDownload
