# coding = UTF-8
"""对所有下载器进行封装，可操作多个网站的数据。"""


import os

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
    Creator = KuGou.Tools.MusicList(MusicName)
    return Creator.GetMusicList()


def GetMusicInfo(AlbumID: str, FileHash: str) -> dict:
    """获取歌曲的相关数据"""
    assert isinstance(AlbumID, str)
    assert isinstance(FileHash, str)
    Got = KuGou.Tools.MusicInfo(AlbumID, FileHash)
    return Got.GetMusicInfo()


def SaveMusic(MusicInfo: dict, Path: str = "./", LrcFile: bool = False, ForceReplace: bool = False) -> None:
    """保存歌曲及歌曲相关数据"""
    assert isinstance(MusicInfo, dict)
    assert isinstance(Path, str)
    assert os.path.exists(Path)
    Music = KuGou.Tools.Music(MusicInfo, Path)
    Music.SaveMusic(LrcFile, ForceReplace)
    return None

