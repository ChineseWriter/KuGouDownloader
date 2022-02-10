#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @FileName  :Controller.py
# @Time      :2022/1/27 8:30
# @Author    :Amundsen Severus Rubeus Bjaaland


import logging
from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import Callable, List

from MediaDL.Objects import Music, Picture
from MediaDL.Objects.FunctionObjectRoot import MusicFunction
from .Music.KuGou import Function as _KuGouFunction
from .Music.QQMusic import Function as _QQMusicFunction
from .Music.WangYiYun import Function as _WangYiYunFunction
from .Picture.Baidu import get_data as _BaiduPictureFunction
from .Picture.Bing import get_data as _BingPictureFunction

_Logger = logging.getLogger(__name__)


class Controller(object):
    """管理所有引擎"""

    def __init__(self):
        self.__music_engine: dict[str, MusicFunction] = {
            _KuGouFunction.name: _KuGouFunction(),
            _WangYiYunFunction.name: _WangYiYunFunction(),
            _QQMusicFunction.name: _QQMusicFunction()
        }
        self.__picture_engine: dict[str, Callable] = {
            "BaiduPicture": _BaiduPictureFunction,
            "BingPicture": _BingPictureFunction,
        }
        self.__video_engine = {}
        self.__novel_engine = {}

    def append_music_engine(self, name: str, engine: MusicFunction) -> bool:
        self.__music_engine[name] = engine
        return True

    def append_picture_engine(self, name: str, engine: Callable) -> bool:
        self.__picture_engine[name] = engine
        return True

    def get_picture(self, select_name: str) -> Callable:
        picture_engine_list = [engine(select_name) for engine in self.__picture_engine.values()]

        def get_one_page() -> List[Picture]:
            nonlocal picture_engine_list
            buffer = []
            with ThreadPoolExecutor() as executor:
                task_list = [executor.submit(engine) for engine in picture_engine_list]
                for task in as_completed(task_list):
                    for one_picture in task.result():
                        buffer.append(one_picture)
            return buffer

        return get_one_page

    def select_music(self, select_name: str) -> List[Music]:
        with ThreadPoolExecutor() as executor:
            task_list = [
                executor.submit(search_function.select_music, select_name)
                for search_function in self.__music_engine.values()
            ]
            buffer = []
            for task in task_list:
                for one_music in task.result():
                    buffer.append(one_music)
        return buffer

    def get_music_info(self, music: Music) -> Music:
        if music.source_site in self.__music_engine:
            return self.__music_engine[music.source_site].download_music(music)
        _Logger.warning("该歌曲的所属网站不受支持")
        return music
