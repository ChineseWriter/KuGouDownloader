#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @FileName  :MusicItem.py
# @Time      :2021/6/27 11:28
# @Author    :Amundsen Severus Rubeus Bjaaland


import copy
import warnings
import re
import os

from eyed3.core import AudioFile
import eyed3
import requests

from KuGou.Tools.LocalTools.AuthorManager import SingerList
from KuGou.Requirement import Header
import KuGou


class MusicItem(object):
    __Supported = KuGou.SUPPORTED.ALL
    From_KuGou = KuGou.SUPPORTED.KuGou
    From_WangYiYun = KuGou.SUPPORTED.WangYiYun
    From_QQ = KuGou.SUPPORTED.QQ
    From_Himalaya = KuGou.SUPPORTED.Himalaya

    def __init__(self, Name: str = "", From: str = "KuGou", MusicSource: str = "",
                 MusicObject: bytes = b"", FileId: str = "", MusicId: str = "", Mv: str = "", MvId: str = "",
                 PictureSource: str = "https://www.kugou.com/yy/static/images/play/default.jpg", Picture: bytes = b"",
                 Lyrics: str = "[00:00.00]纯音乐，请欣赏。", Album: str = "",
                 AlbumID: str = "") -> None:
        assert isinstance(Name, str)
        assert isinstance(From, str)
        assert From in self.__Supported
        assert isinstance(MusicSource, str)
        assert isinstance(MusicObject, bytes)
        assert isinstance(FileId, str) or isinstance(FileId, int)
        assert isinstance(PictureSource, str)
        assert isinstance(Picture, bytes)
        assert isinstance(Lyrics, str)
        assert isinstance(Album, str)
        assert isinstance(AlbumID, str)
        assert isinstance(Mv, str)
        assert isinstance(MvId, str)
        assert isinstance(MusicId, str)
        self.__Author = SingerList()
        self.__Name = Name.replace("/", "").replace("\\", "")
        self.__From = From
        self.__MusicSource = MusicSource
        self.__MusicObject = MusicObject
        self.__FileId = str(FileId)
        self.__PictureSource = PictureSource
        self.__Picture = Picture
        self.__Lyrics = "[00:00.00]纯音乐，请欣赏。"
        self.__LoadLyrics(Lyrics)
        self.__Album = Album
        self.__AlbumID = AlbumID
        self.__Mv = Mv
        self.__MvId = MvId
        self.__MusicId = MusicId

    def __str__(self):
        return self.Name

    def __repr__(self):
        return "<MusicItem Object; Music Name: " + self.Name + ">"

    @property
    def Name(self) -> str:
        return self.__Name

    @Name.setter
    def Name(self, Name: str = ""):
        assert isinstance(Name, str)
        self.__Name = Name.replace("/", "").replace("\\", "")

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
    def FileId(self) -> str:
        return self.__FileId

    @FileId.setter
    def FileId(self, FileId: str = ""):
        if isinstance(FileId, int):
            FileId = str(FileId)
        assert isinstance(FileId, str)
        self.__FileId = FileId

    @property
    def Author(self) -> SingerList:
        return self.__Author

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

    def __LoadLyrics(self, Lyrics: str = "") -> None:
        if not Lyrics:
            self.__Lyrics = ""
            warnings.warn("The lyrics you given is nothing .")
            return None
        Buffer = []
        Lyrics = Lyrics.replace("\r", "").replace("\n\n", "\n")
        for Item in Lyrics.split("\n"):
            AppendFlag = False
            TestItem = Item + "##Finish"
            if re.match(r"(\[\d\d:\d\d\.\d\d])(.*?)(##Finish)", TestItem):
                AppendFlag = True
            elif re.match(r"(\[\d\d:\d\d\.\d\d\d])(.*?)(##Finish)", TestItem):
                AppendFlag = True
            if AppendFlag:
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
    def Lyrics(self, Lyrics: str = "[00:00.00]纯音乐，请欣赏。"):
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
    def AlbumID(self) -> str:
        return self.__AlbumID

    @AlbumID.setter
    def AlbumID(self, AlbumID: str = ""):
        assert isinstance(AlbumID, str)
        self.__AlbumID = AlbumID

    @property
    def Mv(self):
        return self.__Mv

    @Mv.setter
    def Mv(self, NewMv: str = ""):
        assert isinstance(NewMv, str)
        self.__Mv = NewMv

    @property
    def MvId(self):
        return self.__MvId

    @MvId.setter
    def MvId(self, NewMvId: str = ""):
        assert isinstance(NewMvId, str)
        self.__MvId = NewMvId

    @property
    def MusicId(self):
        return self.__MusicId

    @MusicId.setter
    def MusicId(self, NewMusicId: str = ""):
        assert isinstance(NewMusicId, str)
        self.__MusicId = NewMusicId

    def ReloadInfo(self) -> None:
        OneHeader = Header.GetHeader()
        try:
            if self.From == self.From_QQ:
                from pydub import AudioSegment
                with open("./Temp.m4a", "wb") as File:
                    File.write(requests.get(self.__MusicSource, headers=OneHeader).content)
                AudioSegment.from_file("./Temp.m4a").export("./Temp.mp3")
                with open("./Temp.mp3", "rb") as File:
                    self.__MusicObject = File.read()
                os.remove("./Temp.m4a")
                os.remove("./Temp.mp3")
            else:
                self.__MusicObject = requests.get(self.__MusicSource, headers=OneHeader).content
        except Exception:
            warnings.warn("载入歌曲数据失败。")
        try:
            self.__Author.ReLoadInformation()
        except Exception:
            warnings.warn("载入歌手图片失败。")
        try:
            self.__Picture = requests.get(self.__PictureSource, headers=OneHeader).content
        except Exception:
            warnings.warn("载入音乐封面失败。")
        return None

    def Save(self, Path: str = "./", LrcFile: bool = False, ForceReplace: bool = False) -> bool:
        Path = Path.replace("\\", "/").rstrip("/") + "/"
        MusicFilePath = Path + self.__Author.FreshNames + " - " + self.__Name + ".mp3"
        LrcFilePath = Path + self.__Author.FreshNames + " - " + self.__Name + ".lrc"
        if LrcFile:
            MusicSaveTools.SaveLyric(LrcFilePath, self.__Lyrics)
        MusicSaveTools.SaveMusic(MusicFilePath, self.__MusicObject, ForceReplace)
        try:
            Music = MusicSaveTools.LoadMusic(MusicFilePath)
        except Exception as AllError:
            warnings.warn("添加歌曲信息失败。")
            return False
        Music.tag.title = self.__Name
        Music.tag.artist = self.__Author.FreshNames
        Music.tag.images.set(3, self.__Picture, "image/jpeg", "Desc", self.__PictureSource)
        Music.tag.images.set(4, self.__Picture, "image/jpeg", "Desc", self.__PictureSource)
        if self.__Author.GetFirstPicture():
            Picture = self.__Author.GetFirstPicture()
            try:
                Description = self.__Author.GetFirstDescription().encode().decode("UTF-16")
            except UnicodeDecodeError:
                Description = "Desc"
            Music.tag.images.set(7, Picture, "image/jpeg", Description)
        Music.tag.lyrics.set(self.__Lyrics)
        if self.__Album:
            Music.tag.album = self.__Album
        Music.tag.save(version=(2, 3, 0))
        return True


class MusicSaveTools(object):
    @classmethod
    def SaveMusic(cls, Path: str, MusicObject: bytes, ForceReplace: bool = False) -> bool:
        if not MusicObject:
            warnings.warn("下载歌曲为空。")
            return False
        if os.path.exists(Path):
            if ForceReplace:
                with open(Path, "wb") as File:
                    File.write(MusicObject)
            return True
        with open(Path, "wb") as File:
            File.write(MusicObject)
        return True

    @classmethod
    def SaveLyric(cls, Path: str, LyricObject: str) -> bool:
        try:
            with open(Path, "w", encoding="UTF-8") as LyricFile:
                LyricFile.write(LyricObject)
        except Exception as AllError:
            warnings.warn(repr(AllError))
            return False
        else:
            return True

    @classmethod
    def LoadMusic(cls, Path: str) -> AudioFile:
        Music = eyed3.load(Path)
        if Music.info.time_secs <= 60:
            warnings.warn("这个歌曲太短了。(只有不到60秒)")
        if 59.6 <= Music.info.time_secs <= 60.4:
            warnings.warn("这个歌曲可能是一个VIP歌曲。(时长大概为1分钟)")
        return Music
