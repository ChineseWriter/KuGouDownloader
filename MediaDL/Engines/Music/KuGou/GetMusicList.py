#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @FileName  :GetMusicList.py
# @Time      :2022/1/2 12:06
# @Author    :Amundsen Severus Rubeus Bjaaland
"""在酷狗官网上查询歌曲的API"""

import json
import logging
from typing import List

import js2py

from MediaDL.Objects import Music
from MediaDL.Tools import get_response, replace
from .Requirements import create_get_list_params, create_data_list, GetSignFunction, GetSign, set_time_stamp

_Logger = logging.getLogger(__name__)

# 初始化JS命名空间
js_name_space = js2py.EvalJs()
# 在JS命名空间中初始化签名构造函数
js_name_space.execute(GetSignFunction)


def _create_signature(select_name: str, time_stamp: int) -> str:
    """创建发出请求需要的签名（密码）

    使用第三方库Js2Py运行酷狗的签名构造函数将数据转换为签名

    :param select_name: 查询的歌曲名称
    :param time_stamp: 该次请求时使用的时间戳
    :return: 创建的签名值
    """
    data_list = create_data_list(select_name, time_stamp)
    # 在JS命名空间中初始化数据
    js_name_space.execute("o=" + str(data_list))
    # 执行构造函数
    js_name_space.execute(GetSign)
    # 返回创建的签名
    return js_name_space.signature


def _clean_data(music_list: list) -> list:
    """处理返回的歌曲列表

    将列表中以字典存储的歌曲信息用该软件包的标准类储存

    :param music_list: 获取的歌曲列表
    :return: 转换后的歌曲列表
    """
    # 储存所有Music对象使用的列表
    music_buffer = []
    # 获取歌曲名称失败的错误数量
    name_error = 0
    # 获取歌曲主id失败的错误数量
    id_error = 0
    # 获取歌曲演唱者信息失败的错误数量
    singers_info_error = 0
    # 获取单个音乐的信息
    for music_item in music_list:
        music_item: dict
        music = Music()
        # 注明音乐的来源网站
        music.source_site = "KuGou"
        # 获取音乐的名称
        music_name = music_item.get("SongName")
        # 检查音乐的名称是否为空
        if not music_name:
            name_error += 1
            continue
        # 去掉音乐名称中有HTML代码特征的部分
        music.name = replace(music_name)
        # 注明音乐在该网站的主id，在酷狗音乐网站中是该音乐唯一的哈希值
        music.master_id = music_item.get("FileHash")
        # 检查该音乐的主id是否为空
        if not music.master_id:
            id_error += 1
            continue
        # 注明音乐在该网站的副id，在酷狗音乐网站中是该音乐的专辑的id
        music.sub_id = music_item.get("AlbumID")
        # 注明歌曲的演唱者列表的描述，这里使用通用描述
        music.singer_list.description = music.name + "的演唱者"
        # 获取该音乐的演唱者id的列表
        singer_id_list = music_item.get("SingerId")
        # 获取该音乐的演唱者名称的列表
        singer_name_list = music_item.get("SingerName").split("、")
        # 若演唱者id列表和演唱者名称列表均非空
        if singer_id_list and singer_name_list:
            # 检查演唱者id列表和演唱者名称列表长度是否相等(即二者是否对应)
            if len(singer_id_list) == len(singer_name_list):
                # 向音乐信息中添加演唱者信息
                for singer_id, singer_name in zip(singer_id_list, singer_name_list):
                    music.singer_list.add(str(singer_id), replace(singer_name), "KuGou")
            else:
                singers_info_error += 1
        # 将该音乐的信息加入Music对象列表中
        music_buffer.append(music)
    # 检查并报出所有获取音乐信息时出现的问题
    if name_error != 0:
        _Logger.warning(f"{name_error}首歌曲获取歌曲名失败")
    if id_error != 0:
        _Logger.warning(f"{id_error}首歌曲获取歌曲主id失败")
    if singers_info_error != 0:
        _Logger.warning(f"{singers_info_error}首歌曲的演唱者信息有误(演唱者id与演唱者名称数量不匹配)")
    # 返回Music对象列表
    return music_buffer


def get_data(select_name: str) -> List[Music]:
    """返回获取的歌曲列表

    :param select_name: 要搜索的名称
    :return: 获取的数据
    """
    # 生成发出HTTP请求需要的负载数据
    time_stamp = set_time_stamp()  # 设置时间戳
    signature = _create_signature(select_name, time_stamp)  # 创建签名(时效密码)
    params = create_get_list_params(select_name, time_stamp, signature)  # 创建HTTP负载数据
    # 创建连接并获取数据
    response = get_response(
        "https://complexsearch.kugou.com/v2/search/song?",
        params,
        {"referer": "https://www.kugou.com/"}
    )
    # 检查网络返回的数据是否为空
    if response is None:
        _Logger.warning("网络获取的数据为空")
        return []
    # 将数据解码并转换为Python字典
    try:
        string_1 = response.content.decode('UTF-8')  # 以UTF-8格式解码
        string_2 = string_1[string_1.find('(') + 1:-2]  # 获取有效数据片段
        data = json.loads(string_2)  # 转换为Python字典
    except (UnicodeDecodeError, json.JSONDecodeError):
        _Logger.warning("返回的数据无法被有效解码")
        return []
    # 检查状态码是否正确
    if data["status"] != 1:
        # 若有误则显示错误信息并退出函数
        _Logger.warning("酷狗官网返回的状态码不正确")
        return []
    music_list = data["data"]["lists"]  # 获取歌曲相关信息
    # 检查列表是否为空
    if len(music_list) == 0:
        _Logger.info("酷狗官网返回的结果数量为0个")
        return []
    return _clean_data(music_list)
