# coding = UTF-8


import os
import json
import copy

import eyed3

import KuGou


class MusicSheet(object):
    def __init__(self, Path: str = "./KuGouMusicList.json") -> None:
        if os.path.exists(Path):
            if os.path.isfile(Path):
                File = json.load(open(Path, "r", encoding="UTF-8"))
                self.__Musics = File["List"]
                self.__Information = File["Info"]
            else:
                raise
        else:
            with open(Path, "w", encoding="UTF-8") as File:
                File.write('{"Info": {"MaxNumber": 1000000}, "List": []}')
            self.__Musics = []
            self.__Information = {"MaxNumber": 1000000}
        self.__Path = Path
        self.__Information["MusicSheetVersion"] = "1.0.0"
        self.__Information["MusicDownloaderVersion"] = KuGou.Version
        self.__MaxNumber = self.__Information["MaxNumber"]

    def Add(self, AlbumID: str, FileHash: str, FileName: str = "") -> dict:
        self.__Musics: list
        assert isinstance(AlbumID, str)
        assert isinstance(FileHash, str)
        assert isinstance(FileName, str)
        OneMusic = {"FileName": FileName, "FileHash": FileHash, "AlbumID": AlbumID}
        if OneMusic not in self.__Musics:
            self.__Musics.append(OneMusic)
        if len(self.__Musics) >= self.__MaxNumber:
            pass
        return copy.deepcopy(OneMusic)

    def DropByAlbumID(self, AlbumID: str) -> None:
        assert isinstance(AlbumID, str)
        self.__Musics: list
        for OneMusic in self.__Musics:
            OneMusic: dict
            if OneMusic.get("AlbumID") == AlbumID:
                self.__Musics.remove(OneMusic)
        return None

    def DropByFileHash(self, FileHash: str) -> None:
        assert isinstance(FileHash, str)
        self.__Musics: list
        for OneMusic in self.__Musics:
            OneMusic: dict
            if OneMusic.get("FileHash") == FileHash:
                self.__Musics.remove(OneMusic)
        return None

    def DropByFileName(self, FileName: str) -> None:
        assert isinstance(FileName, str)
        self.__Musics: list
        for OneMusic in self.__Musics:
            OneMusic: dict
            if OneMusic.get("FileName") == FileName:
                self.__Musics.remove(OneMusic)
        return None

    def Save(self) -> None:
        json.dump({"Info": self.__Information, "List": self.__Musics}, open(self.__Path, "w", encoding="UTF-8"))
        return None

    def Musics(self) -> dict:
        for OneMusic in self.__Musics:
            yield OneMusic

    def GetMusics(self) -> list:
        return copy.deepcopy(self.__Musics)

    def GetSheetVersion(self) -> str:
        return self.__Information["MusicSheetVersion"]

    def GetDownloaderVersion(self) -> str:
        return self.__Information["MusicDownloaderVersion"]

    def SetMaxNumber(self, Number: int) -> None:
        if isinstance(Number, int):
            if Number > 0:
                self.__MaxNumber = Number
                self.__Information["MaxNumber"] = Number
        return None


class CheckMusic(object):
    def __init__(self, Path: str = "./") -> None:
        assert os.path.exists(Path)
        self.__Path = Path
        if self.__Path[-1] != ("\\" or "/"):
            self.__Path = self.__Path + "/"
        self.__Musics = \
            [self.__Path + Music if os.path.splitext(Music)[1] == ".mp3" else "Error" for Music in os.listdir(self.__Path)]
        Buffer = []
        for i in self.__Musics:
            if i == "Error":
                continue
            Buffer.append(i)
        self.__Musics = Buffer

    def DeleteTooShortMusic(self, InputFlag: bool = True) -> None:
        for i in self.__Musics:
            MusicPath = i
            LrcPath = self.__Path + os.path.splitext(os.path.split(i)[1])[0] + ".lrc"
            if eyed3.load(i).info.time_secs <= 65:
                if InputFlag:
                    Text = input("Really ? ")
                    if Text == ("Y" or "y"):
                        try:
                            os.remove(MusicPath)
                            os.remove(LrcPath)
                        except FileNotFoundError:
                            pass
                    else:
                        pass
                else:
                    try:
                        os.remove(MusicPath)
                        os.remove(LrcPath)
                    except FileNotFoundError:
                        pass
        return None
