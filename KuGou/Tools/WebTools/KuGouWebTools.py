# coding = UTF-8


import time
import re

import js2py
import requests
import json

import KuGou
from KuGou.Requirement import Header


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
        OneHeader = Header.GetHeader(Referrer=Header.REFERRER_KUGOU_SEARCH)
        Response = requests.get(
            'https://complexsearch.kugou.com/v2/search/song?',
            headers=OneHeader, params=self.__GetData
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
            >>>MusicList.CleanData(list())

        :param Data: 获取的数据
        :return: 每个歌曲的结果，为list类型。
        """
        Buffer = []  # 初始化临时存储列表
        for OneSongInfo in Data:  # 遍历每个歌曲及其数据
            OneMusic = KuGou.Music()
            OneMusic.AlbumID = OneSongInfo["AlbumID"]  # 获取歌曲所属专辑的ID
            OneMusic.FileId = OneSongInfo["FileHash"]  # 获取歌曲的哈希值
            Name = OneSongInfo["SongName"].replace("<em>", "").replace("</em>", "")  # 处理歌曲名中的强调HTML标签
            OneMusic.Name = Name
            for Id, SingerName in zip(OneSongInfo["SingerId"], OneSongInfo["SingerName"].split("、")):
                SingerName = SingerName.replace("<em>", "").replace("</em>", "")
                OneMusic.Author.Append(KuGou.SUPPORTED.KuGou, Id, SingerName)
            Buffer.append(OneMusic)  # 添加歌曲至列表中
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
    """从酷狗官网获取歌曲相关数据。"""

    def __init__(self, MusicItem) -> None:
        # 设置基本时间戳
        self.__TimeStamp = int(time.time() * 1000)
        # 设置存放网络请求负载数据的容器
        self.__Params = {}
        MusicItem: KuGou.Music
        self.__Music = MusicItem

    def __SetTimeStamp(self) -> int:
        """设置网络请求的时间戳

        :return: 返回设置的时间戳
        """
        self.__TimeStamp = int(time.time() * 1000)
        return self.__TimeStamp

    def __CreateParams(self) -> dict:
        """创建网络请求必要的负载

        :return: 返回创建的负载数据
        """
        self.__Params = {
            "r": "play/getdata",
            "callback": "jQuery19100824172432511463_1612781797757",
            "hash": self.__Music.FileId,
            "dfid": "073Nfk3nSl6t0sst5p3fjWxH",
            "mid": "578a45450e07d9022528599a86a22d26",
            "platid": 4,
            "album_id": self.__Music.AlbumID,
            "_": str(self.__TimeStamp)
        }
        return self.__Params

    def __GetResponse(self) -> dict:
        OneHeader = Header.GetHeader(Referrer=Header.REFERRER_KUGOU_SEARCH)
        Response = requests.get(
            "https://wwwapi.kugou.com/yy/index.php",
            headers=OneHeader, params=self.__Params
        )
        String_1 = Response.content.decode('utf-8')
        String_2 = String_1[String_1.find('(') + 1:-2]
        Data = json.loads(String_2)
        if Data["status"] != 1:
            raise
        Data = Data["data"]
        return Data

    def CleanData(self, Data):
        if Data["have_album"] == 1:
            self.__Music.Album = Data["album_name"]
        self.__Music.PictureSource = Data["img"]
        for OneSinger in Data["authors"]:
            self.__Music.Author.Append(
                KuGou.SUPPORTED.KuGou,
                OneSinger["author_id"],
                OneSinger["author_name"],
                (OneSinger["avatar"],),
                True
            )
        self.__Music.Lyrics = Data["lyrics"]
        if Data.get("play_url") is not None:
            self.__Music.MusicSource = Data.get("play_url")
        else:
            if Data.get("play_backup_url") is not None:
                self.__Music.MusicSource = Data.get("play_backup_url")
            else:
                return KuGou.Music()
        self.__Music.ReloadInfo()
        String = re.match("(.*?)( - )(.*?)(-)", Data["audio_name"] + "-")
        if String:
            self.__Music.Name = String.group(3).replace("/", "-").replace("\\", "-")
        else:
            self.__Music.Name = Data["audio_name"]
        return None

    def GetMusicInfo(self):
        self.__SetTimeStamp()
        self.__CreateParams()
        self.CleanData(self.__GetResponse())
        return self.__Music
