#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @FileName  :GetMusicList.py
# @Time      :2022/1/27 8:37
# @Author    :Amundsen Severus Rubeus Bjaaland


import json
import logging
from typing import List

from MediaDL.Objects import Music
from MediaDL.Tools import get_response
from .Requirement import create_select_params

_Logger = logging.getLogger(__name__)


def _clean_data(music_list: list) -> List[Music]:
    """处理返回的歌曲列表

    将列表中以字典存储的歌曲信息用该软件包的标准类储存

    :param music_list: 获取的歌曲列表
    :return: 转换后的歌曲列表
    """
    music_buffer = []
    for music_item in music_list:
        music_item: dict
        music = Music()
        music.source_site = "WangYiYun"
        music.name = music_item["name"]
        music.master_id = str(music_item["id"])
        music.singer_list.description = music.name + "的演唱者"
        for singer_info in music_item["ar"]:
            music.singer_list.add(str(singer_info["id"]), singer_info["name"], "WangYiYun")
        music_buffer.append(music)
    return music_buffer


def get_data(select_name: str) -> List[Music]:
    """返回获取的歌曲列表

    :param select_name: 要搜索的名称
    :return: 获取的数据
    """
    response = get_response(
        "https://music.163.com/weapi/cloudsearch/get/web?csrf_token=",
        method="post",
        data=create_select_params(select_name)
    )
    try:
        json_data = response.json()
    except json.decoder.JSONDecodeError:
        _Logger.error("Failed to parse JSON data.")
        return []
    if json_data["code"] != 200:
        _Logger.error("Failed to get data.")
        return []
    song_list = json_data["result"]["songs"]
    if len(song_list) == 0:
        _Logger.info("网易云官网返回的结果数量为0个")
        return []
    return _clean_data(song_list)
