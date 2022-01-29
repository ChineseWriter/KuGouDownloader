#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @FileName  :Objects.py
# @Time      :2021/12/25 18:45
# @Author    :Amundsen Severus Rubeus Bjaaland


import copy
import logging

import cv2
import numpy

from .Validators import String, Bytes, URL, SourceWebSite, List, Lyrics
from ..logo import LOGO


class AdditionalInformation(object):
    def __init__(self, **kwargs) -> None:
        for k, v in kwargs.items():
            setattr(self, k, v)


class InformationList(AdditionalInformation):
    self_objects: list = List()
    description: str = String()

    def __init__(self):
        super(InformationList, self).__init__()
        self.self_objects = []
        self.description = ""

    def clear(self):
        self.self_objects.clear()
        return None

    def __getitem__(self, item):
        return self.self_objects[item]

    def get_first(self):
        return self.self_objects[0]


class Media(object):
    """该类描述所有媒体"""
    # 对每个媒体的基本属性
    name = String()
    source_site = SourceWebSite()
    self_source = URL()
    self_object = Bytes()
    master_id = String()
    sub_id = String()
    __logger = logging.getLogger(__name__ + ".Media")

    def __init__(self, **kwargs) -> None:
        self.name = ""
        self.source_site = "KuGou"
        self.self_source = "https://www.kugou.com/"
        self.self_object = b""
        self.master_id = ""
        self.sub_id = ""
        for k, v in kwargs.items():
            setattr(self, k, v)

    def __len__(self):
        return len(self.self_object)


class Picture(Media):
    description: str = String()

    def __init__(self, **kwargs):
        super(Picture, self).__init__(**kwargs)
        if "self_source" not in kwargs:
            raise ValueError("Parameter 'self_source' is required.")
        if "self_object" in kwargs:
            self.__image: numpy.ndarray = cv2.imdecode(
                numpy.frombuffer(kwargs["self_object"], numpy.uint8), cv2.IMREAD_COLOR
            )
        else:
            self.self_object = LOGO
            self.__image: numpy.ndarray = cv2.imdecode(numpy.frombuffer(LOGO, numpy.uint8), cv2.IMREAD_COLOR)

    @property
    def shape(self):
        return self.__image.shape


class PictureList(InformationList):
    self_objects: list = List(Picture)

    def __init__(self):
        super(PictureList, self).__init__()
        self.self_objects = []

    def add(self, source: str, pic_object: bytes, desc: str = "") -> Picture:
        picture_object = Picture(self_source=source, self_object=pic_object, description=desc)
        self.self_objects.append(picture_object)
        return copy.deepcopy(picture_object)


class Person(AdditionalInformation):
    name = String()
    id = String()
    source_site = SourceWebSite()
    description = String()

    def __init__(self, **kwargs):
        super(Person, self).__init__(**kwargs)
        self.__Picture = PictureList()


class PeopleList(InformationList):
    self_objects: list = List(Person)

    def __init__(self):
        super(PeopleList, self).__init__()
        self.self_objects = []

    def add(self, person_id: str, name: str, source_site: str, desc: str = ""):
        for i in self.self_objects:
            if i.id == person_id:
                return copy.deepcopy(i)
        else:
            person_object = Person(id=person_id, name=name, source_site=source_site, description=desc)
            self.self_objects.append(person_object)
            return copy.deepcopy(person_object)

    @property
    def name_list(self):
        buffer = ""
        for i in self.self_objects:
            i: Person
            buffer = buffer + i.name + "、"
        return buffer.rstrip("、")


class Music(Media):
    """该类描述所有音乐种类或相关媒体类型"""
    mv_source = String()
    mv = Bytes()
    lyrics = Lyrics()
    album = String()

    def __init__(self, **kwargs):
        super(Music, self).__init__(**kwargs)
        self.mv_source = ""
        self.mv = b""
        self.lyrics = ""
        self.album = ""
        self.__poster_list = PictureList()
        self.__singer_list = PeopleList()

    @property
    def poster_list(self):
        """返回该歌曲的专辑封面列表"""
        return self.__poster_list

    @property
    def singer_list(self):
        """返回该歌曲的演唱者列表"""
        return self.__singer_list
