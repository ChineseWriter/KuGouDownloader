# coding = UTF-8


import json

import requests

from KuGou.Requirement import AESKey


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
            OneMusicInfo = {"Name": OneMusic["name"], "ID": OneMusic["id"]}
            if OneMusic.get("al"):
                OneMusicInfo["AlbumID"] = OneMusic["al"]["id"]
                OneMusicInfo["MusicPictureSource"] = OneMusic["al"]["picUrl"]
            else:
                OneMusicInfo["AlbumID"] = ""
            OneMusicInfo["MusicAuthorName"] = OneMusic["ar"][0]["name"]
            OneMusicInfo["MusicAuthorID"] = OneMusic["ar"][0][""]
            try:
                OneMusicInfo["MusicLyrics"] = requests.post(self.LyricUrl, data=self.KeyCreator.GetParams(
                    json.dumps({"id": OneMusicInfo["ID"], "lv": -1, "tv": -1, "csrf_token": ""})),
                                                            headers=self.__Headers).json()['lrc']['lyric']
            except Exception:
                OneMusicInfo["MusicLyrics"] = "[00:00.00]纯音乐，请欣赏。"
            try:
                OneMusicInfo["MusicSource"] = requests.post(self.MusicSourceUrl, data=self.KeyCreator.GetParams(
                    json.dumps({"ids": [OneMusicInfo["ID"]], "br": 128000, "csrf_token": ""})),
                                                            headers=self.__Headers).json()['data'][0]['url']
            except Exception as AllError:
                raise AllError
            Buffer.append(OneMusicInfo)
        self.__CleanedData = Buffer
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
        return None
