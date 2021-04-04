# coding = UTF-8


import os
import inspect

import KuGou


def GetMusicList(MusicName: str) -> list:
    assert isinstance(MusicName, str)
    Creator = KuGou.MusicList(MusicName)
    return Creator.GetMusicList()


def GetMusicInfo(AlbumID: str, FileHash: str) -> dict:
    assert isinstance(AlbumID, str)
    assert isinstance(FileHash, str)
    Got = KuGou.MusicInfo(AlbumID, FileHash)
    return Got.GetMusicInfo()


def SaveMusic(MusicInfo: dict, Path: str = "./", LrcFile: bool = False, ForceReplace: bool = False) -> None:
    assert isinstance(MusicInfo, dict)
    assert isinstance(Path, str)
    assert os.path.exists(Path)
    Music = KuGou.Music(MusicInfo, Path)
    Music.SaveMusic(LrcFile, ForceReplace)
    return None


def ReDownload(MusicSheetPath: str = "./KuGouMusicList.json", FilePath: str = "./",
               LrcFile: bool = False, DebugFlag: bool = False, ForceReplace: bool = False):
    Musics = KuGou.MusicSheet(MusicSheetPath)
    if DebugFlag:
        print("Download the songs in the song list again .")
    for OneMusic in Musics.Musics():
        if DebugFlag:
            print("The basic information of the music :\n\t" + str(OneMusic) + " .")
            print("\tReady to download again . . .", end="")
        Result = GetMusicInfo(OneMusic["AlbumID"], OneMusic["FileHash"])
        SaveMusic(Result, FilePath, LrcFile, ForceReplace)
        if DebugFlag:
            print(" Successful !")


def Download(MusicName: str, Selector=None, MusicSheetPath: str = "./KuGouMusicList.json", FilePath: str = "./",
             LrcFile: bool = False, DebugFlag: bool = False, ForceReplace: bool = False) -> None:
    try:
        os.mkdir(FilePath)
        if DebugFlag:
            print("Create music file folder successfully .")
    except FileExistsError:
        if DebugFlag:
            print("The music file folder has been created .")
    if Selector is None:
        if DebugFlag:
            print("The default song selector will be used .")
        Selector = lambda x: x[0]
    if not inspect.isfunction(Selector):
        raise ValueError("The Argument 'Selector' must be a function (Executable) .")
    Result = GetMusicList(MusicName)
    Result = Selector(Result)
    if not isinstance(Result, dict):
        raise ValueError("The return value of the Function 'Selector' is incorrect .")
    if len(Result) != 3:
        raise ValueError("The return value of the Function 'Selector' is incorrect .")
    if not Result.get("AlbumID") and Result.get("FileHash") and Result.get("FileName"):
        raise ValueError("The return value of the Function 'Selector' is incorrect .")
    if DebugFlag:
        print("The basic information of the music :\n\t" + str(Result) + " .")
    Musics = KuGou.MusicSheet(MusicSheetPath)
    Musics.Add(Result["AlbumID"], Result["FileHash"], Result["FileName"])
    Musics.Save()
    if DebugFlag:
        print("Ready to download . . .", end="")
    SaveMusic(GetMusicInfo(Result["AlbumID"], Result["FileHash"]), FilePath, LrcFile, ForceReplace)
    if DebugFlag:
        print(" Successful !")
    return None
