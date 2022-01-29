#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @FileName  :GetMusicList.py
# @Time      :2022/1/29 12:41
# @Author    :Amundsen Severus Rubeus Bjaaland


import json
import logging
from typing import List

from MediaDL.Objects import Music
from MediaDL.Tools import get_response
from .Requirements import create_select_params

_Logger = logging.getLogger(__name__)


def get_data(select_name: str) -> List[Music]:
    response = get_response(
        "https://c.y.qq.com/soso/fcgi-bin/client_search_cp",
        create_select_params(select_name),
        {"referer": "https://y.qq.com/", "origin": "https://y.qq.com"}
    )
    if response is None:
        _Logger.warning("获取网络数据失败")
        return []
    try:
        data = response.json()
    except json.JSONDecodeError:
        _Logger.warning("Json数据解码失败")
        return []
    if data["code"] != 0:
        _Logger.warning("QQ音乐官网返回的状态码有误(不为0)")
        return []
    music_list = data["data"]["song"]["list"]
    if len(music_list) == 0:
        _Logger.info("QQ音乐官网返回的结果数量为0个")
    return []
