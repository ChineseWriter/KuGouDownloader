# coding = UTF-8


import os

import KuGou


def GetMusicList(MusicName: str) -> list:
    assert isinstance(MusicName, str)
    Creator = KuGou.Tools.MusicList(MusicName)
    return Creator.GetMusicList()


def GetMusicInfo(AlbumID: str, FileHash: str) -> dict:
    assert isinstance(AlbumID, str)
    assert isinstance(FileHash, str)
    Got = KuGou.Tools.MusicInfo(AlbumID, FileHash)
    return Got.GetMusicInfo()


def SaveMusic(MusicInfo: dict, Path: str = "./", LrcFile: bool = False, ForceReplace: bool = False) -> None:
    assert isinstance(MusicInfo, dict)
    assert isinstance(Path, str)
    assert os.path.exists(Path)
    Music = KuGou.Tools.Music(MusicInfo, Path)
    Music.SaveMusic(LrcFile, ForceReplace)
    return None

