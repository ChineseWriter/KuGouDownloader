#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @FileName  :LocalTools.py
# @Time      :2022/1/8 19:16
# @Author    :Amundsen Severus Rubeus Bjaaland


import logging


def set_log() -> bool:
    """设置全局日志格式"""
    logging.basicConfig(
        format="[%(asctime)s](%(levelname)s)%(name)s: %(message)s",
        datefmt="%Y/%m/%d %H:%M:%S",
        level=logging.WARNING
    )
    return True
