#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @FileName  :Base.py
# @Time      :2021/7/17 11:59
# @Author    :Amundsen Severus Rubeus Bjaaland


class MusicList(object):
    def __init__(self, MusicName: str) -> None:
        assert isinstance(MusicName, str)
        self.__MusicName = MusicName
