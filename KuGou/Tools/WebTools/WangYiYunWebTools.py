# coding = UTF-8


import json

import requests

from KuGou.Requirement import AESKey

import KuGou


class MusicList(object):
    SearchUrl = "https://music.163.com/weapi/cloudsearch/get/web?csrf_token="
    LyricUrl = "https://music.163.com/weapi/song/lyric?csrf_token="
    MusicSourceUrl = "https://music.163.com/weapi/song/enhance/player/url?csrf_token="
    AuthorUrl = "https://music.163.com/artist"

    def __init__(self) -> None:
        self.__Headers = {
            'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                          "(KHTML, like Gecko) Chrome/89.0.4389.114 Safari/537.36 Edg/89.0.774.68",
            'Referer': 'http://music.163.com/'
        }
        self.KeyCreator = AESKey()
        self.__GetParams = None
        self.__GetData = []
        self.__MusicName = ""
        self.__CleanedData = []

    def __CreateParams(self) -> dict:
        Data = {
            "hlpretag": "",
            "hlposttag": "",
            "s": self.__MusicName,
            "type": "1",
            "offset": "0",
            "total": "true",
            "limit": "30",
            "csrf_token": ""
        }
        Data = json.dumps(Data)
        self.__GetParams = self.KeyCreator.GetParams(Data)
        return self.__GetParams

    def __GetResponse(self) -> None:
        self.__CreateParams()
        OneResponse = requests.post(self.SearchUrl, data=self.__GetParams, headers=self.__Headers)
        try:
            JsonData = OneResponse.json()
            if JsonData["code"] != 200:
                raise Exception()
            ResultList = JsonData["result"]["songs"]
        except Exception:
            return None
        self.__GetData = ResultList
        return self.__GetData

    def __CleanData(self):
        Buffer = []
        for OneMusic in self.__GetData:
            OneMusicInfo = KuGou.Music()
            OneMusicInfo.From = KuGou.Music.From_WangYiYun
            OneMusicInfo.Name = OneMusic["name"]
            OneMusicInfo.FileId = OneMusic["id"]
            if OneMusic.get("al"):
                OneMusicInfo.AlbumID = str(OneMusic["al"]["id"])
                OneMusicInfo.PictureSource = OneMusic["al"]["picUrl"]
            else:
                OneMusicInfo.AlbumID = ""
            OneMusicInfo.AuthorName = OneMusic["ar"][0]["name"]
            OneMusicInfo.AuthorId = OneMusic["ar"][0]["id"]
            self.__GetLyrics(OneMusicInfo, str(OneMusicInfo.FileId))
            self.__GetMusicSource(OneMusicInfo, OneMusicInfo.FileId)
            Buffer.append(OneMusicInfo)
        self.__CleanedData = Buffer
        return None

    def __GetLyrics(self, OneMusic, MusicId):
        OneMusic: KuGou.Music
        try:
            Params = {"id": str(MusicId), "lv": -1, "tv": -1, "csrf_token": ""}
            Params = json.dumps(Params)
            Params = self.KeyCreator.GetParams(Params)
            Response = requests.post(self.LyricUrl, data=Params, headers=self.__Headers)
            JsonData = Response.json()
            if JsonData["code"] != 200:
                raise Exception()
            if JsonData.get("nolyric"):
                OneMusic.Lyrics = "[00:00.00]纯音乐，请欣赏。"
            else:
                OneMusic.Lyrics = JsonData['lrc']['lyric']
        except Exception:
            OneMusic.Lyrics = "[00:00.00]纯音乐，请欣赏。"
        finally:
            return None

    def __GetMusicSource(self, OneMusic, MusicId):
        OneMusic: KuGou.Music
        try:
            Params = {"ids": [int(MusicId)], "br": 128000, "csrf_token": ""}
            Params = json.dumps(Params)
            Params = self.KeyCreator.GetParams(Params)
            Response = requests.post(self.MusicSourceUrl, data=Params, headers=self.__Headers)
            JsonData = Response.json()
            OneMusic.MusicSource = JsonData['data'][0]['url']
        except Exception:
            pass
        finally:
            return None

    def __SetMusicName(self, MusicName):
        if not isinstance(MusicName, str):
            raise
        self.__MusicName = MusicName
        return None

    def GetMusicList(self, MusicName: str):
        self.__SetMusicName(MusicName)
        self.__GetResponse()
        self.__CleanData()
        return self.__CleanedData
