#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @FileName  :MusicSheet.py
# @Time      :2021/6/27 11:34
# @Author    :Amundsen Severus Rubeus Bjaaland


import time, copy

import KuGou

from ..MusicSheet import VERSION
from .MusicItem import MusicItem
from .PreservationManager import Manager


class SheetInfo(object):
    def __init__(self, Creator: str = "Machine", MaxNumber: int = 1000, CreateTime: float = 0.0,
                 RevisionTime: float = 0.0) -> None:
        assert isinstance(Creator, str)
        assert isinstance(MaxNumber, int)
        assert isinstance(CreateTime, float)
        assert isinstance(RevisionTime, float)
        self.__DownloaderVersion = KuGou.Version
        self.__Version = VERSION
        self.__Creator = [Creator]
        self.__MaxNumber = MaxNumber
        self.__CreateTime = CreateTime if CreateTime else time.time()
        self.__RevisionTime = RevisionTime if RevisionTime else time.time()

    @property
    def DownloaderVersion(self):
        return self.__DownloaderVersion

    @property
    def Version(self):
        return self.__Version

    @property
    def Creator(self):
        return self.__Creator

    @property
    def MaxNumber(self):
        return self.__MaxNumber

    @property
    def CreateTime(self):
        return self.__CreateTime

    @property
    def RevisionTime(self):
        return self.__RevisionTime

    def AddCreator(self, Creator: str = "Machine"):
        assert isinstance(Creator, str)
        if Creator not in self.__Creator:
            self.__Creator.append(Creator)

    def DropCreator(self, Creator: str = "Machine"):
        assert isinstance(Creator, str)
        if Creator in self.__Creator:
            self.__Creator.remove(Creator)

    @MaxNumber.setter
    def MaxNumber(self, maxNumber: int = 1000):
        assert isinstance(maxNumber, int)
        self.__MaxNumber = maxNumber

    @CreateTime.setter
    def CreateTime(self, Time: float = 0.0):
        assert isinstance(Time, float)
        if Time:
            self.__CreateTime = Time

    def SetChange(self):
        self.__RevisionTime = time.time()
        return copy.deepcopy(self.__RevisionTime)


class MusicSheet(object):
    Json = "Json"
    SQLite3 = "SQLite3"
    AllMode = [Json, SQLite3]

    def __init__(self) -> None:
        self.__Information = SheetInfo()
        self.__MusicList = []

    @property
    def Information(self):
        return self.__Information

    def Append(self, Music: MusicItem):
        assert isinstance(Music, MusicItem)
        for OneMusic in self.__MusicList:
            OneMusic: MusicItem
            if OneMusic.FileId == Music.FileId:
                break
        else:
            self.__MusicList.append(Music)
        return None

    def Clear(self) -> bool:
        self.__MusicList.clear()
        return True

    @property
    def AllItem(self):
        for Item in self.__MusicList:
            yield Item

    def __len__(self):
        return len(self.__MusicList)

    def __add__(self, other):
        other: MusicSheet
        NewListObject = MusicSheet()
        for i in self.Information.Creator:
            NewListObject.Information.AddCreator(i)
        for i in other.Information.Creator:
            NewListObject.Information.AddCreator(i)
        for i in self.__MusicList:
            NewListObject.Append(i)
        for i in other.AllItem:
            NewListObject.Append(i)
        NewListObject.Information.MaxNumber = len(NewListObject)
        if self.Information.CreateTime >= other.Information.CreateTime:
            NewListObject.Information.CreateTime = other.Information.CreateTime
        else:
            NewListObject.Information.CreateTime = self.Information.CreateTime
        NewListObject.Information.SetChange()
        return NewListObject

    def Save(self, Mode: str = "Json", Path: str = "./"):
        assert Mode in self.AllMode
        assert isinstance(Path, str)
        Path = Path.replace("\\", "/").rstrip("/")
        SheetManager = Manager(Path)
        if Mode == self.Json:
            SheetManager.JsonSave(self)
        else:
            SheetManager.JsonSave(self)

    def Load(self, Mode: str = "Json", Path: str = "./"):
        assert isinstance(Mode, str)
        assert Mode in self.AllMode
        assert isinstance(Path, str)
        Path = Path.replace("\\", "/").rstrip("/")
        SheetManager = Manager(Path)
        if Mode == self.Json:
            SheetManager.JsonLoad(self)
