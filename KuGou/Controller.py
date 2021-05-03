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
            print("The basic information of the music :")
            print(f"\tName: {OneMusic.Name}")
        try:
            Result = KuGou.Tools.GetMusicInfo(OneMusic)
            if DebugFlag:
                print("\tSuccessful !")
        except Exception:
            if DebugFlag:
                print("\tFailed !")
            continue
        Result.Save(FilePath, LrcFile, ForceReplace)
        if DebugFlag:
            print("The details of this song :")
            print(f"\tName: {Result.Name}")
            print(f"\tAlbum: {Result.Album}")
            print(f"\tAuthor: {Result.AuthorName}")
            print(f"\tSong Source: {Result.MusicSource}")
            print(f"\tFrom: {Result.From}")
            print("\n")
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
        raise ValueError("The return value of the Function 'Selector' is incorrect .")
    if not (Result.FileHash or Result.FileId) and Result.Name:
        raise ValueError("The return value of the Function 'Selector' is incorrect .")
    if not Result.AlbumID:
        Result.AlbumID = ""
    if DebugFlag:
        print("The basic information of the music :")
        print(f"\tName: {Result.Name}")
    if DebugFlag:
        print("Ready to download . . .", end="")
    Result = KuGou.Tools.GetMusicInfo(Result)
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
    Musics = KuGou.MusicList()
    Musics.Load(KuGou.MusicList.Json, MusicSheetPath)
    Musics.Append(Result)
    Musics.Save(KuGou.MusicList.Json, MusicSheetPath)
    return None
