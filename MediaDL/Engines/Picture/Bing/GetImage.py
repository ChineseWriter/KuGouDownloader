#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @FileName  :GetImage.py
# @Time      :2022/1/30 19:15
# @Author    :Amundsen Severus Rubeus Bjaaland


import json
import logging
from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import Callable, List

from bs4 import BeautifulSoup as bs

from MediaDL.Objects import Picture
from MediaDL.Tools import get_response

_Logger = logging.getLogger(__name__)


def _download_picture(data: bs) -> Picture:
    image_tag = data.find("a")
    if image_tag is None:
        return Picture()
    image_info: str = image_tag.get("m")
    if image_info is None:
        return Picture()
    try:
        image_info: dict = json.loads(image_info)
    except json.JSONDecodeError:
        return Picture()
    response = get_response(image_info.get("murl"))
    if response is None:
        return Picture()
    picture = Picture()
    picture.source_site = "BingPicture"
    picture.self_source = image_info.get("murl")
    picture.master_id = image_info.get("md5")
    picture.description = image_info.get("t")
    picture.sub_id = image_info.get("mid")
    picture.self_object = response.content
    return picture


def _clean_data(data: List[bs], name: str) -> List[Picture]:
    buffer = []
    with ThreadPoolExecutor() as executor:
        task_list = [executor.submit(_download_picture, one_picture_info)
                     for one_picture_info in data]
        for i in as_completed(task_list):
            result = i.result()
            if not result.master_id:
                continue
            result.name = name
            buffer.append(result)
    return buffer


def get_data(select_name: str) -> Callable:
    next_url = f"https://cn.bing.com/images/search?q={select_name}" \
               f"&form=BESBTB&first=1&tsc=ImageBasicHover&ensearch=1"

    def get_one_page():
        nonlocal next_url
        while True:
            response = get_response(next_url)
            if response is None:
                _Logger.warning("网络连接错误")
                continue
            html = bs(response.text, "lxml")
            container_div_tag = html.find("div", attrs={"class": "dgControl hover"})
            if container_div_tag is None:
                _Logger.warning("未找到任何图片信息")
                continue
            image_info_li_tag_list = container_div_tag.find_all("li")
            next_data_url = container_div_tag.get("data-nexturl")
            if next_data_url is None:
                _Logger.warning("未获取到下一个图片包的URL")
            else:
                next_url = "https://cn.bing.com/" + next_data_url
            return _clean_data(image_info_li_tag_list, select_name)

    return get_one_page
