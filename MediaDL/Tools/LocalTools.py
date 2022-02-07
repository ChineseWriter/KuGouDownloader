#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @FileName  :LocalTools.py
# @Time      :2022/1/8 19:16
# @Author    :Amundsen Severus Rubeus Bjaaland


import logging
import re

_INVALID_CHAR_LIST = ["*", ".", '"', "'", "/", "\\", "[", "}", ":", ";", "|", ",", "<", ">", "?"]
_INVALID_PATTERN_LIST = ["<.*?>", "</.*?>"]


def set_log(level: int = logging.WARNING) -> bool:
    """设置全局日志格式"""
    logging.basicConfig(
        format="[%(asctime)s](%(levelname)s)%(name)s: %(message)s",
        datefmt="%Y/%m/%d %H:%M:%S",
        level=level
    )
    return True


def replace(string: str) -> str:
    for i in _INVALID_PATTERN_LIST:
        string = re.sub(i, "", string)
    for i in _INVALID_CHAR_LIST:
        string = string.replace(i, "")
    return string
