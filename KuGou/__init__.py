# coding = UTF-8


import os

import KuGou.JavaScript as JSRequirements
from KuGou.WebTools import MusicList, MusicInfo, Music
from KuGou.Main import GetMusicList, GetMusicInfo, SaveMusic


__version__ = "1.0.1"
Headers = [
    {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/84.0.4147.125 Safari/537.36',
        'referer': 'https://www.kugou.com/yy/html/search.html',
    },
]
Require = os.path.abspath("./KuGou/KuGouRequirement.txt")
Logo = os.path.abspath("./KuGou/logo.ico")
