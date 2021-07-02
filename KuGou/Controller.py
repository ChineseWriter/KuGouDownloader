# coding = UTF-8


import os
import inspect
import warnings

import KuGou


def ReDownload(MusicSheetPath: str = "./KuGouMusicList.json", FilePath: str = "./",
               LrcFile: bool = False, DebugFlag: bool = False, ForceReplace: bool = False) -> None:
    try:
        os.mkdir(FilePath)
        if DebugFlag:
            print("Create music file folder successfully .")
    except FileExistsError:
        if DebugFlag:
            print("The music file folder has been created .")
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
             LrcFile: bool = False, DebugFlag: bool = False, ForceReplace: bool = False):
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

        def Selector(x):
            return x[0]
    if not inspect.isfunction(Selector):
        raise ValueError("The Argument 'Selector' must be a function (Executable) .")
    if not MusicName:
        return None
    Result = KuGou.Tools.GetMusicList(MusicName)
    Result = Selector(Result)
    if not isinstance(Result, KuGou.Music):
        if not isinstance(Result, list):
            raise ValueError("The return value of the Function 'Selector' is incorrect .")
    if isinstance(Result, KuGou.Music):
        if not Result.FileId and Result.Name:
            raise ValueError("The return value of the Function 'Selector' is incorrect .")
        Result = DownloadMusic(Result, FilePath, ForceReplace, DebugFlag, LrcFile)
    else:
        Result: list
        if not len(Result):
            return None
        Buffer = []
        Counter = 0
        for OneMusic in Result:
            OneMusic: KuGou.Music
            Counter += 1
            if not OneMusic.FileId and OneMusic.Name:
                raise ValueError("The return value of the Function 'Selector' is incorrect .")
            if DebugFlag:
                print(f"This is the {Counter} Item .")
            SuccessFlag = DownloadMusic(OneMusic, FilePath, ForceReplace, DebugFlag, LrcFile)
            if SuccessFlag:
                Buffer.append(SuccessFlag)
        Result = Buffer
    Buffer = []
    for OneMusic in Result:
        if OneMusic is None:
            continue
        Buffer.append(OneMusic)
    Musics = KuGou.MusicList()
    Musics.Load(KuGou.MusicList.Json, MusicSheetPath)
    if isinstance(Result, KuGou.Music):
        Musics.Append(Result)
    else:
        for OneMusic in Result:
            Musics.Append(OneMusic)
    Musics.Save(KuGou.MusicList.Json, MusicSheetPath)
    return Result


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
        warnings.warn("获取歌曲信息失败。")
        return None
    SuccessFlag = Result.Save(FilePath, LrcFile, ForceReplace)
    if not SuccessFlag:
        warnings.warn("获取歌曲信息失败。")
        return None
    if DebugFlag:
        print(" Successful !")
    if DebugFlag:
        print("The details of this song :")
        print(f"\tName: {Result.Name}")
        print(f"\tAlbum: {Result.Album}")
        print(f"\tAuthor: {Result.Author.Name}")
        print(f"\tSong Source: {Result.MusicSource}")
        print(f"\tFrom: {Result.From}")
    return Result
