#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @FileName  :GetImage.py
# @Time      :2022/1/30 13:13
# @Author    :Amundsen Severus Rubeus Bjaaland


import json
import logging
import re
from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import List, Callable

from MediaDL.Objects import Picture
from MediaDL.Tools import get_response
from .Requirement import create_params

_Logger = logging.getLogger(__name__)


def baidtu_uncomplie(url):
    res = ''
    c = ['_z2C$q', '_z&e3B', 'AzdH3F']
    d = {'w': 'a', 'k': 'b', 'v': 'c', '1': 'd', 'j': 'e', 'u': 'f', '2': 'g', 'i': 'h', 't': 'i', '3': 'j', 'h': 'k',
         's': 'l', '4': 'm', 'g': 'n', '5': 'o', 'r': 'p', 'q': 'q', '6': 'r', 'f': 's', 'p': 't', '7': 'u', 'e': 'v',
         'o': 'w', '8': '1', 'd': '2', 'n': '3', '9': '4', 'c': '5', 'm': '6', '0': '7', 'b': '8', 'l': '9', 'a': '0',
         '_z2C$q': ':', '_z&e3B': '.', 'AzdH3F': '/'}
    if (url == None or 'http' in url):
        return url
    else:
        j = url
        for m in c:
            j = j.replace(m, d[m])
        for char in j:
            if re.match('^[a-w\d]+$', char):
                char = d[char]
            res = res + char
        return res


def _download_picture(picture_info: dict) -> Picture:
    picture = Picture()
    picture.source_site = "BaiduPicture"
    if not (picture_info.get("thumbURL") and picture_info.get("objURL") and picture_info.get(
            "simid") and picture_info.get("fromPageTitleEnc") and picture_info.get("os")):
        return Picture()
    response = get_response(picture_info.get("thumbURL"))
    if response is None:
        return Picture()
    picture.self_source = picture_info.get("thumbURL")
    picture.sub_self_source = baidtu_uncomplie(picture_info.get("objURL"))
    picture.master_id = picture_info.get("simid")
    picture.description = picture_info.get("fromPageTitleEnc")
    picture.sub_id = picture_info.get("os")
    picture.self_object = response.content
    return picture


def _clean_data(data: dict) -> List[Picture]:
    data_list = data.get("data")
    if not data_list:
        return []
    buffer = []
    with ThreadPoolExecutor() as executor:
        task_list = [executor.submit(_download_picture, one_picture_info)
                     for one_picture_info in data_list]
        for i in as_completed(task_list):
            result = i.result()
            if not result.master_id:
                continue
            result.name = data["queryExt"]
            buffer.append(result)
    return buffer


def get_data(select_name: str) -> Callable:
    page_number_counter = 1

    def get_one_page():
        nonlocal page_number_counter
        while True:
            param = create_params(select_name, page_number_counter)
            response = get_response("https://image.baidu.com/search/acjson", param)
            if response is None:
                _Logger.warning("网络连接错误")
                continue
            try:
                json_data = response.json()
            except json.JSONDecodeError:
                _Logger.warning("Json数据解析失败")
                continue
            page_number_counter += 1
            return _clean_data(json_data)

    return get_one_page
