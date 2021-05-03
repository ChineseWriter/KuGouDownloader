# coding = UTF-8
"""下载器核心组件，包括下载器和本地文件管理等。"""

# 导入歌单构造模块和音乐检查模块
from KuGou.Tools.LocalTools import MusicItem as Music
from KuGou.Tools.LocalTools import MusicSheet as MusicList

from KuGou.Tools.LocalTools import CheckMusic

# 导入酷狗音乐必需的下载组件
from KuGou.Tools.WebTools import KuGouMusicList
from KuGou.Tools.WebTools import KuGouMusicInfo

# 导入网易云音乐必需的下载组件
from KuGou.Tools.WebTools import WangYiYunMusicList
from KuGou.Tools.WebTools import WangYiYunMusicInfo

# 导入聚合管理模块(可聚合并操作多个网站的结果)
from KuGou.Tools.Controller import GetMusicList, GetMusicInfo
