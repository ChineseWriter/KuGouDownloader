# coding = UTF-8


import os
import copy
import eyed3


class Check(object):
    def __init__(self, Path: str = "./") -> None:
        assert isinstance(Path, str)
        assert os.path.exists(Path)
        self.__Path = Path.rstrip("\\").rstrip("/")
        self.__VIPMusic = self.__CheckVIP()
        self.__TooShortMusic = self.__CheckTooShort()

    @property
    def Path(self):
        return self.__Path

    @Path.setter
    def Path(self, Path: str = "./"):
        assert isinstance(Path, str)
        assert os.path.exists(Path)
        self.__Path = Path.rstrip("\\").rstrip("/")

    @property
    def VIPMusic(self):
        return copy.deepcopy(self.__VIPMusic)

    @property
    def TooShortMusic(self):
        return copy.deepcopy(self.__TooShortMusic)

    def __CheckVIP(self):
        Buffer = []
        for i in os.listdir(self.__Path):
            if os.path.splitext(i)[1] == ".mp3":
                if 59.5 <= eyed3.load(self.__Path + "/" + i).info.time_secs <= 60.5:
                    Buffer.append(i)
        return Buffer

    def __CheckTooShort(self):
        Buffer = []
        for i in os.listdir(self.__Path):
            if os.path.splitext(i)[1] == ".mp3":
                if eyed3.load(self.__Path + "/" + i).info.time_secs <= 59.5:
                    Buffer.append(i)
        return Buffer

    def DeleteVIPMusic(self, LrcFile: bool = True, DebugFlag: bool = False) -> None:
        for i in self.__VIPMusic:
            self.__DeleteItem(i, LrcFile, DebugFlag)
        return None

    def DeleteTooShortMusic(self, LrcFile: bool = True, DebugFlag: bool = False) -> None:
        for i in self.__TooShortMusic:
            self.__DeleteItem(i, LrcFile, DebugFlag)
        return None

    def __DeleteItem(self, Item, LrcFile: bool = True, DebugFlag: bool = False):
        Item = os.path.splitext(Item)[0]
        if DebugFlag:
            print(f"Remove : {Item}")
        try:
            os.remove(self.__Path + "/" + Item + ".mp3")
        except FileNotFoundError:
            pass
        if LrcFile:
            try:
                os.remove(self.__Path + "/" + Item + ".lrc")
            except FileNotFoundError:
                pass
