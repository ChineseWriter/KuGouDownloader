# coding = UTF-8


import os
import inspect

import KuGou


def ReDownload(MusicSheetPath: str = "./KuGouMusicList.json", FilePath: str = "./",
               LrcFile: bool = False, DebugFlag: bool = False, ForceReplace: bool = False):
    Musics = KuGou.Tools.MusicSheet(MusicSheetPath)
    if DebugFlag:
        print("Download the songs in the song list again .")
    for OneMusic in Musics.Musics():
        if DebugFlag:
            print("The basic information of the music :\n\t" + str(OneMusic) + " .")
            print("\tReady to download again . . .", end="")
        Result = KuGou.Tools.GetMusicInfo(OneMusic["AlbumID"], OneMusic["FileHash"])
        KuGou.Tools.SaveMusic(Result, FilePath, LrcFile, ForceReplace)
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
    Result = KuGou.Tools.GetMusicList(MusicName)
    Result = Selector(Result)
    if not isinstance(Result, dict):
        raise ValueError("The return value of the Function 'Selector' is incorrect .")
    if len(Result) != 3:
        raise ValueError("The return value of the Function 'Selector' is incorrect .")
    if not Result.get("FileHash") and Result.get("FileName"):
        raise ValueError("The return value of the Function 'Selector' is incorrect .")
    if not Result.get("AlbumID"):
        Result["AlbumID"] = ""
    if DebugFlag:
        print("The basic information of the music :\n\t" + str(Result) + " .")
    Musics = KuGou.Tools.MusicSheet(MusicSheetPath)
    Musics.Add(Result["AlbumID"], Result["FileHash"], Result["FileName"])
    Musics.Save()
    if DebugFlag:
        print("Ready to download . . .", end="")
    KuGou.Tools.SaveMusic(KuGou.Tools.GetMusicInfo(Result["AlbumID"], Result["FileHash"]), FilePath, LrcFile, ForceReplace)
    if DebugFlag:
        print(" Successful !")
    return None
