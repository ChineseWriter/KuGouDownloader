#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @FileName  :MusicItem.py
# @Time      :2021/6/27 11:28
# @Author    :Amundsen Severus Rubeus Bjaaland


# 导入所需库
# # 导入所需标准库
import copy
import logging
import traceback
import re
import os
# # 导入所需第三方库
from eyed3.core import AudioFile
import eyed3
import requests
# # 导入自己编写的模块
from ..AuthorManager import SingerList
from KuGou.Requirement import Header
import KuGou


class MusicItem(object):
    """Music对象，包含一首歌曲的基本信息和保存函数、信息重载函数"""
    # 所有受支持网站组成的列表
    __Supported = KuGou.SUPPORTED.ALL
    # 酷狗网站代号
    From_KuGou = KuGou.SUPPORTED.KuGou
    # 网易云网站代号
    From_WangYiYun = KuGou.SUPPORTED.WangYiYun
    # QQ网站代号
    From_QQ = KuGou.SUPPORTED.QQ
    # 喜马拉雅网站代号
    From_Himalaya = KuGou.SUPPORTED.Himalaya

    # 该类的日志记录器
    Logger = logging.getLogger(__name__ + ".MusicItem")

    def __init__(self, Name: str = "", From: str = "KuGou", MusicSource: str = "",
                 MusicObject: bytes = b"", FileId: str = "", MusicId: str = "", Mv: str = "", MvId: str = "",
                 PictureSource: str = "https://www.kugou.com/yy/static/images/play/default.jpg", Picture: bytes = b"",
                 Lyrics: str = "[00:00.00]纯音乐，请欣赏。", Album: str = "",
                 AlbumID: str = "") -> None:
        """初始化该类

        :param Name: 歌曲名称，为str类型
        :param From: 歌曲来源网站，为str类型
        :param MusicSource: 歌曲本身源URL，为str类型
        :param MusicObject: 歌曲本身，为bytes类型
        :param FileId: 歌曲在所属网站的唯一标识，为str类型
        :param MusicId: 歌曲在QQ音乐网站的第二标识，为str类型
        :param Mv: 歌曲相关MV，为bytes类型
        :param MvId: 歌曲相关MV在所属网站的唯一标识，为str类型
        :param PictureSource: 歌曲封面的源URL，为str类型
        :param Picture: 歌曲封面，为bytes类型
        :param Lyrics: 歌曲的歌词，为str类型
        :param Album: 歌曲的所属专辑名称，为str类型
        :param AlbumID: 歌曲所属专辑在所属网站上的唯一标识，为str类型
        :raise AssertError: 有参数的类型有误
        :return: 无返回值
        """
        # 对传入参数进行类型检查
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
        # 记录歌曲相关信息
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
        """将该类转换为str类型

        :return: 歌曲名称
        """
        return self.Name

    def __repr__(self):
        """该类的调试用字符串

        :return: 带有歌曲名称的调试用字符串
        """
        return "<MusicItem Object; Music Name: " + self.Name + ">"

    @property
    def Name(self) -> str:
        """获取歌曲名称"""
        return self.__Name

    @Name.setter
    def Name(self, Name: str = ""):
        """设置歌曲名称"""
        assert isinstance(Name, str)
        self.__Name = Name.replace("/", "").replace("\\", "")

    @property
    def From(self) -> str:
        """获取歌曲来源网站"""
        return self.__From

    @From.setter
    def From(self, From: str = "KuGou"):
        """设置歌曲来源网站"""
        assert isinstance(From, str)
        assert From in self.__Supported
        self.__From = From

    @property
    def MusicSource(self) -> str:
        """获取歌曲来源URL"""
        return self.__MusicSource

    @MusicSource.setter
    def MusicSource(self, MusicSource: str = ""):
        """设置歌曲来源URL"""
        assert isinstance(MusicSource, str)
        self.__MusicSource = MusicSource

    @property
    def MusicObject(self) -> bytes:
        """获取歌曲本身（比特对象）"""
        return self.__MusicObject

    @MusicObject.setter
    def MusicObject(self, MusicObject: bytes = b""):
        """设置歌曲本身（比特对象）"""
        assert isinstance(MusicObject, bytes)
        self.__MusicObject = MusicObject

    @property
    def FileId(self) -> str:
        """获取歌曲主编号"""
        return self.__FileId

    @FileId.setter
    def FileId(self, FileId: str = ""):
        """设置歌曲主编号"""
        if isinstance(FileId, int):
            FileId = str(FileId)
        assert isinstance(FileId, str)
        self.__FileId = FileId

    @property
    def Author(self) -> SingerList:
        """获取歌曲演唱者相关信息"""
        return self.__Author

    @property
    def PictureSource(self) -> str:
        """获取歌曲专辑封面来源URL"""
        return self.__PictureSource

    @PictureSource.setter
    def PictureSource(self, PictureSource: str = "https://www.kugou.com/yy/static/images/play/default.jpg"):
        """设置歌曲封面来源URL"""
        assert isinstance(PictureSource, str)
        self.__PictureSource = PictureSource

    @property
    def Picture(self) -> bytes:
        """获取歌曲封面本身（比特对象）"""
        return copy.deepcopy(self.__Picture)

    @Picture.setter
    def Picture(self, Picture: bytes = b""):
        """设置歌曲封面本身（比特对象）"""
        assert isinstance(Picture, bytes)
        self.__Picture = Picture

    def __LoadLyrics(self, Lyrics: str = "") -> None:
        """对歌曲的歌词按LRC文件格式进行清洗

        :param Lyrics: 歌曲的LRC文件，为str类型
        :return: 无返回值
        """
        # 检查传入的Lyric参数是否为空
        if not Lyrics:
            # 设置默认的Lyric并警告
            self.__Lyrics = "[00:00.00]纯音乐，请欣赏。"
            self.Logger.warning("您给出的歌词为空。")
            return None
        # 初始化放置歌词文件的列表，每个元素为一行歌词，str类型
        Buffer = []
        # 规范化歌词文件
        Lyrics = Lyrics.replace("\r", "").replace("\n\n", "\n")
        # 清洗歌词文件
        for Item in Lyrics.split("\n"):
            TestItem = Item + "##Finish"
            if re.match(r"(\[\d\d:\d\d\.\d\d])(.*?)(##Finish)", TestItem):
                Buffer.append(Item)
            elif re.match(r"(\[\d\d:\d\d\.\d\d\d])(.*?)(##Finish)", TestItem):
                Buffer.append(Item)
        # 将歌词列表转换为一个字符串
        MusicLyrics = ""
        for Item in Buffer:
            MusicLyrics = MusicLyrics + Item + "\r\n"
        self.__Lyrics = MusicLyrics.rstrip("\r\n")
        return None

    @property
    def Lyrics(self) -> str:
        """获取歌曲歌词"""
        return copy.deepcopy(self.__Lyrics)

    @Lyrics.setter
    def Lyrics(self, Lyrics: str = "[00:00.00]纯音乐，请欣赏。"):
        """设置歌曲歌词"""
        assert isinstance(Lyrics, str)
        self.__LoadLyrics(Lyrics)

    @property
    def Album(self) -> str:
        """获取歌词所属专辑"""
        return self.__Album

    @Album.setter
    def Album(self, MusicAlbum: str = ""):
        """设置歌曲所属专辑"""
        assert isinstance(MusicAlbum, str)
        self.__Album = MusicAlbum

    @property
    def AlbumID(self) -> str:
        """获取歌词所属专辑的编号"""
        return self.__AlbumID

    @AlbumID.setter
    def AlbumID(self, AlbumID: str = ""):
        """设置歌词所属专辑的编号"""
        assert isinstance(AlbumID, str)
        self.__AlbumID = AlbumID

    @property
    def Mv(self):
        """获取歌曲MV"""
        return self.__Mv

    @Mv.setter
    def Mv(self, NewMv: str = ""):
        """设置歌曲MV"""
        assert isinstance(NewMv, str)
        self.__Mv = NewMv

    @property
    def MvId(self):
        """获取歌曲MV的编号"""
        return self.__MvId

    @MvId.setter
    def MvId(self, NewMvId: str = ""):
        """设置歌曲MV的编号"""
        assert isinstance(NewMvId, str)
        self.__MvId = NewMvId

    @property
    def MusicId(self):
        """获取歌曲的副编号"""
        return self.__MusicId

    @MusicId.setter
    def MusicId(self, NewMusicId: str = ""):
        """设置歌曲的副编号"""
        assert isinstance(NewMusicId, str)
        self.__MusicId = NewMusicId

    def ReloadInfo(self) -> None:
        """重载歌曲的部分相关信息"""
        OneHeader = Header.GetHeader()
        # 重载歌曲本身（比特对象）
        try:
            # 从QQ上重载歌曲本身（比特对象）
            if self.From == self.From_QQ:
                from pydub import AudioSegment  # 使用该库将QQ音乐的M4A文件转为MP3文件
                # 从QQ音乐上下载文件并保存到本地
                with open("./Temp.m4a", "wb") as File:
                    File.write(requests.get(self.__MusicSource, headers=OneHeader).content)
                # 转换下载的文件并保存到本地
                AudioSegment.from_file("./Temp.m4a").export("./Temp.mp3")
                # 读取转换后的文件
                with open("./Temp.mp3", "rb") as File:
                    self.__MusicObject = File.read()
                # 删除本地多余的文件
                os.remove("./Temp.m4a")
                os.remove("./Temp.mp3")
            # 从其它网站上重载歌曲本身
            else:
                self.__MusicObject = requests.get(self.__MusicSource, headers=OneHeader).content
        except Exception:
            self.Logger.warning(f"歌曲“{self.__Name}”载入歌曲数据失败。")
        # 重载歌曲演唱者相关信息
        try:
            self.__Author.ReLoadInformation()
        except Exception:
            self.Logger.warning(f"歌曲“{self.__Name}”载入歌手图片失败。")
        # 重载歌曲的专辑封面
        try:
            self.__Picture = requests.get(self.__PictureSource, headers=OneHeader).content
        except Exception:
            self.Logger.warning(f"歌曲“{self.__Name}”载入音乐封面失败。")
        return None

    def Save(self, Path: str = "./", LrcFile: bool = False, ForceReplace: bool = False) -> bool:
        """保存歌曲到本地

        :param Path: 保存到本地的路径，该路径必须存在，为str类型
        :param LrcFile: 是否保存LRC文件到保存该歌曲的目录下，为bool类型
        :param ForceReplace: 是否强制替换已存在的歌曲文件，为bool类型
        :return: 保存是否成功，为bool类型
        """
        # 将路径字符串中的“\”转换为“/”
        Path = Path.replace("\\", "/").rstrip("/") + "/"
        # 生成歌曲文件的保存路径（含歌曲文件）
        MusicFilePath = Path + self.__Author.FreshNames + " - " + self.__Name + ".mp3"
        # 生成歌词文件的保存路径（含歌词文件）
        LrcFilePath = Path + self.__Author.FreshNames + " - " + self.__Name + ".lrc"
        # 保存歌词文件
        if LrcFile:
            MusicSaveTools.SaveLyric(LrcFilePath, self.__Lyrics)
        # 保存歌曲文件
        MusicSaveTools.SaveMusic(MusicFilePath, self.__MusicObject, ForceReplace)
        # 载入歌曲文件并准备添加 IDv3 Tag
        try:
            Music = MusicSaveTools.LoadMusic(MusicFilePath)
        except Exception as AllError:
            self.Logger.warning("添加歌曲信息失败。")
            traceback.print_exc()
            return False
        # 在歌曲文件上设置歌曲名称
        Music.tag.title = self.__Name
        # 在歌曲文件上设置演唱者名称
        Music.tag.artist = self.__Author.FreshNames
        # 在歌曲文件上设置专辑封面
        Music.tag.images.set(3, self.__Picture, "image/jpeg", "Cover (front)", self.__PictureSource)
        Music.tag.images.set(4, self.__Picture, "image/jpeg", "Cover (back)", self.__PictureSource)
        # 在歌曲文件上设置演唱者图片
        if self.__Author.GetFirstPicture():
            # 获取第一个演唱者的图片
            Picture = self.__Author.GetFirstPicture()
            # 获取演唱者的描述
            try:
                Description = self.__Author.GetFirstDescription().encode().decode("UTF-16")
            except UnicodeDecodeError:
                Description = "Singer"
            # 设置演唱者图片
            Music.tag.images.set(7, Picture, "image/jpeg", Description)
        # 在歌曲文件上设置歌词
        Music.tag.lyrics.set(self.__Lyrics)
        # 在歌曲文件上设置专辑名称
        if self.__Album:
            Music.tag.album = self.__Album
        # 保存歌曲文件
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
        Music.initTag()
        return Music
