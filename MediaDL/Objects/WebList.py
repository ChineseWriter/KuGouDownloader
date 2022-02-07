#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @FileName  :WebList.py
# @Time      :2021/12/25 19:22
# @Author    :Amundsen Severus Rubeus Bjaaland


import copy

SupportWebList = [
    "KuGou",
    "WangYiYun",
    "QQMusic",
    "BaiduPicture",
    "BingPicture",
]


class WebType(object):
    """描述支持的网站的类型"""
    music = "Music"
    picture = "Picture"
    video = "Video"
    novel = "Novel"


class SupportWeb(object):
    """描述所有受支持网站"""
    type = ""
    e_name = ""
    c_name = ""
    official_profile_url = ""
    unofficial_profile_url = ""


class KuGou(SupportWeb):
    """支持的音乐网站：酷狗音乐"""
    type = WebType.music
    e_name = "KuGou"
    c_name = "酷狗"
    official_profile_url = "https://www.kugou.com/about/aboutus.html"
    unofficial_profile_url = "https://baike.baidu.com/item/%E9%85%B7%E7%8B%97/98649"


class WangYiYun(SupportWeb):
    """支持的音乐网站：网易云音乐"""
    type = WebType.music
    e_name = "WangYiYun"
    c_name = "网易云"
    official_profile_url = ""
    unofficial_profile_url = "https://baike.baidu.com/item/%E7%BD%91%E6%98%93%E4%BA%91%E9%9F%B3%E4%B9%90/4453795"


class QQMusic(SupportWeb):
    """支持的音乐网站：QQ音乐"""
    type = WebType.music
    e_name = "QQ"
    c_name = "QQ音乐"
    official_profile_url = "https://www.tencentmusic.com/"
    unofficial_profile_url = "https://baike.baidu.com/item/QQ%E9%9F%B3%E4%B9%90/1157130"


# TODO 继续完成受支持的网站列表功能
class WebList(object):
    """受支持的网站及其相关信息"""
    __web_list = [
        KuGou,
        WangYiYun,
        QQMusic
    ]

    @classmethod
    def supported_music_web(cls):
        """返回所有受支持的音乐网站列表"""
        buffer = []
        for i in cls.__web_list:
            i: SupportWeb
            if i.type == WebType.music:
                buffer.append(i)
        return copy.deepcopy(buffer)
