# coding = UTF-8
"""对所有下载器进行封装，可操作多个网站的数据。"""
import warnings

import KuGou


def GetMusicList(MusicName: str) -> list:
    """获取歌单列表并返回。

    使用目前已有的网站下载器中的查询组件获取歌曲，将其拼接为一个列表并返回。

    ::Usage:
        >>> GetMusicList("匆匆那年 王菲")

    :param MusicName: 要获取的歌曲名，必须为str类型。
    :return: 歌曲列表，为list类型
    """
    assert isinstance(MusicName, str)
    Creator1 = KuGou.Tools.KuGouMusicList(MusicName)
    Creator2 = KuGou.Tools.WangYiYunMusicList(MusicName)
    Creator3 = KuGou.Tools.QQMusicList(MusicName)
    MusicList1 = Creator1.GetMusicList()
    MusicList2 = Creator2.GetMusicList()
    MusicList3 = Creator3.GetMusicList()
    MusicList = MusicList1 + MusicList2 + MusicList3
    return MusicList


def GetMusicInfo(MusicItem):  # -> KuGou.Music:
    """获取歌曲的相关数据"""
    MusicItem: KuGou.Music()
    if MusicItem.From == KuGou.Music.From_KuGou:
        Got = KuGou.Tools.KuGouMusicInfo(MusicItem)
    elif MusicItem.From == KuGou.Music.From_WangYiYun:
        Got = KuGou.Tools.WangYiYunMusicInfo(MusicItem)
    elif MusicItem.From == KuGou.Music.From_QQ:
        Got = KuGou.Tools.QQMusicInfo(MusicItem)
    else:
        warnings.warn("下载该网站的歌曲目前不被支持。")
        return None
    Result = Got.GetMusicInfo()
    return Result
