#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @FileName  :AuthorManager.py
# @Time      :2021/6/5 11:49
# @Author    :Amundsen Severus Rubeus Bjaaland


import warnings
import copy

import requests
from bs4 import BeautifulSoup as Bs

import KuGou
from KuGou.Requirement import Header


class SingerItem(object):
    __SUPPORTED = KuGou.SUPPORTED.ALL
    KUGOU = KuGou.SUPPORTED.KuGou
    WANGYIYUN = KuGou.SUPPORTED.WangYiYun

    def __init__(self, Name: str = "", Id: str = "", Platform: str = KuGou.SUPPORTED.KuGou):
        assert isinstance(Name, str)
        assert isinstance(Id, str)
        assert Platform in self.__SUPPORTED
        self.__Name = Name
        self.__Id = Id
        self.__Description = ""
        self.__PictureSources = []
        self.__Pictures = []
        self.__Platform = Platform

    def LoadInformation(self):
        self.__Pictures: list
        self.__Pictures.clear()
        if self.__Platform == self.KUGOU:
            self.__LoadInfoFromKuGou()
        elif self.__Platform == self.WANGYIYUN:
            self.__LoadInfoFromWangYiYun()
        else:
            warnings.warn(f"该歌手({self.__Name})来源网站目前不被支持。")
            return None
        self.__LoadPicture()
        return None

    def __LoadPicture(self):
        for OnePictureSource in self.__PictureSources:
            OneHeader = Header.GetHeader()
            try:
                OneResponse = requests.get(OnePictureSource, headers=OneHeader)
                assert OneResponse.status_code == 200
            except Exception:
                warnings.warn(f"加载歌手({self.__Name})写真失败。")
                continue
            else:
                self.__Pictures.append(OneResponse.content)

    def __LoadInfoFromKuGou(self):
        OneHeader = Header.GetHeader(Referrer=Header.REFERRER_KUGOU_SONGERINFO)
        OneUrl = "https://www.kugou.com/singer/" + self.__Id + ".html"
        try:
            OneResponse = requests.get(OneUrl, headers=OneHeader)
            assert OneResponse.status_code == 200
        except Exception:
            warnings.warn(f"加载歌手{self.__Name}简介失败。")
        else:
            Html = Bs(OneResponse.text, "lxml")
            BufferGroup = Html.find("div", attrs={"class": "intro"})
            self.__Description = BufferGroup.find("p").text
            self.__Name = BufferGroup.find("strong").text
        finally:
            return None

    def __LoadInfoFromWangYiYun(self):
        try:
            OneHeader = Header.GetHeader(Header.REFERRER_WANGYIYUN_MAIN)
            OneUrl = "https://music.163.com/artist/desc"
            OneResponse = requests.get(OneUrl, params={"id": self.__Id}, headers=OneHeader)
            Html = Bs(OneResponse.text, "lxml")
            self.__Description = Html.find("div", attrs={"class": "n-artdesc"}).text
            OneUrl = "https://music.163.com/artist"
            OneResponse = requests.get(OneUrl, params={"id": self.__Id}, headers=OneHeader)
            Html = Bs(OneResponse.text, "lxml")
            self.__Name = Html.find("h2", attrs={"id": "artist-name"}).text
            ImageSource = Html.find("div", attrs={"class": "n-artist f-cb"}).find("img").get("src")
            self.__PictureSources.append(ImageSource)
        except Exception:
            warnings.warn(f"加载歌手{self.__Name}简介或写真失败。")
        finally:
            return None

    def GetPicturesByList(self):
        return copy.deepcopy(self.__Pictures)

    def GetPicturesOneByOne(self):
        for i in self.__Pictures:
            yield i

    def GetFirstPicture(self):
        if len(self.__Pictures) > 0:
            return self.__Pictures[0]
        return b""

    def AppendPictureSource(self, PictureSource: str = ""):
        self.__PictureSources.append(PictureSource)
        return None

    @property
    def Name(self):
        return self.__Name

    @Name.setter
    def Name(self, Name: str = ""):
        assert isinstance(Name, str)
        self.__Name = Name

    @property
    def Id(self):
        return self.__Id

    @Id.setter
    def Id(self, Id: str = ""):
        assert isinstance(Id, str) or isinstance(Id, int)
        self.__Id = str(Id)

    @property
    def Platform(self):
        return self.__Platform

    @Platform.setter
    def Platform(self, Platform: str = KuGou.SUPPORTED.KuGou):
        assert Platform in self.__SUPPORTED
        self.__Platform = Platform

    @property
    def Description(self):
        return self.__Description


class SingerList(object):
    def __init__(self):
        self.__MainList = []
        self.__Names = ""

    def Append(self, PlatForm: str = KuGou.SUPPORTED.KuGou, Id: str = "", Name: str = "",
               PictureSources: tuple = tuple(), LoadFlag: bool = False):
        OneSinger = SingerItem()
        OneSinger.Id = Id
        OneSinger.Name = Name
        for OnePictureSource in PictureSources:
            OneSinger.AppendPictureSource(OnePictureSource)
        OneSinger.Platform = PlatForm
        if LoadFlag:
            OneSinger.LoadInformation()
        self.__MainList.append(OneSinger)
        return None

    def ReLoadInformation(self):
        for OneSinger in self.__MainList:
            OneSinger.LoadInformation()

    def GetSingerByName(self, Name: str = ""):
        for OneSinger in self.__MainList:
            if OneSinger.Name == Name:
                return OneSinger
        else:
            return SingerItem()

    def GetSingerById(self, Id: str = ""):
        for OneSinger in self.__MainList:
            if OneSinger.Id == Id:
                return OneSinger
        else:
            return SingerItem()

    def GetFirstSinger(self) -> SingerItem:
        if len(self.__MainList) > 0:
            return self.__MainList[0]
        else:
            return SingerItem()

    def GetSingersByList(self):
        return copy.deepcopy(self.__MainList)

    def GetSingersOneByOne(self):
        for OneSinger in self.__MainList:
            yield OneSinger

    def GetFreshNames(self):
        Buffer = ""
        for OneSinger in self.__MainList:
            Buffer = Buffer + OneSinger.Name + "、"
        return Buffer.rstrip("、")

    def SetNames(self, Name: str = ""):
        self.__Names = Name
        return None

    def GetSetNames(self):
        return self.__Names

    def GetFirstPicture(self):
        if len(self.__MainList) > 0:
            Picture: SingerItem = self.__MainList[0]
            return Picture.GetFirstPicture()
        else:
            return b""

    def GetFirstDescription(self):
        if len(self.__MainList) > 0:
            FirstSinger: SingerItem = self.__MainList[0]
            return FirstSinger.Description
        else:
            return ""
