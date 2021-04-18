# coding = UTF-8


import os
import inspect

import KuGou


def ReDownload(MusicSheetPath: str = "./KuGouMusicList.json", FilePath: str = "./",
               LrcFile: bool = False, DebugFlag: bool = False, ForceReplace: bool = False) -> None:
    Musics = KuGou.MusicList()
    Musics.Load(KuGou.MusicList.Json, MusicSheetPath)
    if DebugFlag:
        print("Download the songs in the song list again .")
    for OneMusic in Musics.AllItem():
        OneMusic: KuGou.Music
        if DebugFlag:
            print("The basic information of the music :\n\t" + str(OneMusic.Name) + " .")
            print("\tReady to download again . . .", end="")
        if OneMusic.From == KuGou.Music.From_KuGou:
            Result = KuGou.Tools.GetMusicInfo(OneMusic.AlbumID, OneMusic.FileHash)
            Result.Save(FilePath, LrcFile, ForceReplace)
        if DebugFlag:
            print(" Successful !")
    return None


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
    Result = KuGou.Tools.GetMusicList(MusicName)
    Result = Selector(Result)
    if not isinstance(Result, dict):
        raise ValueError("The return value of the Function 'Selector' is incorrect .")
    if len(Result) != 4:
        raise ValueError("The return value of the Function 'Selector' is incorrect .")
    if not Result.get("FileHash") and Result.get("FileName"):
        raise ValueError("The return value of the Function 'Selector' is incorrect .")
    if not Result.get("AlbumID"):
        Result["AlbumID"] = ""
    if DebugFlag:
        print("The basic information of the music :\n\t" + str(Result) + " .")
    if DebugFlag:
        print("Ready to download . . .", end="")
    Result = KuGou.Tools.GetMusicInfo(Result["AlbumID"], Result["FileHash"])
    Result.Save(FilePath, LrcFile, ForceReplace)
    if DebugFlag:
        print(" Successful !")
    Musics = KuGou.MusicList()
    Musics.Load(KuGou.MusicList.Json, MusicSheetPath)
    Musics.Append(Result)
    Musics.Save(KuGou.MusicList.Json, MusicSheetPath)
    return None
