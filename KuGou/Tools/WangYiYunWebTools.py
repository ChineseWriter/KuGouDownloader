# coding = UTF-8


import json

import requests

from KuGou.Requirement import AESKey


class MusicList(object):
    SearchUrl = "https://music.163.com/weapi/cloudsearch/get/web?csrf_token="

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

    def __CreateParams(self, MusicName: str) -> dict:
        Data = {
            "hlpretag": "",
            "hlposttag": "",
            "s": MusicName,
            "type": "1",
            "offset": "0",
            "total": "true",
            "limit": "30",
            "csrf_token": ""
        }
        Data = json.dumps(Data)
        self.__GetParams = self.KeyCreator.GetParams(Data)
        return self.__GetParams

    def __GetResponse(self, MusicName: str) -> None:
        self.__CreateParams(MusicName)
        OneResponse = requests.post(self.SearchUrl, data=self.__GetParams)
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
        for OneMusic in self.__GetData:
            MusicName = OneMusic['name']
            MusicID = OneMusic['id']
            MusicSinger = OneMusic['ar'][0]
            MusicAlbum = OneMusic["al"][0]

    def SetMusicName(self, MusicName):
        if not isinstance(MusicName, str):
            raise
        self.__MusicName = MusicName
        return None

    def GetMusicList(self):
        pass
