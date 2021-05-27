# coding = UTF-8
"""下载器核心组件，包括下载器和本地文件管理等。"""

# 导入歌单构造模块和音乐检查模块
from .LocalTools import MusicItem as Music
from .LocalTools import MusicSheet as MusicList

from .LocalTools import CheckMusic

# 导入酷狗音乐必需的下载组件
from .WebTools import KuGouMusicList
from .WebTools import KuGouMusicInfo

# 导入网易云音乐必需的下载组件
from .WebTools import WangYiYunMusicList
from .WebTools import WangYiYunMusicInfo

# 导入聚合管理模块(可聚合并操作多个网站的结果)
from .Controller import GetMusicList, GetMusicInfo
