#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @FileName  :Controller.py
# @Time      :2022/1/16 9:06
# @Author    :Amundsen Severus Rubeus Bjaaland


from typing import List

from MediaDL.Objects import MusicFunction, Music
from .DownloadMusic import get_data as get_music
from .GetMusicList import get_data as get_list


class KuGouFunction(MusicFunction):
    """定义酷狗音乐的所有可用API"""

    name = "KuGou"

    def select_music(self, select_name: str) -> List[Music]:
        """从酷狗官网上查询歌曲

        :param select_name: 查询的关键字
        :return: 查询结果，为该MediaDL包的标准Music类型
        """
        return get_list(select_name)

    def download_music(self, basic_info: Music) -> Music:
        """从酷狗官网上下载歌曲

        :param basic_info: 歌曲的基本信息
        :return: 歌曲的详细信息
        """
        return get_music(basic_info)

    def get_rec_music(self) -> List[Music]:
        # TODO 完成该函数
        return []
