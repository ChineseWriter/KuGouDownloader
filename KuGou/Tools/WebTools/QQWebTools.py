#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @FileName  :QQWebTools.py
# @Time      :2021/7/10 18:38
# @Author    :Amundsen Severus Rubeus Bjaaland


import copy
import json

import requests

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
            "remoteplace": "txt.yqq.song",
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
            raise Exception("QQ音乐官网的返回状态码有误(不为1)。")
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
            OneMusic.Name = OneMusicInfo["name"]
            for OneSingerInfo in OneMusicInfo["singer"]:
                OneMusic.Author.Append(KuGou.SUPPORTED.QQ, OneSingerInfo["mid"], OneSingerInfo["name"])
            Buffer.append(OneMusic)
        return Buffer

    def GetMusicList(self) -> list:
        self.__GetParams()
        return self.__GetResponse()
