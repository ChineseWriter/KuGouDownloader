#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @FileName  :DownloadMusic.py
# @Time      :2022/1/27 8:38
# @Author    :Amundsen Severus Rubeus Bjaaland
import json
import logging

from bs4 import BeautifulSoup as bs

from MediaDL.Objects import Music
from MediaDL.Tools import get_response
from .Requirement import create_lyrics_params, create_get_music_params

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


def _get_basic_info(music: Music) -> bool:
    """获取歌曲的基本信息

    获取歌曲的名称，主id，副id，歌手，海报封面等信息

    :param music: 原始歌曲及其信息
    :return: 歌曲及其基本信息
    """
    # 创建连接并获取数据
    response = get_response(
        "https://music.163.com/song",
        {"id": music.master_id}
    )
    # 检查网络获取的数据是否为空
    if response is None:
        _Logger.warning("网络获取的数据为空")
        return False
    # 将数据转换为bs对象
    html = bs(response.text, "lxml")
    # 找到包含歌曲基本信息的div标签(HTML)
    details_div_tag = html.find("div", attrs={"class": "cnt"})
    # 确认找到了包含基本信息的标签
    if details_div_tag is None:
        _Logger.warning("未找到歌曲的基本信息")
        return False
    # 获取包含歌曲名称的em标签(HTML)
    music_name_tag = details_div_tag.find("em", attrs={"class": "f-ff2"})
    # 确认找到了包含歌曲名称的标签
    if music_name_tag is None:
        _Logger.warning("未找到该歌曲的名称")
    else:
        # 将标签的内容作为歌曲名
        music.name = music_name_tag.text
        if not music.name:
            music.name = music_name_tag.get_text()
            if not music.name:
                _Logger.warning("未找到该歌曲的名称")
    # 找到歌曲的歌手信息
    singers_info_tag = details_div_tag.find("span")
    if singers_info_tag is None:
        _Logger.warning("未找到该歌曲的歌手相关信息")
    else:
        # 找到包含每个歌手信息的标签
        singers = singers_info_tag.find_all("a")
        # 将每个歌手的信息添加到Music对象中
        for singer_info in singers:
            music.singer_list.add(str(singer_info["href"].split("=")[1]), singer_info.text, "WangYiYun")
    # 找到歌曲的专辑信息
    album_and_singer_info_tag = details_div_tag.find_all("a", attrs={"class": "s-fc7"})
    if album_and_singer_info_tag:
        # 获取包含歌曲专辑信息的标签
        album_info_tag = album_and_singer_info_tag[-1]
        # 将该标签的内容作为该歌曲的专辑名
        music.album = album_info_tag.text
        # 将该专辑的id作为该歌曲的副id
        music.sub_id = album_info_tag.get("href").split("=")[1] if album_info_tag.get("href") else ""
        # 获取包含该歌曲的专辑页面
        response = get_response("https://music.163.com/album", {"id": music.sub_id})
        music.poster_list.description = music.name + "的海报封面"
        # 检查网络返回的数据是否为空
        if response is None:
            _Logger.warning("网络获取的数据为空")
        else:
            # 找到包含该歌曲的专辑封面的img标签(HTML)
            picture_source_tag = bs(response.text, "lxml").find("img", attrs={"class": "j-img"})
            if picture_source_tag is None:
                _Logger.warning("未找到该歌曲的海报封面")
            else:
                # 找到歌曲专辑封面的源URL
                picture_source = picture_source_tag.get("data-src")
                if picture_source is None:
                    _Logger.warning("未找到该歌曲的海报封面")
                else:
                    # 获取歌曲的专辑封面
                    response = get_response(picture_source)
                    if response is None:
                        _Logger.warning("未找到该歌曲的海报封面")
                    else:
                        # 将该歌曲的封面添加入歌曲信息中
                        music.poster_list.add(picture_source, response.content)
    return True


def _get_lyrics(music: Music) -> bool:
    """获取歌曲的歌词

    :param music: 原始歌曲及其信息
    :return: 歌曲信息及歌词
    """
    # 创建获取歌词需要的参数
    params = create_lyrics_params(music.master_id)
    # 创建连接并获取数据
    response = get_response(
        "https://music.163.com/weapi/song/lyric?csrf_token=", method="post", data=params
    )
    # 检查网络获取的数据是否为空
    if response is None:
        _Logger.warning("网络获取的数据为空")
        return False
    # 将Json格式数据解码
    try:
        json_data = response.json()
    except json.JSONDecodeError:
        _Logger.warning("解码Json数据失败")
        return False
    # 确认网易云官网的返回码
    if json_data["code"] != 200:
        _Logger.warning("获取歌词失败")
        return False
    # 确认该歌曲是否有歌词
    if json_data.get("nolyric"):
        music.lyrics = "[00:00.00]纯音乐，请欣赏。"
    else:
        music.lyrics = json_data["lrc"]["lyric"]
    return True


def _get_music_object(music: Music) -> bool:
    """获取歌曲音频文件

    :param music: 原始歌曲及其信息
    :return: 歌曲信息及音频文件
    """
    # 创建获取歌曲文件需要的参数
    params = create_get_music_params(music.master_id)
    # 创建连接并获取数据
    response = get_response(
        "https://music.163.com/weapi/song/enhance/player/url?csrf_token=",
        method="post", data=params
    )
    # 检查网络获取的数据是否为空
    if response is None:
        _Logger.warning("网络获取的数据为空")
        return False
    # 将Json格式数据解码
    try:
        json_data = response.json()
    except json.JSONDecodeError:
        _Logger.warning("解码Json数据失败")
        return False
    # 获取歌曲的源URL
    music.self_source = json_data["data"][0]["url"]
    # 创建连接并获取数据
    response = get_response(music.self_source)
    # 检查网络获取的数据是否为空
    if response is None:
        _Logger.warning("网络获取的数据为空")
        return False
    # 将歌曲文件添加入歌曲信息中
    music.self_object = response.content
    return True


def _get_music_mv(music: Music) -> bool:
    """获取歌曲MV

    :param music: 原始歌曲及其信息
    :return: 歌曲信息及MV
    """
    # TODO 完成该函数
    return True


def get_data(music: Music) -> Music:
    """根据歌曲原始信息返回获取的歌曲信息

    :param music: 歌曲基本信息
    :return: 歌曲的详细信息
    """
    # 检查歌曲的基本信息(主id)
    if not _check_info(music):
        _Logger.warning("歌曲基本信息(主id)为空")
        return music
    # 获取歌曲其余的基本信息
    if not _get_basic_info(music):
        _Logger.warning("获取歌曲基本信息失败")
    # 获取歌词
    if not _get_lyrics(music):
        _Logger.warning("获取歌词失败")
    # 获取歌曲文件
    if not _get_music_object(music):
        _Logger.warning("获取歌词文件失败")
    # 获取歌曲的MV
    if not _get_music_mv(music):
        _Logger.warning("获取歌曲MV失败")
    return music
