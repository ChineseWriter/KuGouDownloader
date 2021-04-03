# coding = UTF-8


import os
import json
import copy
from pygame import mixer


class MusicSheet(object):
    def __init__(self, Path="./KuGouMusicList.json"):
        if os.path.exists(Path):
            if os.path.isfile(Path):
                self.__Musics = json.load(open(Path, "r", encoding="UTF-8"))
            else:
                raise
        else:
            with open(Path, "w", encoding="UTF-8") as File:
                File.write("[]")
            self.__Musics = []
        self.__Path = Path

    def Add(self, AlbumID, FileHash, FileName=""):
        self.__Musics: list
        assert isinstance(AlbumID, str)
        assert isinstance(FileHash, str)
        assert isinstance(FileName, str)
        OneMusic = {"FileName": FileName, "FileHash": FileHash, "AlbumID": AlbumID}
        if OneMusic not in self.__Musics:
            self.__Musics.append(OneMusic)
        if len(self.__Musics) >= 1500:
            pass
        return copy.deepcopy(OneMusic)

    def DropByAlbumID(self, AlbumID):
        assert isinstance(AlbumID, str)
        self.__Musics: list
        for OneMusic in self.__Musics:
            OneMusic: dict
            if OneMusic.get("AlbumID") == AlbumID:
                self.__Musics.remove(OneMusic)
        return None

    def DropByFileHash(self, FileHash):
        assert isinstance(FileHash, str)
        self.__Musics: list
        for OneMusic in self.__Musics:
            OneMusic: dict
            if OneMusic.get("FileHash") == FileHash:
                self.__Musics.remove(OneMusic)
        return None

    def DropByFileName(self, FileName):
        assert isinstance(FileName, str)
        self.__Musics: list
        for OneMusic in self.__Musics:
            OneMusic: dict
            if OneMusic.get("FileName") == FileName:
                self.__Musics.remove(OneMusic)
        return None

    def Save(self):
        json.dump(self.__Musics, open(self.__Path, "w", encoding="UTF-8"))
        return None

    def Musics(self):
        for OneMusic in self.__Musics:
            yield OneMusic

    def GetMusics(self):
        return copy.deepcopy(self.__Musics)


class Play(object):
    def __init__(self):
        mixer.init()
        self.__Path = "./"

    def load(self, Path):
        assert os.path.exists(Path)
        assert os.path.isfile(Path)
        self.__Path = Path
        mixer.music.load(Path)
        return Path

    def play(self, Times, StartAt=0):
        mixer.music.play(Times, StartAt)
        return None

    def stop(self):
        mixer.music.stop()
        return None
