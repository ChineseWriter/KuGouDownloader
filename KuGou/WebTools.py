# coding = UTF-8


import time
import re
import os

import js2py
import requests
import json
import eyed3

import KuGou


class MusicList(object):
    def __init__(self, MusicName: str) -> None:
        assert isinstance(MusicName, str)
        self.__TimeStamp = int(time.time() * 1000)
        self.__MusicName = MusicName
        self.__Signature = ""
        self.__GetData = {}
        self.__JSNameSpace = js2py.EvalJs()
        self.__JSNameSpace.execute(KuGou.JSRequirements.GetSignFunction)

    def SetMusicName(self, MusicName: str) -> str:
        assert isinstance(MusicName, str)
        self.__MusicName = MusicName
        return self.__MusicName

    def __SetTimeStamp(self) -> int:
        self.__TimeStamp = int(time.time() * 1000)
        return self.__TimeStamp

    def __CreateMusicSignature(self) -> str:
        DataDict = [
            KuGou.JavaScript.Key,
            "bitrate=0",
            "callback=callback123",
            f"clienttime={self.__TimeStamp}",
            "clientver=2000",
            "dfid=-",
            "inputtype=0",
            "iscorrection=1",
            "isfuzzy=0",
            f"keyword={self.__MusicName}",
            f"mid={self.__TimeStamp}",
            "page=1",
            "pagesize=30",
            "platform=WebFilter",
            "privilege_filter=0",
            "srcappid=2919",
            "tag=em",
            "userid=-1",
            f"uuid={self.__TimeStamp}",
            KuGou.JavaScript.Key,
        ]
        MusicSign = "o=" + str(DataDict)
        self.__JSNameSpace.execute(MusicSign)
        self.__JSNameSpace.execute(KuGou.JSRequirements.GetSign)
        MusicSign = self.__JSNameSpace.signature
        self.__Signature = MusicSign
        return MusicSign

    def __CreateParams(self) -> dict:
        self.__GetData = {
            'callback': 'callback123',
            'keyword': self.__MusicName,
            'page': "1",
            'pagesize': "30",
            'bitrate': '0',
            'isfuzzy': '0',
            'tag': 'em',
            'inputtype': '0',
            'platform': 'WebFilter',
            'userid': '-1',
            'clientver': '2000',
            'iscorrection': '1',
            'privilege_filter': '0',
            'srcappid': '2919',
            'clienttime': self.__TimeStamp,
            'mid': self.__TimeStamp,
            'uuid': self.__TimeStamp,
            'dfid': '-',
            'signature': self.__Signature,
        }
        return self.__GetData

    def __GetResponse(self) -> dict:
        Response = requests.get(
            'https://complexsearch.kugou.com/v2/search/song?',
            headers=KuGou.Headers[0], params=self.__GetData
        )
        String_1 = Response.content.decode('utf-8')
        String_2 = String_1[String_1.find('(') + 1:-2]
        Data = json.loads(String_2)
        if Data["status"] != 1:
            raise
        Data = Data["data"]
        GotMusicList = Data["lists"]
        if len(GotMusicList) == 0:
            raise
        return MusicList.CleanData(GotMusicList)

    @classmethod
    def CleanData(cls, Data: list):
        Buffer = []
        for OneSongInfo in Data:
            Buffer.append(
                {
                    "AlbumID": OneSongInfo["AlbumID"],
                    "FileHash": OneSongInfo["FileHash"],
                    "FileName": OneSongInfo["SongName"].replace("<em>", "").replace("</em>", "")
                }
            )
        return Buffer

    def GetMusicList(self):
        self.__SetTimeStamp()
        self.__CreateMusicSignature()
        self.__CreateParams()
        return self.__GetResponse()


class MusicInfo(object):
    def __init__(self, AlbumID: str, FileHash: str) -> None:
        assert isinstance(AlbumID, str)
        assert isinstance(FileHash, str)
        self.__TimeStamp = int(time.time() * 1000)
        self.__Params = {}
        self.__AlbumID = AlbumID
        self.__FileHash = FileHash

    def SetRequirements(self, AlbumID: str, FileHash: str) -> None:
        assert isinstance(AlbumID, str)
        assert isinstance(FileHash, str)
        self.__AlbumID = AlbumID
        self.__FileHash = FileHash
        return None

    def __SetTimeStamp(self) -> int:
        self.__TimeStamp = int(time.time() * 1000)
        return self.__TimeStamp

    def __CreateParams(self) -> dict:
        self.__Params = {
            "r": "play/getdata",
            "callback": "jQuery19100824172432511463_1612781797757",
            "hash": self.__FileHash,
            "dfid": "073Nfk3nSl6t0sst5p3fjWxH",
            "mid": "578a45450e07d9022528599a86a22d26",
            "platid": 4,
            "album_id": self.__AlbumID,
            "_": str(self.__TimeStamp)
        }
        return self.__Params

    def __GetResponse(self) -> dict:
        Response = requests.get(
            "https://wwwapi.kugou.com/yy/index.php",
            headers=KuGou.Headers[0], params=self.__Params
        )
        String_1 = Response.content.decode('utf-8')
        String_2 = String_1[String_1.find('(') + 1:-2]
        Data = json.loads(String_2)
        if Data["status"] != 1:
            raise
        Data = Data["data"]
        return Data

    @classmethod
    def CleanData(cls, Data) -> dict:
        OneMusicInfo = {"MusicName": Data["audio_name"]}
        OneMusicInfo["HaveAlbum"] = Data["have_album"]
        if Data["have_album"] == 1:
            OneMusicInfo["MusicAlbum"] = Data["album_name"]
        else:
            OneMusicInfo["MusicAlbum"] = None
        if Data["have_mv"] == 1:
            OneMusicInfo["MusicVideo_id"] = Data["video_id"]
        OneMusicInfo["MusicPictureSource"] = Data["img"]
        OneMusicInfo["MusicAuthorName"] = Data["author_name"]
        OneMusicInfo["MusicLyrics"] = Data["lyrics"]
        OneMusicInfo["MusicSource"] = [Data["play_url"], Data["play_backup_url"]]
        OneMusicInfo["MusicAuthorPictureSource"] = Data["authors"][0]["avatar"]
        OneMusicInfo["MusicPicture"] = requests.get(
            OneMusicInfo["MusicPictureSource"], headers=KuGou.Headers[0]
        ).content
        OneMusicInfo["MusicAuthorPicture"] = requests.get(
            OneMusicInfo["MusicAuthorPictureSource"], headers=KuGou.Headers[0]
        ).content
        OneMusicInfo["MusicObject"] = requests.get(
            OneMusicInfo["MusicSource"][0], headers=KuGou.Headers[0]
        ).content
        Buffer = []
        for ii in str(OneMusicInfo["MusicLyrics"]).split("\r\n"):
            if re.match(r"(\[\d\d:\d\d\.\d\d\])(.*?)", ii):
                Buffer.append(ii)
        MusicLyrics = ""
        for ii in Buffer:
            MusicLyrics = MusicLyrics + ii + "\r\n"
        MusicLyrics.rstrip("\r\n")
        String = re.match("(.*?)( - )(.*?)(-)", OneMusicInfo["MusicName"] + "-")
        if String:
            OneMusicInfo["MusicName"] = String.group(3)
        return OneMusicInfo

    def GetMusicInfo(self):
        self.__SetTimeStamp()
        self.__CreateParams()
        return MusicInfo.CleanData(self.__GetResponse())


class Music(object):
    def __init__(self, MusicInfo: dict, Path: str = "./") -> None:
        assert isinstance(MusicInfo, dict)
        assert isinstance(Path, str)
        assert os.path.exists(Path)
        self.__MusicInfo = MusicInfo
        self.__Path = Path

    def SetPath(self, Path: str = "./") -> str:
        assert os.path.exists(Path)
        assert isinstance(Path, str)
        self.__Path = Path
        return self.__Path

    def SaveMusic(self) -> None:
        FilePath = self.__Path + self.__MusicInfo["MusicName"] + ".mp3"
        with open(FilePath, "wb") as File:
            File.write(self.__MusicInfo["MusicObject"])
        OneMusicObject = eyed3.load(FilePath)
        OneMusicObject.initTag()
        OneMusicObject.tag.title = self.__MusicInfo["MusicName"]
        OneMusicObject.tag.artist = self.__MusicInfo["MusicAuthorName"]
        OneMusicObject.tag.images.set(
            3, self.__MusicInfo["MusicPicture"],
            "image/jpeg", "Desc",
            self.__MusicInfo["MusicPictureSource"]
        )
        OneMusicObject.tag.images.set(
            4, self.__MusicInfo["MusicPicture"],
            "image/jpeg", "Desc",
            self.__MusicInfo["MusicPictureSource"]
        )
        OneMusicObject.tag.images.set(
            7, self.__MusicInfo["MusicAuthorPicture"],
            "image/jpeg", "Desc",
            self.__MusicInfo["MusicAuthorPictureSource"]
        )
        OneMusicObject.tag.lyrics.set(self.__MusicInfo["MusicLyrics"])
        if self.__MusicInfo["HaveAlbum"] == 1:
            OneMusicObject.tag.album = self.__MusicInfo["MusicAlbum"]
        OneMusicObject.tag.save(version=(2, 3, 0))
