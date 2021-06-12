# coding = UTF-8
"""提供音乐文件检查功能。"""

# 文件资源管理需要
import os
# 类中防止错误（主要为误修改）
import copy
# MP3文件信息提取
import warnings

import eyed3


class Check(object):
    """音乐检查类"""

    def __init__(self, Path: str = "./Music") -> None:
        """该类的初始化

        初始化该类，将传入的参数设置为类的工作目录，同时检查该工作目录下的所有MP3文件，分别找出可能为VIP的歌曲和过短歌曲。

        :param Path: 该类的工作目录，为str类型。
        """
        # 必要类型检查
        assert isinstance(Path, str)
        assert os.path.exists(Path)
        # 将"\"替换为"/"防止意外错误
        self.__Path = Path.rstrip("\\").rstrip("/")
        # 分别查找VIP歌曲和过短歌曲
        self.__VIPMusic = self.__CheckVIP()
        self.__TooShortMusic = self.__CheckTooShort()
        self.__LrcWithoutMusic = self.__CheckLrcWithoutMusic()

    @property
    def Path(self):
        """获取类的工作目录

        :return: 该类的工作目录，为str类型。
        """
        return self.__Path

    @Path.setter
    def Path(self, Path: str = "./Music"):
        """设置类的工作目录

        将传入的参数设置为类的工作目录，同时检查该工作目录下的所有MP3文件，分别找出可能为VIP的歌曲和过短歌曲。

        :param Path: 类的工作目录，为str类型。
        """
        assert isinstance(Path, str)
        assert os.path.exists(Path)
        self.__Path = Path.rstrip("\\").rstrip("/")

    @property
    def VIPMusic(self):
        """获取所有的VIP歌曲名。

        获取所有的VIP歌曲名，不含工作路径。

        :return: 返回查找的所有VIP歌曲名。
        """
        return copy.deepcopy(self.__VIPMusic)

    @property
    def TooShortMusic(self):
        """获取所有的过短歌曲名。

        获取所有的过短歌曲名，不含工作路径。

        :return: 返回查找的所有过短歌曲。
        """
        return copy.deepcopy(self.__TooShortMusic)

    @property
    def LrcWithoutMusic(self):
        return copy.deepcopy(self.__LrcWithoutMusic)

    def __CheckVIP(self):
        Buffer = []
        for OneMusicName in os.listdir(self.__Path):
            if os.path.splitext(OneMusicName)[1] == ".mp3":
                OneMusicPath = self.__Path + "/" + OneMusicName
                try:
                    LoadedMusic = eyed3.load(OneMusicPath)
                except Exception:
                    warnings.warn(f"加载歌曲({OneMusicName})失败。")
                    continue
                if 59.5 <= LoadedMusic.info.time_secs <= 60.5:
                    Buffer.append(OneMusicName)
        return Buffer

    def __CheckTooShort(self):
        Buffer = []
        for OneMusicName in os.listdir(self.__Path):
            if os.path.splitext(OneMusicName)[1] == ".mp3":
                OneMusicPath = self.__Path + "/" + OneMusicName
                try:
                    LoadedMusic = eyed3.load(OneMusicPath)
                except Exception:
                    warnings.warn(f"加载歌曲({OneMusicName})失败。")
                    continue
                if LoadedMusic.info.time_secs <= 59.5:
                    Buffer.append(OneMusicName)
        return Buffer

    def __CheckLrcWithoutMusic(self):
        Buffer = []
        for i in os.listdir(self.__Path):
            if os.path.splitext(i)[1] == ".lrc":
                MusicFilePath = self.__Path + "/" + os.path.splitext(i)[0] + ".mp3"
                if not os.path.exists(MusicFilePath):
                    Buffer.append(i)
        return Buffer

    def DeleteVIPMusic(self, LrcFile: bool = True, DebugFlag: bool = False) -> None:
        for i in self.__VIPMusic:
            self.__DeleteItem(i, LrcFile, DebugFlag)
        return None

    def DeleteTooShortMusic(self, LrcFile: bool = True, DebugFlag: bool = False) -> None:
        for i in self.__TooShortMusic:
            self.__DeleteItem(i, LrcFile, DebugFlag)
        return None

    def DeleteLrcWithoutMusic(self, DebugFlag: bool = False):
        for i in self.__LrcWithoutMusic:
            if DebugFlag:
                print(f"Remove {i}")
            try:
                os.remove(self.__Path + "/" + i)
            except Exception:
                pass
        return None

    def __DeleteItem(self, Item, LrcFile: bool = True, DebugFlag: bool = False):
        Item = os.path.splitext(Item)[0]
        if DebugFlag:
            print(f"Remove : {Item}")
        try:
            os.remove(self.__Path + "/" + Item + ".mp3")
        except FileNotFoundError:
            pass
        if LrcFile:
            try:
                os.remove(self.__Path + "/" + Item + ".lrc")
            except FileNotFoundError:
                pass
