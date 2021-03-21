# coding = UTF-8


import KuGou
import os


def GetMusicList(MusicName: str) -> list:
    assert isinstance(MusicName, str)
    Creator = KuGou.MusicList(MusicName)
    return Creator.GetMusicList()


def GetMusicInfo(AlbumID: str, FileHash: str) -> dict:
    assert isinstance(AlbumID, str)
    assert isinstance(FileHash, str)
    Got = KuGou.MusicInfo(AlbumID, FileHash)
    return Got.GetMusicInfo()


def SaveMusic(MusicInfo: dict, Path: str = "./") -> None:
    assert isinstance(MusicInfo, dict)
    assert isinstance(Path, str)
    assert os.path.exists(Path)
    Music = KuGou.Music(MusicInfo, Path)
    Music.SaveMusic()
    return None

