# coding = UTF-8


import os
import inspect

import KuGou


def ReDownload(MusicSheetPath: str = "./KuGouMusicList.json", FilePath: str = "./",
               LrcFile: bool = False, DebugFlag: bool = False, ForceReplace: bool = False) -> None:
    Musics = KuGou.MusicList()
    Musics.Load(KuGou.MusicList.Json, MusicSheetPath)
    if DebugFlag:
        print("Download the songs in the song list again .\n")
    Counter = 0
    for OneMusic in Musics.AllItem():
        OneMusic: KuGou.Music
        Counter += 1
        if DebugFlag:
            print(f"This is the {Counter} Item .")
        DownloadMusic(OneMusic, FilePath, ForceReplace, DebugFlag, LrcFile)
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
    if not isinstance(Result, KuGou.Music):
        if not isinstance(Result, list):
            raise ValueError("The return value of the Function 'Selector' is incorrect .")
    if isinstance(Result, KuGou.Music):
        if not (Result.FileHash or Result.FileId) and Result.Name:
            raise ValueError("The return value of the Function 'Selector' is incorrect .")
        Result = DownloadMusic(Result, FilePath, ForceReplace, DebugFlag, LrcFile)
    else:
        Result: list
        Buffer = []
        Counter = 0
        for i in Result:
            i: KuGou.Music
            Counter += 1
            if not (i.FileHash or i.FileId) and i.Name:
                raise ValueError("The return value of the Function 'Selector' is incorrect .")
            if DebugFlag:
                print(f"This is the {Counter} Item .")
            Buffer.append(DownloadMusic(i, FilePath, ForceReplace, DebugFlag, LrcFile))
        Result = Buffer
    Musics = KuGou.MusicList()
    Musics.Load(KuGou.MusicList.Json, MusicSheetPath)
    if isinstance(Result, KuGou.Music):
        Musics.Append(Result)
    else:
        for i in Result:
            Musics.Append(i)
    Musics.Save(KuGou.MusicList.Json, MusicSheetPath)
    return None


def DownloadMusic(MusicItem: KuGou.Music, FilePath: str = "./", ForceReplace: bool = False, DebugFlag: bool = False,
                  LrcFile: bool = True):
    if DebugFlag:
        print("The basic information of the music :")
        print(f"\tName: {MusicItem.Name}")
    if DebugFlag:
        print("Ready to download . . .", end="")
    try:
        Result = KuGou.Tools.GetMusicInfo(MusicItem)
    except Exception as AllError:
        if DebugFlag:
            print(f"Failed : {repr(AllError)}")
        return None
    Result.Save(FilePath, LrcFile, ForceReplace)
    if DebugFlag:
        print(" Successful !")
    if DebugFlag:
        print("The details of this song :")
        print(f"\tName: {Result.Name}")
        print(f"\tAlbum: {Result.Album}")
        print(f"\tAuthor: {Result.AuthorName}")
        print(f"\tSong Source: {Result.MusicSource}")
        print(f"\tFrom: {Result.From}")
    return Result
