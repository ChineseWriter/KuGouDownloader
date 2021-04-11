# coding = UTF-8


import warnings
import time
import re
import os

import js2py
import requests
import json
import eyed3

import KuGou


class MusicList(object):
    """从酷狗获取要查询的歌曲的结果列表"""

    def __init__(self, MusicName: str) -> None:
        """初始化该类：

        检查参数正确性，创建时间戳，初始化签名和数据容器，初始化JS命名空间(初始化命名空间并添加签名创建函数)。

        ::Usage:
            >>> var = MusicList("匆匆那年 王菲")

        :param MusicName: 要下载的歌曲名，必须为str类型。
        """
        # 检查传入的参数是否为str类型
        assert isinstance(MusicName, str)
        # 创建时间戳，为Python标准返回时间戳的一百倍再取整
        self.__TimeStamp = int(time.time() * 1000)
        self.__MusicName = MusicName  # 绑定歌曲名
        self.__Signature = ""  # 初始化签名容器
        self.__GetData = {}  # 初始化数据容器
        # 初始化JavaScript命名空间
        self.__JSNameSpace = js2py.EvalJs()
        # 添加JavaScript编写的签名构造函数
        self.__JSNameSpace.execute(KuGou.Requirement.GetSignFunction)

    def SetMusicName(self, MusicName: str) -> str:
        """设置或重置歌曲名：

        检查参数正确性，改变实例属性__MusicName到传入的参数值。

        ::Usage:
            >>>MusicList.SetMusicName("匆匆那年 王菲")

        :param MusicName: 要下载的歌曲名，必须为str类型。
        :return: 传入的歌曲名，为str类型。
        """
        # 检查传入的参数是否为str类型
        assert isinstance(MusicName, str)
        # 设置类属性__MusicName为传入的参数值
        self.__MusicName = MusicName
        return self.__MusicName

    def __SetTimeStamp(self) -> int:
        """设置时间戳：

        获取时间戳并将类属性__TimeStamp设置为改时间戳。

        :return: 获取的时间戳，为int类型。
        """
        # 创建时间戳，为Python标准返回时间戳的一百倍再取整
        self.__TimeStamp = int(time.time() * 1000)
        return self.__TimeStamp

    def __CreateMusicSignature(self) -> str:
        """创建签名：

        使用第三方库Js2Py运行酷狗的签名构造函数将数据转换为签名。

        :return: 创建的签名值，为str类型。
        """
        # 将要被转换的数据
        DataDict = [
            KuGou.Requirement.Key,
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
            KuGou.Requirement.Key,
        ]
        # 在JS命名空间中初始化该数据
        MusicSign = "o=" + str(DataDict)
        self.__JSNameSpace.execute(MusicSign)
        # 触发执行构造函数
        self.__JSNameSpace.execute(KuGou.Requirement.GetSign)
        # 获取执行后的签名
        MusicSign = self.__JSNameSpace.signature
        # 设置类属性__Signature为创建的签名
        self.__Signature = MusicSign
        # 返回签名
        return MusicSign

    def __CreateParams(self) -> dict:
        """创建网络请求必需的参数：

        :return: 创建的参数，为dict类型。
        """
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

    def __GetResponse(self) -> list:
        """从酷狗上获取查询结果：

        从酷狗获取数据，按照UTF-8编码解码，提取可被Json模块解析的内容，检查状态码是否正确，提取查询结果列表，清洗数据。

        :return: 清洗过的结果，为dict类型。
        """
        Response = requests.get(
            'https://complexsearch.kugou.com/v2/search/song?',
            headers=KuGou.Headers[0], params=self.__GetData
        )  # 获取数据
        String_1 = Response.content.decode('UTF-8')  # 按UTF-8编码解码
        String_2 = String_1[String_1.find('(') + 1:-2]  # 获取可被Json模块解析的内容
        Data = json.loads(String_2)  # 用Json模块解析
        if Data["status"] != 1:  # 检查状态码是否正确
            raise Exception("酷狗官网的返回状态码有误(不为1)。")  # 抛出错误
        # 提取需要的部分，即包含查询结果的列表
        GotMusicList = Data["data"]["lists"]
        if len(GotMusicList) == 0:  # 检查列表是否为空
            raise Exception("酷狗官网的返回结果数量为0个。")
        return MusicList.CleanData(GotMusicList)  # 清洗数据并返回

    @classmethod
    def CleanData(cls, Data: list) -> list:
        """清洗从酷狗官网获取的数据：

        提取歌名(FileName)、文件的哈希值(FileHash)、专辑ID(AlbumID)，并打上KuGou标识(From:KuGou)后的结果(为dict类型)，
        作为列表的一个元素，返回每个歌曲操作后的结果。

        ::Usage:
            >>>MusicList.CleanData({})

        :param Data: 获取的数据
        :return: 每个歌曲的结果，为list类型。
        """
        Buffer = []  # 初始化临时存储列表
        for OneSongInfo in Data:  # 遍历每个歌曲及其数据
            Buffer.append(
                {
                    "AlbumID": OneSongInfo["AlbumID"],  # 获取专辑ID
                    "FileHash": OneSongInfo["FileHash"],  # 获取文件哈希值
                    "FileName": OneSongInfo["SongName"].replace("<em>", "").replace("</em>", "").replace("/",
                                                                                                         "-").replace(
                        "\\", "-"),  # 获取歌曲名
                    "From": "KuGou"  # 打上KuGou标识
                }
            )
        return Buffer

    def GetMusicList(self) -> list:
        """获取查询结果：

        设置该次运行时间戳，创建签名，创建负载数据，获取结果列表。

        ::Usage:
            >>>var1 = MusicList("匆匆那年 王菲")
            >>>var2 = var1.GetMusicList()

        :return: 查询结果，为list类型。
        """
        self.__SetTimeStamp()  # 设置时间戳
        self.__CreateMusicSignature()  # 创建签名
        self.__CreateParams()  # 创建请求负载数据
        return self.__GetResponse()  # 获取返回数据


class MusicInfo(object):
    """获取歌曲相关数据。"""
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
        OneMusicInfo = {"MusicName": Data["audio_name"], "HaveAlbum": Data["have_album"]}
        if Data["have_album"] == 1:
            OneMusicInfo["MusicAlbum"] = Data["album_name"]
        else:
            OneMusicInfo["MusicAlbum"] = None
        if Data["have_mv"] == 1:
            OneMusicInfo["MusicVideo_id"] = Data["video_id"]
        OneMusicInfo["MusicPictureSource"] = Data["img"]
        OneMusicInfo["MusicAuthorName"] = Data["author_name"]
        OneMusicInfo["MusicLyrics"] = Data["lyrics"]
        OneMusicInfo["MusicSource"] = [Data.get("play_url"), Data.get("play_backup_url")]
        try:
            OneMusicInfo["MusicObject"] = requests.get(
                OneMusicInfo["MusicSource"][0], headers=KuGou.Headers[0]
            ).content
        except Exception:
            try:
                OneMusicInfo["MusicObject"] = requests.get(
                    OneMusicInfo["MusicSource"][1], headers=KuGou.Headers[0]
                ).content
            except Exception:
                OneMusicInfo["MusicObject"] = b""
        try:
            OneMusicInfo["MusicAuthorPictureSource"] = Data["authors"][0]["avatar"]
            OneMusicInfo["MusicAuthorPicture"] = requests.get(
                OneMusicInfo["MusicAuthorPictureSource"], headers=KuGou.Headers[0]
            ).content
        except KeyError:
            OneMusicInfo["MusicAuthorPicture"] = b""
            OneMusicInfo["MusicAuthorPictureSource"] = ""
        except requests.exceptions.MissingSchema:
            OneMusicInfo["MusicAuthorPicture"] = b""
        OneMusicInfo["MusicPicture"] = requests.get(
            OneMusicInfo["MusicPictureSource"], headers=KuGou.Headers[0]
        ).content
        Buffer = []
        for ii in str(OneMusicInfo["MusicLyrics"]).split("\r\n"):
            if re.match(r"(\[\d\d:\d\d\.\d\d\])(.*?)(##Finish)", ii + "##Finish"):
                Buffer.append(ii)
        MusicLyrics = ""
        for ii in Buffer:
            MusicLyrics = MusicLyrics + ii + "\r\n"
        MusicLyrics.rstrip("\r\n")
        String = re.match("(.*?)( - )(.*?)(-)", OneMusicInfo["MusicName"] + "-")
        if String:
            OneMusicInfo["MusicName"] = String.group(3).replace("/", "-").replace("\\", "-")
        return OneMusicInfo

    def GetMusicInfo(self) -> dict:
        self.__SetTimeStamp()
        self.__CreateParams()
        return MusicInfo.CleanData(self.__GetResponse())


class Music(object):
    def __init__(self, MusicInformation: dict, Path: str = "./") -> None:
        assert isinstance(MusicInformation, dict)
        assert isinstance(Path, str)
        assert os.path.exists(Path)
        self.__MusicInfo = MusicInformation
        self.__Path = Path if Path[-1] == ("/" or "\\") else Path + "/"

    def SetPath(self, Path: str = "./") -> str:
        assert os.path.exists(Path)
        assert isinstance(Path, str)
        self.__Path = Path
        return self.__Path

    def SaveMusic(self, LrcFile=False, ForceReplace=False) -> None:
        FilePath = self.__Path + self.__MusicInfo["MusicName"] + ".mp3"
        LrcFilePath = self.__Path + self.__MusicInfo["MusicName"] + ".lrc"
        if not self.__MusicInfo["MusicObject"]:
            warnings.warn("The music cannot be downloaded !")
            return None
        if os.path.exists(FilePath):
            if ForceReplace:
                with open(FilePath, "wb") as File:
                    File.write(self.__MusicInfo["MusicObject"])
        else:
            with open(FilePath, "wb") as File:
                File.write(self.__MusicInfo["MusicObject"])
        OneMusicObject = eyed3.load(FilePath)
        if OneMusicObject.info.time_secs <= 65:
            warnings.warn("The music you downloaded is too short !")
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
        if self.__MusicInfo["MusicAuthorPicture"]:
            OneMusicObject.tag.images.set(
                7, self.__MusicInfo["MusicAuthorPicture"],
                "image/jpeg", "Desc",
                self.__MusicInfo["MusicAuthorPictureSource"]
            )
        OneMusicObject.tag.lyrics.set(self.__MusicInfo["MusicLyrics"])
        if LrcFile:
            with open(LrcFilePath, "w", encoding="UTF-8") as File:
                File.write(self.__MusicInfo["MusicLyrics"])
        if self.__MusicInfo["HaveAlbum"] == 1:
            OneMusicObject.tag.album = self.__MusicInfo["MusicAlbum"]
        OneMusicObject.tag.save(version=(2, 3, 0))
