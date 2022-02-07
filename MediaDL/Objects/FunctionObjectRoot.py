#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @FileName  :FunctionObjectRoot.py
# @Time      :2022/1/2 12:11
# @Author    :Amundsen Severus Rubeus Bjaaland


from abc import ABC, abstractmethod
from typing import List

from .CirculationObjectsRoot import Music


class Function(ABC):
    """所有工具的基类"""
    pass


class MusicFunction(Function):
    """规定每个音乐下载引擎应该实现的方法"""
    name = ""

    def __init__(self) -> None:
        pass

    @abstractmethod
    def select_music(self, select_name: str) -> List[Music]:
        """获取查询的关键字的结果列表"""
        return []

    @abstractmethod
    def download_music(self, basic_info: Music) -> Music:
        """下载歌曲"""
        return Music()

    @abstractmethod
    def get_rec_music(self) -> List[Music]:
        """获取推荐歌曲"""
        return []
