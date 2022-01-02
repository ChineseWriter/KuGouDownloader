#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @FileName  :GetMusicList.py
# @Time      :2022/1/2 12:06
# @Author    :Amundsen Severus Rubeus Bjaaland


import time

import js2py

from MediaDL.Objects import GetList
from .Requirements import create_data_list, GetSignFunction, GetSign

# 初始化JS命名空间
js_name_space = js2py.EvalJs()
# 在JS命名空间中初始化签名构造函数
js_name_space.execute(GetSignFunction)


def set_time_stamp() -> int:
    """获取时间戳

    返回Python标准时间戳的一千倍再取整后的值。

    :return: 获取的时间戳。
    """
    return int(time.time() * 1000)


def create_signature(select_name: str, time_stamp: int) -> str:
    """创建发出请求需要的签名（密码）

    使用第三方库Js2Py运行酷狗的签名构造函数将数据转换为签名。

    :return: 创建的签名值。
    """
    data_list = create_data_list(select_name, time_stamp)
    # 在JS命名空间中初始化数据
    js_name_space.execute("o=" + str(data_list))
    # 执行构造函数
    js_name_space.execute(GetSign)
    # 返回创建的签名
    return js_name_space.signature


def get_data() -> list:
    """返回获取的原始数据
    :return: 获取的数据
    """
    # TODO 完成该函数
    return []


class GetMusicList(GetList):
    def __call__(self, *args, **kwargs):
        pass
