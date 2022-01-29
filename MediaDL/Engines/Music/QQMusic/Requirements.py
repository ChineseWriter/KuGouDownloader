#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @FileName  :Requirements.py
# @Time      :2022/1/29 12:42
# @Author    :Amundsen Severus Rubeus Bjaaland


def create_select_params(select_name: str):
    """创建获取歌曲列表需要的参数

    :param select_name: 查询名称
    :return: 创建的参数
    """
    return {
        "ct": 24,
        "qqmusic_ver": 1298,
        "new_json": 1,
        "remoteplace": "Text.yqq.song",
        "searchid": 63229658163010696,
        "t": 0,
        "aggr": 1,
        "cr": 1,
        "catZhida": 1,
        "lossless": 0,
        "flag_qc": 0,
        "p": 1,
        "n": 10,
        "w": select_name,
        "g_tk": 5381,
        "loginUin": 0,
        "hostUin": 0,
        "format": "json",
        "inCharset": "utf-8",
        "outCharset": "utf-8",
        "notice": 0,
        "platform": "yqq.json",
        "needNewCode": 0
    }
