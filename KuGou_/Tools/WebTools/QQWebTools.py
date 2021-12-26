#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @FileName  :QQWebTools.py
# @Time      :2021/7/10 18:38
# @Author    :Amundsen Severus Rubeus Bjaaland
import base64
import copy
import json
import time

import requests
from pydub import AudioSegment
from bs4 import BeautifulSoup as BS

import KuGou
from KuGou.Requirement import Header


class MusicList(object):
    QQSearchUrl = "https://c.y.qq.com/soso/fcgi-bin/client_search_cp"

    def __init__(self, MusicName: str):
        assert isinstance(MusicName, str)
        self.__MusicName = MusicName
        self.__Params = dict()

    def SetMusicName(self, MusicName: str) -> str:
        # 检查传入的参数是否为str类型
        assert isinstance(MusicName, str)
        # 设置类属性__MusicName为传入的参数值
        self.__MusicName = MusicName
        return self.__MusicName

    def __GetParams(self):
        self.__Params = {
            "ct": 24,
            "qqmusic_ver": 1298,
            "new_json": 1,
            "remoteplace": "Text.yqq.song",
            "searchid": 63229658163010696,
            "t": 0,
            "aggr": 1,
            "cr": 1,
            "catZhida": 1,
            "lossless": 0,
            "flag_qc": 0,
            "p": 1,
            "n": 10,
            "w": self.__MusicName,
            "g_tk": 5381,
            "loginUin": 0,
            "hostUin": 0,
            "format": "json",
            "inCharset": "utf8",
            "outCharset": "utf-8",
            "notice": 0,
            "platform": "yqq.json",
            "needNewCode": 0
        }
        return copy.deepcopy(self.__Params)

    def __GetResponse(self):
        OneHeader = Header.GetHeader(Referrer=Header.REFERRER_QQ_SEARCH, Origin=Header.ORIGIN_QQ)
        OneResponse = requests.get(self.QQSearchUrl, params=self.__Params, headers=OneHeader)
        String_1 = OneResponse.content.decode('UTF-8')
        Data = json.loads(String_1)
        if Data["code"] != 0:
            raise Exception("QQ音乐官网的返回状态码有误(不为0)。")
        GotMusicList = Data["data"]["song"]["list"]
        if len(GotMusicList) == 0:
            raise Exception("QQ音乐官网的返回结果数量为0个。")
        return self.__CleanData(GotMusicList)

    def __CleanData(self, Data: list) -> list:
        Buffer = []
        for OneMusicInfo in Data:
            OneMusic = KuGou.Music()
            OneMusic.From = KuGou.Music.From_QQ
            OneMusic.AlbumID = OneMusicInfo["album"]["mid"]
            OneMusic.FileId = OneMusicInfo["mid"]
            OneMusic.MusicId = str(OneMusicInfo["id"])
            OneMusic.Name = OneMusicInfo["name"]
            for OneSingerInfo in OneMusicInfo["singer"]:
                OneMusic.Author.Append(KuGou.SUPPORTED.QQ, OneSingerInfo["mid"], OneSingerInfo["name"])
            OneMusic.Album = OneMusicInfo["album"]["name"]
            OneMusic.AlbumID = OneMusicInfo["album"]["mid"]
            OneMusic.MvId = OneMusicInfo["mv"]["vid"]
            Buffer.append(OneMusic)
        return Buffer

    def GetMusicList(self) -> list:
        self.__GetParams()
        return self.__GetResponse()


class MusicInfo(object):
    QQMusicUrl = "https://u.y.qq.com/cgi-bin/musicu.fcg"
    QQSongDetailUrl = "https://y.qq.com/n/ryqq/songDetail/"
    QQLyricUrl = "https://c.y.qq.com/lyric/fcgi-bin/fcg_query_lyric_new.fcg"

    def __init__(self, OneMusic):
        self.__Music: KuGou.Music = OneMusic
        self.__Param_1 = dict()
        self.__Param_2 = dict()
        self.__MusicURLs = []

    def __GetParams_1(self):
        self.__Param_1 = {
            "-": "getplaysongvkey5559460738919986",
            "g_tk": 5381,
            "loginUin": 0,
            "hostUin": 0,
            "format": "json",
            "inCharset": "utf8",
            "outCharset": "utf-8",
            "notice": 0,
            "platform": "yqq.json",
            "needNewCode": 0,
            "data": json.dumps(
                {
                    "req": {
                        "module": "CDN.SrfCdnDispatchServer",
                        "method": "GetCdnDispatch",
                        "param": {"guid": "1825194589", "calltype": 0, "userip": ""}
                    },
                    self.__Music.FileId: {
                        "module": "vkey.GetVkeyServer",
                        "method": "CgiGetVkey",
                        "param": {
                            "guid": "1825194589",
                            "songmid": [self.__Music.FileId],
                            "songtype": [0],
                            "uin": "0",
                            "loginflag": 1,
                            "platform": "20"
                        }
                    },
                    "comm": {"uin": 0, "format": "json", "ct": 24, "cv": 0}
                }
            )
        }
        return copy.deepcopy(self.__Param_1)

    def __GetParams_2(self):
        self.__Param_2 = {
            "_": 1626343861190,
            # "_": str(time.time()).replace(".", "")[:13],
            "cv": 4747474,
            "ct": 24,
            "format": "json",
            "inCharset": "utf-8",
            "outCharset": "utf-8",
            "notice": 0,
            "platform": "yqq.json",
            "needNewCode": 1,
            "uin": 0,
            "g_tk_new_20200303": 5381,
            "g_tk": 5381,
            "loginUin": 0,
            "songmid": self.__Music.FileId,
            "musicid": self.__Music.MusicId
        }
        return copy.deepcopy(self.__Param_2)

    def __GetResponse(self):
        OneHeader = Header.GetHeader()
        OneResponse = requests.get(self.QQMusicUrl, params=self.__Param_1, headers=OneHeader)
        String_1 = OneResponse.content.decode('UTF-8')
        Data = json.loads(String_1)
        if Data["code"] != 0:
            raise Exception("QQ音乐官网的返回状态码有误(不为0)。")
        self.__MusicURLs = Data["req"]["data"]['freeflowsip']
        Data = Data[self.__Music.FileId]
        if Data["code"] != 0:
            raise Exception("QQ音乐官网的返回状态码有误(不为0)。")
        Data = Data["data"]
        return self.__CleanData(Data)

    def __CleanData(self, Data):
        self.__Music.MusicSource = self.__MusicURLs[0] + Data["midurlinfo"][0]["purl"]
        OneHeader = Header.GetHeader()
        OneResponse = requests.get(self.QQSongDetailUrl + self.__Music.FileId, headers=OneHeader)
        Html = BS(OneResponse.text, "lxml")
        Image = "https:" + Html.find("img", attrs={"class": "data__photo"})["src"]
        self.__Music.PictureSource = Image
        self.__Music.Name = Html.find("h1", attrs={"class": "data__name_txt"})["title"]
        SingerList = Html.find("div", attrs={"class": "data__singer"}).find_all("a")
        for OneSingerInfo in SingerList:
            SingerName = OneSingerInfo["title"]
            SingerId = OneSingerInfo["href"].split("/")[-1]
            SingerPictureSource = requests.get("https://y.qq.com/" + OneSingerInfo["href"], headers=Header.GetHeader())
            PictureSource = BS(SingerPictureSource.text, "lxml").find("img", attrs={"class": "data__photo"})["src"]
            self.__Music.Author.Append(self.__Music.From_QQ, SingerId, SingerName, (PictureSource,), True)
        self.__Music.Album = Html.find("ul", attrs={"class": "data__info"}) \
            .find("li", attrs={"class": "data_info__item_song"}).find("a")["title"]
        OneHeader = Header.GetHeader(Origin=Header.ORIGIN_QQ, Referrer=Header.REFERRER_QQ_MAIN)
        OneResponse = requests.get(self.QQLyricUrl, params=self.__Param_2, headers=OneHeader)
        Lyrics = json.loads(OneResponse.content.decode("UTF-8"))
        # Lyrics = json.loads(OneResponse.content.decode("UTF-8")[18:-1])
        if Lyrics["code"] == 0:
            self.__Music.Lyrics = base64.b64decode(Lyrics["lyric"]).decode()
        self.__Music.ReloadInfo()
        return None

    def GetMusicInfo(self):
        self.__GetParams_1()
        self.__GetParams_2()
        self.__GetResponse()
        return self.__Music
