#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @FileName  :Objects.py
# @Time      :2021/12/25 18:45
# @Author    :Amundsen Severus Rubeus Bjaaland


import copy
import logging

from .Validators import String, Number, Bytes, URL, SourceWebSite, List


class AdditionalInformation(object):
    pass


class Picture(AdditionalInformation):
    self_source: str = URL()
    self_object: bytes = Bytes()
    description: str = String()

    def __init__(self, **kwargs):
        for k, v in kwargs:
            setattr(self, k, v)


class PictureList(AdditionalInformation):
    self_objects: list = List(Picture)
    description: str = String()

    def add(self, source: str, pic_object: bytes, desc: str = "") -> Picture:
        picture_object = Picture(self_source=source, self_object=pic_object, description=desc)
        self.self_objects.append(pic_object)
        return copy.deepcopy(picture_object)

    def clear(self):
        pass

    def __getitem__(self, item):
        return self.self_objects[item]

    def get_first(self):
        return self.self_objects[0]


class Person(AdditionalInformation):
    name = String()
    id = String()
    source_site = SourceWebSite()
    description = String()

    def __init__(self):
        self.__Picture = PictureList()



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
        for k, v in kwargs.items():
            setattr(self, k, v)


class Music(Media):
    pass
