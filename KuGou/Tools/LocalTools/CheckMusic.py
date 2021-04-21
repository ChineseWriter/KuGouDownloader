# coding = UTF-8


import os


class Check(object):
    def __init__(self, Path: str = "./") -> None:
        self.__Path = Path

    @property
    def Path(self):
        return self.__Path

    @Path.setter
    def Path(self, Path: str = "./"):
        assert isinstance(Path, str)
        assert os.path.exists(Path)
        self.__Path = Path
