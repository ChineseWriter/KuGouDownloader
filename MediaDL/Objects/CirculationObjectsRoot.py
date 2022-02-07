#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @FileName  :Objects.py
# @Time      :2021/12/25 18:45
# @Author    :Amundsen Severus Rubeus Bjaaland


import copy
import logging
import os.path

import cv2
import eyed3
import numpy

from .Validators import String, Bytes, URL, SourceWebSite, List, Lyrics

_Logger = logging.getLogger(__name__)


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

    def __repr__(self):
        return f"<Media name={self.name} source-site={self.source_site}>"

    def __str__(self):
        return f"<Media name={self.name} source-site={self.source_site}>"


class Picture(Media):
    description: str = String()
    sub_self_source: str = String()

    def __init__(self, **kwargs):
        super(Picture, self).__init__(**kwargs)
        self.description = ""
        self.sub_self_source = ""

    @property
    def image_object(self) -> numpy.ndarray:
        if self.self_object:
            return cv2.imdecode(
                numpy.frombuffer(self.self_object, numpy.uint8), cv2.IMREAD_COLOR
            )
        else:
            return numpy.array([[[]]], dtype=numpy.uint8)

    @property
    def shape(self):
        if self.self_object:
            return cv2.imdecode(
                numpy.frombuffer(self.self_object, numpy.uint8), cv2.IMREAD_COLOR
            ).shape
        else:
            return 0, 0, 3

    def save(self, path: str, other_desc: str = "") -> bool:
        """保存该图片

        :param path: 该图片文件的保存路径
        :param other_desc: 其他的描述，用于防止图片文件重名
        :return: 保存是否成功
        """
        try:
            os.makedirs(path, exist_ok=True)
        except (FileExistsError, OSError):
            _Logger.warning("目标目录权限不正确或有其它问题导致目录创建失败")
            return False
        if other_desc:
            file_path = os.path.join(path, f"{self.source_site} - {self.name} - {other_desc}.jpg")
        else:
            _Logger.warning("您没有为图片创建唯一标识")
            file_path = os.path.join(path, f"{self.source_site} - {self.name}.jpg")
        with open(file_path, "wb") as File:
            File.write(self.self_object)
        return True


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

    def __repr__(self):
        return f"<Music name={self.name} singers={self.__singer_list.name_list} " \
               f"album={self.album} source-site={self.source_site}>"

    def __str__(self):
        return f"<Music name={self.name} singers={self.__singer_list.name_list} " \
               f"album={self.album} source-site={self.source_site}>"

    @property
    def poster_list(self):
        """返回该歌曲的专辑封面列表"""
        return self.__poster_list

    @property
    def singer_list(self):
        """返回该歌曲的演唱者列表"""
        return self.__singer_list

    def save(self, path: str = "./", lyric_file: bool = True, replace: bool = False) -> bool:
        """保存该歌曲

        :param path: 歌曲的保存路径
        :param lyric_file: 是否将歌词另存为一个文件
        :param replace: 当歌曲已存在时是否替换
        :return: 保存是否成功
        """
        try:
            os.makedirs(path, exist_ok=True)
        except (FileExistsError, OSError):
            _Logger.warning("目标目录权限不正确或有其它问题导致目录创建失败")
            return False
        music_file_path = os.path.join(path, f"{self.__singer_list.name_list} -"
                                             f" {self.name}.mp3")
        lyric_file_path = os.path.join(path, f"{self.__singer_list.name_list} -"
                                             f" {self.name}.lrc")
        if replace:
            with open(music_file_path, "wb") as File:
                File.write(self.self_object)
        else:
            if not os.path.exists(music_file_path):
                with open(music_file_path, "wb") as File:
                    File.write(self.self_object)
        one_music = eyed3.load(music_file_path, (2, 3, 0))
        if one_music is None:
            os.remove(music_file_path)
            _Logger.warning("写入歌曲元信息失败")
            return False
        one_music.initTag((2, 3, 0))
        one_music.tag.title = self.name
        one_music.tag.artist = self.__singer_list.name_list
        one_music.tag.lyrics.set(self.lyrics)
        one_music.tag.album = self.album
        music_poster: Picture = self.poster_list.get_first()
        one_music.tag.images.set(3, music_poster.self_object, "image/jpeg", "Cover(front)", music_poster.description)
        one_music.tag.images.set(4, music_poster.self_object, "image/jpeg", "Cover(back)", music_poster.description)
        one_music.tag.save(version=(2, 3, 0))
        if lyric_file:
            with open(lyric_file_path, "w", encoding="UTF-8") as File:
                File.write(self.lyrics)
        return True
