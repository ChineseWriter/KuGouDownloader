# coding = UTF-8


import copy
import json
import warnings
import re
import os
import time

import eyed3
import requests

import KuGou

VERSION = "1.0.0"


class MusicItem(object):
    __Supported = KuGou.Supported
    From_KuGou = "KuGou"

    def __init__(self, Name: str = "", From: str = "KuGou", AuthorName: str = "", MusicSource: str = "",
                 MusicObject: bytes = b"",
                 PictureSource: str = "https://www.kugou.com/yy/static/images/play/default.jpg", Picture: bytes = b"",
                 AuthorPictureSource: str = "https://www.kugou.com/yy/static/images/play/default.jpg",
                 AuthorPicture: bytes = b"", Lyrics: str = "[00:00.00]纯音乐，请欣赏。", Album: str = "", FileHash: str = "",
                 AlbumID: str = "") -> None:
        assert isinstance(Name, str)
        assert isinstance(From, str)
        assert From in self.__Supported
        assert isinstance(MusicSource, str)
        assert isinstance(MusicObject, bytes)
        assert isinstance(AuthorName, str)
        assert isinstance(PictureSource, str)
        assert isinstance(Picture, bytes)
        assert isinstance(AuthorPictureSource, str)
        assert isinstance(AuthorPicture, bytes)
        assert isinstance(Lyrics, str)
        assert isinstance(Album, str)
        assert isinstance(FileHash, str)
        assert isinstance(AlbumID, str)
        self.__Name = Name
        self.__From = From
        self.__MusicSource = MusicSource
        self.__MusicObject = MusicObject
        self.__AuthorName = AuthorName
        self.__PictureSource = PictureSource
        self.__Picture = Picture
        self.__AuthorPictureSource = AuthorPictureSource
        self.__AuthorPicture = AuthorPicture
        self.__Lyrics = ""
        self.__LoadLyrics(Lyrics)
        self.__Album = Album
        self.__FileHash = FileHash
        self.__AlbumID = AlbumID

    @property
    def Name(self) -> str:
        return self.__Name

    @Name.setter
    def Name(self, Name: str = ""):
        assert isinstance(Name, str)
        self.__Name = Name

    @property
    def From(self) -> str:
        return self.__From

    @From.setter
    def From(self, From: str = "KuGou"):
        assert isinstance(From, str)
        assert From in self.__Supported
        self.__From = From

    @property
    def MusicSource(self) -> str:
        return self.__MusicSource

    @MusicSource.setter
    def MusicSource(self, MusicSource: str = ""):
        assert isinstance(MusicSource, str)
        self.__MusicSource = MusicSource

    @property
    def MusicObject(self) -> bytes:
        return self.__MusicObject

    @MusicObject.setter
    def MusicObject(self, MusicObject: bytes = b""):
        assert isinstance(MusicObject, bytes)
        self.__MusicObject = MusicObject

    @property
    def AuthorName(self) -> str:
        return self.__AuthorName

    @AuthorName.setter
    def AuthorName(self, AuthorName: str = ""):
        assert isinstance(AuthorName, str)
        self.__AuthorName = AuthorName

    @property
    def PictureSource(self) -> str:
        return self.__PictureSource

    @PictureSource.setter
    def PictureSource(self, PictureSource: str = "https://www.kugou.com/yy/static/images/play/default.jpg"):
        assert isinstance(PictureSource, str)
        self.__PictureSource = PictureSource

    @property
    def Picture(self) -> bytes:
        return copy.deepcopy(self.__Picture)

    @Picture.setter
    def Picture(self, Picture: bytes = b""):
        assert isinstance(Picture, bytes)
        self.__Picture = Picture

    @property
    def AuthorPictureSource(self) -> str:
        return self.__AuthorPictureSource

    @AuthorPictureSource.setter
    def AuthorPictureSource(self, AuthorPictureSource: str = "https://www.kugou.com/yy/static/images/play/default.jpg"):
        assert isinstance(AuthorPictureSource, str)
        self.__AuthorPictureSource = AuthorPictureSource

    @property
    def AuthorPicture(self) -> bytes:
        return self.__AuthorPicture

    @AuthorPicture.setter
    def AuthorPicture(self, AuthorPicture: bytes = b""):
        assert isinstance(AuthorPicture, bytes)
        self.__AuthorPicture = AuthorPicture

    def __LoadLyrics(self, Lyrics: str = "") -> None:
        if not Lyrics:
            self.__Lyrics = ""
            warnings.warn("The lyrics you given is nothing .")
            return None
        Buffer = []
        for Item in Lyrics.split("\r\n"):
            if re.match(r"([\d\d:\d\d.\d\d])(.*?)(##Finish)", Item + "##Finish"):
                Buffer.append(Item)
        MusicLyrics = ""
        for Item in Buffer:
            MusicLyrics = MusicLyrics + Item + "\r\n"
        self.__Lyrics = MusicLyrics.rstrip("\r\n")
        return None

    @property
    def Lyrics(self) -> str:
        return copy.deepcopy(self.__Lyrics)

    @Lyrics.setter
    def Lyrics(self, Lyrics: str = ""):
        assert isinstance(Lyrics, str)
        self.__LoadLyrics(Lyrics)

    @property
    def Album(self) -> str:
        return self.__Album

    @Album.setter
    def Album(self, MusicAlbum: str = ""):
        assert isinstance(MusicAlbum, str)
        self.__Album = MusicAlbum

    @property
    def FileHash(self) -> str:
        return self.__FileHash

    @FileHash.setter
    def FileHash(self, FileHash: str = ""):
        assert isinstance(FileHash)
        self.__FileHash = FileHash

    @property
    def AlbumID(self) -> str:
        return copy.deepcopy(self.__AlbumID)

    @AlbumID.setter
    def AlbumID(self, AlbumID: str = ""):
        assert isinstance(AlbumID, str)
        self.__AlbumID = AlbumID

    def ReloadInfo(self) -> None:
        try:
            self.__MusicObject = requests.get(self.__MusicSource, headers=KuGou.Headers[1]).content
        except Exception:
            warnings.warn("Reload music object failed .")
        try:
            self.__AuthorPicture = requests.get(self.__AuthorPictureSource, headers=KuGou.Headers[1]).content
        except Exception:
            warnings.warn("Reload the picture of author failed .")
        try:
            self.__Picture = requests.get(self.__PictureSource, headers=KuGou.Headers[1]).content
        except Exception:
            warnings.warn("Reload the picture of the music failed .")
        return None

    def Save(self, Path: str = "./", LrcFile: bool = False, ForceReplace: bool = False) -> None:
        Path = Path.replace("\\", "/").rstrip("/") + "/"
        MusicFilePath = Path + self.__AuthorName + " - " + self.__Name + ".mp3"
        LrcFilePath = Path + self.__AuthorName + " - " + self.__Name + ".lrc"
        if LrcFile:
            with open(LrcFilePath, "w", encoding="UTF-8") as File:
                File.write(self.__Lyrics)
        if os.path.exists(MusicFilePath):
            if ForceReplace:
                if not self.__MusicObject:
                    warnings.warn("The music object is nothing .")
                    return None
                with open(MusicFilePath, "wb") as File:
                    File.write(self.__MusicObject)
            else:
                with open(MusicFilePath, "rb") as File:
                    self.__MusicObject = File.read()
        else:
            if not self.__MusicObject:
                warnings.warn("The music object is nothing .")
                return None
            with open(MusicFilePath, "wb") as File:
                File.write(self.__MusicObject)
        Music = eyed3.load(MusicFilePath)
        if Music.info.time_secs <= 60:
            warnings.warn("The music is too short !")
        if 59.6 <= Music.info.time_secs <= 60.4:
            warnings.warn("The music might be a VIP music !")
        Music.initTag()
        Music.tag.Title = self.__Name
        Music.tag.artist = self.__AuthorName
        Music.tag.images.set(3, self.__Picture, "image/jpeg", "Desc", self.__PictureSource)
        Music.tag.images.set(4, self.__Picture, "image/jpeg", "Desc", self.__PictureSource)
        if self.__AuthorPicture:
            Music.tag.images.set(7, self.__AuthorPicture, "image/jpeg", "Desc", self.__AuthorPictureSource)
        Music.tag.lyrics.set(self.__Lyrics)
        if self.__Album:
            Music.tag.album = self.__Album
        Music.tag.save(version=(2, 3, 0))
        return None


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
        if Music not in self.__MusicList:
            self.__MusicList.append(Music)
        return None

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
        for i in other.AllItem():
            NewListObject.Append(i)
        NewListObject.Information.MaxNumber = len(NewListObject)
        if self.Information.CreateTime >= other.Information.CreateTime:
            NewListObject.Information.CreateTime = other.Information.CreateTime
        else:
            NewListObject.Information.CreateTime = self.Information.CreateTime
        NewListObject.Information.SetChange()
        return NewListObject

    def Save(self, Mode: str = "Json", Path: str = "./"):
        assert isinstance(Mode, str)
        assert Mode in self.AllMode
        assert isinstance(Path, str)
        Path = Path.replace("\\", "/").rstrip("/")
        if Mode == self.Json:
            self.__JsonSave(Path)
        else:
            self.__JsonSave(Path)

    def __JsonSave(self, Path: str) -> None:
        Object = dict()
        Object["Info"] = {
            "SelfVersion": self.__Information.Version,
            "DownloaderVersion": self.__Information.DownloaderVersion,
            "MaxNumber": self.__Information.MaxNumber,
            "CreateTime": self.__Information.CreateTime,
            "RevisionTime": self.__Information.RevisionTime,
            "Creator": self.__Information.Creator
        }
        Buffer = []
        for i in self.__MusicList:
            i: MusicItem
            if i.From == MusicItem.From_KuGou:
                Buffer.append({"From": i.From, "FileHash": i.FileHash, "AlbumID": i.AlbumID, "MusicName": i.Name})
        Object["Musics"] = Buffer
        with open(Path, "w", encoding="UTF-8") as File:
            json.dump(Object, File)
        return None

    def Load(self, Mode: str = "Json", Path: str = "./"):
        assert isinstance(Mode, str)
        assert Mode in self.AllMode
        assert isinstance(Path, str)
        Path = Path.replace("\\", "/").rstrip("/")
        if Mode == self.Json:
            self.__JsonLoad(Path)

    def __JsonLoad(self, Path: str) -> None:
        if not os.path.exists(Path):
            Object = {
                "Info": {
                    "Creator": ["Machine", ],
                    "MaxNumber": 1000,
                    "SelfVersion": VERSION,
                    "DownloaderVersion": KuGou.Version,
                    "CreateTime": time.time(),
                    "RevisionTime": time.time()
                },
                "Musics": []
            }
            with open(Path, "w", encoding="UTF-8") as File:
                json.dump(Object, File)
        with open(Path, "r", encoding="UTF-8") as File:
            Object = json.load(File)
        Info = Object["Info"]
        MusicList = Object["Musics"]
        Info: dict
        self.__Information.MaxNumber = Info["MaxNumber"]
        self.__Information.CreateTime = Info["CreateTime"]
        self.__Information.SetChange()
        for OneMusic in Info["Creator"]:
            self.__Information.AddCreator(OneMusic)
        self.__MusicList.clear()
        for OneMusic in MusicList:
            if OneMusic["From"] == MusicItem.From_KuGou:
                OneMusic = MusicItem(Name=OneMusic["MusicName"], FileHash=OneMusic["FileHash"], From=OneMusic["From"],
                                     AlbumID=OneMusic["AlbumID"])
                self.__MusicList.append(OneMusic)
        return None
