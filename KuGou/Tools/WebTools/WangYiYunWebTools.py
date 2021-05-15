# coding = UTF-8


import json

import requests
from bs4 import BeautifulSoup as Bs

from KuGou.Requirement import AESKey

import KuGou


class MusicList(object):
    SearchUrl = "https://music.163.com/weapi/cloudsearch/get/web?csrf_token="
    __Headers = {
        'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                      "(KHTML, like Gecko) Chrome/89.0.4389.114 Safari/537.36 Edg/89.0.774.68",
        'Referer': 'https://music.163.com/'
    }

    def __init__(self) -> None:
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
            Author = ""
            for i in OneMusic["ar"]:
                Author = Author + i["name"] + "、"
            OneMusicInfo.Author.Name = Author.rstrip("、")
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
        return self.__CleanedData


class MusicInfo(object):
    SongDetailUrl = "https://music.163.com/song"
    AlbumUrl = "https://music.163.com/album"
    LyricUrl = "https://music.163.com/weapi/song/lyric?csrf_token="
    MusicSourceUrl = "https://music.163.com/weapi/song/enhance/player/url?csrf_token="
    AuthorUrl = "https://music.163.com/artist"
    __Headers = {
        'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                      "(KHTML, like Gecko) Chrome/89.0.4389.114 Safari/537.36 Edg/89.0.774.68",
        'Referer': 'https://music.163.com/'
    }

    def __init__(self, Id: int = 0) -> None:
        assert isinstance(Id, int)
        self.__Id = Id
        self.__Music = KuGou.Music()
        self.__Music.From = KuGou.Music.From_WangYiYun
        self.__Music.FileId = Id
        self.KeyCreator = AESKey()

    def GetBasicInfo(self):
        Response = requests.get(self.SongDetailUrl, params={"id": self.__Id}, headers=self.__Headers)
        Html = Bs(Response.text, "lxml")
        DetailsDiv = Html.find("div", attrs={"class": "cnt"})
        MusicName = DetailsDiv.find("em", attrs={"class": "f-ff2"}).text
        if not MusicName:
            MusicName = DetailsDiv.find("em", attrs={"class": "f-ff2"}).get_text()
            if not MusicName:
                raise Exception()
        self.__Music.Name = MusicName
        AlbumAndAuthor = DetailsDiv.find_all("a", attrs={"class": "s-fc7"})
        AuthorInfo: Bs = AlbumAndAuthor[0]
        AlbumInfo: Bs = AlbumAndAuthor[1]
        AuthorName = AuthorInfo.text
        if not AuthorName:
            AuthorName = AuthorInfo.get_text()
            if not AuthorName:
                raise Exception()
        self.__Music.Author.Name = AuthorName
        AuthorId = AuthorInfo.get("href") or ""
        if AuthorId:
            AuthorId = AuthorId.split("=")[1]
            if AuthorId.isdigit():
                self.__Music.Author.Id = int(AuthorId)
        AlbumName = AlbumInfo.text
        if not AlbumName:
            AlbumName = AlbumInfo.get_text()
        self.__Music.Album = AlbumName
        AlbumId = AlbumInfo.get("href") or ""
        if AlbumId:
            AlbumId = AlbumId.split("=")[1]
            if AlbumId.isdigit():
                self.__Music.AlbumID = AlbumId
        Response = requests.get(self.AlbumUrl, params={"id": self.__Music.AlbumID}, headers=self.__Headers)
        self.__Music.PictureSource = Bs(Response.text, "lxml").find("img", attrs={"class": "j-img"})["data-src"]
        Response = requests.get(self.AuthorUrl, params={"id": self.__Music.Author.Id}, headers=self.__Headers)
        self.__Music.Author.PictureSource = Bs(Response.text, "lxml").find("meta", attrs={"property": "og:image"})[
            "content"]
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

    def GetMusicInfo(self):
        self.GetBasicInfo()
        self.__GetLyrics(self.__Music, self.__Music.FileId)
        self.__GetMusicSource(self.__Music, self.__Music.FileId)
        self.__Music.ReloadInfo()
        return self.__Music
