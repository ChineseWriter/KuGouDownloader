#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @FileName  :DownloadMusic.py
# @Time      :2022/1/16 11:30
# @Author    :Amundsen Severus Rubeus Bjaaland


import json
import logging
import re

from bs4 import BeautifulSoup as bs

from MediaDL.Objects import Music
from MediaDL.Tools import get_response, replace
from .Requirements import set_time_stamp, create_get_music_params

_Logger = logging.getLogger(__name__)


def _check_info(music: Music) -> bool:
    """检查歌曲下载相关信息是否完整(是否含有主id)

    :param music: 歌曲信息
    :return: 完整则返回True，不完整则返回False
    """
    # 检查该歌曲对象是否有主id
    if not music.master_id:
        return False
    return True


def _get_singer_desc(singer_id: str) -> str:
    """获取歌手的简介

    :param singer_id: 酷狗网站歌手的统一编号
    :return: 歌手简介
    """
    # 创建连接并获取数据
    response = get_response(f"https://www.kugou.com/singer/{singer_id}.html")
    # 检查获取的数据是否为空
    if response is None:
        _Logger.warning("获取歌手简介失败")
        return ""
    # 将数据包装为bs类型
    html = bs(response.text, "lxml")
    # 找到div标签(HTML)
    div_tag = html.find("div", attrs={"class": "intro"})
    # 检查标签是否存在
    if div_tag is None:
        _Logger.warning("获取歌手简介失败")
        return ""
    # 找到p标签(HTML)
    p_tag = div_tag.find("p")
    # 检查标签是否存在
    if p_tag is None:
        _Logger.warning("获取歌手简介失败")
        return ""
    # 储存歌手的简介
    desc = p_tag.text
    if not desc:
        desc = p_tag.get_text()
    if not desc:
        _Logger.warning("获取歌手简介失败")
        return ""
    return desc


def _get_music_mv(mv_id: int) -> bytes:
    # TODO 完成该函数
    return b""


def _download_music(music: Music, play_url: str, play_backup_url: str) -> Music:
    if play_url:
        response = get_response(play_url)
        if response:
            music.self_source = play_url
            music.self_object = response.content
            return music
    if play_backup_url:
        response = get_response(play_backup_url)
        if response:
            music.self_source = play_backup_url
            music.self_object = response.content
            return music
    _Logger.warning(f"未找到歌曲{music.name}的源")
    return music


def _clean_data(music: Music, data: dict) -> Music:
    """处理返回的歌曲数据

    :param music: 歌曲的信息存储处
    :param data: 获取的原始数据
    :return: 歌曲信息
    """
    # 确认该歌曲是否包含于某个专辑中
    if data["have_album"] == 1:
        music.album = data["album_name"]
    # 为该歌曲的专辑封面列表添加描述
    music.poster_list.description = music.name + "的海报封面"
    # 创建连接并获取数据
    response = get_response(data["img"])
    # 检查获取的数据是否为空
    if response is None:
        _Logger.warning("获取歌手简介失败")
    else:
        # 将歌曲的专辑封面添加至歌曲信息中
        music.poster_list.add(data["img"], response.content)
    # 获取每个歌手的信息
    for one_singer in data["authors"]:
        singer_id = one_singer["author_id"]
        music.singer_list.add(
            singer_id, replace(one_singer["author_name"]),
            "KuGou", _get_singer_desc(singer_id)
        )
    music.lyrics = data["lyrics"]
    string = re.match("(.*?)( - )(.*?)(-)", data["audio_name"] + "-")
    music.name = replace(string.group(3)) if string else data["audio_name"]
    _download_music(music, data.get("play_url"), data.get("play_backup_url"))
    if data["have_mv"] == 1:
        music.mv = _get_music_mv(int(data['video_id']))
    return music


def get_data(music: Music) -> Music:
    """根据歌曲原始信息返回获取的歌曲信息

    :param music: 歌曲基本信息
    :return: 歌曲的详细信息
    """
    if not _check_info(music):
        _Logger.warning("Song information is missing.")
        return music
    time_stamp = set_time_stamp()
    params = create_get_music_params(music, time_stamp)
    response = get_response(
        "https://wwwapi.kugou.com/yy/index.php",
        params,
        {"referrer": "https://www.kugou.com/"}
    )
    string_1 = response.content.decode('utf-8')
    string_2 = string_1[string_1.find('(') + 1:-2]
    data = json.loads(string_2)
    if data["status"] != 1:
        _Logger.warning("Unknown error: the returned data is incorrect.")
        return music
    data = data["data"]
    return _clean_data(music, data)
