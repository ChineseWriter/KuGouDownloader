#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @FileName  :HeaderCreator.py
# @Time      :2021/6/2 20:01
# @Author    :Amundsen Severus Rubeus Bjaaland
"""Http协议请求头构造"""


class UserAgentCreator(object):
    """构造Http协议请求头中User-Agent"""

    @classmethod
    def get_user_agent(cls):
        """构造Http协议请求头中User-Agent

        :return: Edge浏览器的User-Agent
        """
        return "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.77 " \
               "Safari/537.36 Edg/91.0.864.37"


class Header(object):
    """构造Http协议请求头"""
    # 构造时需指定的常量
    # # Host部分
    HOST_KUGOU = "www.kugou.com"
    HOST_WANGYIYUN = "music.163.com"
    HOST_QQ = "y.qq.com"
    # # Origin部分
    ORIGIN_KUGOU = "https://www.kugou.com"
    ORIGIN_WANGYIYUN = "https://music.163.com"
    ORIGIN_QQ = "https://y.qq.com"
    # # Referrer部分
    # # # 主页面访问所需Referrer头
    REFERRER_KUGOU_MAIN = "https://www.kugou.com/"
    REFERRER_WANGYIYUN_MAIN = "https://music.163.com/"
    REFERRER_QQ_MAIN = "https://y.qq.com/"
    # # # 搜索页面访问所需Referrer头
    REFERRER_KUGOU_SEARCH = "https://www.kugou.com/"
    REFERRER_WANGYIYUN_SEARCH = "https://music.163.com/"
    REFERRER_QQ_SEARCH = "https://y.qq.com/"
    # # # 获取歌曲信息所需Referrer头
    REFERRER_KUGOU_GETINFO = "https://www.kugou.com/"
    REFERRER_WANGYIYUN_GETINFO = "https://music.163.com/search/"
    # # # 获取歌手信息所需Referrer头
    REFERRER_KUGOU_SINGERINFO = "https://www.kugou.com/song/"

    # 由Host头组成的list
    HOST_LIST = [
        HOST_KUGOU,
        HOST_WANGYIYUN,
        HOST_QQ
    ]
    # 由Origin头组成的list
    ORIGIN_LIST = [
        ORIGIN_KUGOU,
        ORIGIN_WANGYIYUN,
        ORIGIN_QQ
    ]
    # 由Referrer头组成的list
    REFERRER_LIST = [
        # 主页面访问所需Referrer头
        REFERRER_KUGOU_MAIN,
        REFERRER_WANGYIYUN_MAIN,
        REFERRER_QQ_MAIN,
        # 搜索页面访问所需Referrer头
        REFERRER_KUGOU_SEARCH,
        REFERRER_WANGYIYUN_SEARCH,
        REFERRER_QQ_SEARCH,
        # 获取歌曲信息所需Referrer头
        REFERRER_KUGOU_GETINFO,
        REFERRER_WANGYIYUN_GETINFO,
        # 获取歌手信息所需Referrer头
        REFERRER_KUGOU_SINGERINFO
    ]

    @classmethod
    def GetHeader(cls, Host=None, Origin=None, Referrer=None, UserAgent=None) -> dict:
        """根据传入的参数构造Http请求头所需dict

        :param Host: 该参数必须位于HOST_LIST中，为str类型或None类型(请求头中不予添加)
        :param Origin: 该参数必须位于ORIGIN_LIST中，为str类型或None类型(请求头中不予添加)
        :param Referrer: 该参数必须位于REFERRER_LIST中，为str类型或None类型(请求头中不予添加)
        :param UserAgent: 为空时使用默认User-Agent头，不为空时使用传入值
        :return: 返回构造好的dict
        """
        if UserAgent is not None:
            OneHeader = {"User-Agent": UserAgent}
        else:
            OneHeader = {"User-Agent": UserAgentCreator.get_user_agent()}
        if Host is not None:
            if Host in cls.HOST_LIST:
                OneHeader["Host"] = Host
        if Origin is not None:
            if Origin in cls.ORIGIN_LIST:
                OneHeader["Origin"] = Origin
        if Referrer is not None:
            if Referrer in cls.REFERRER_LIST:
                OneHeader["Referer"] = Referrer
        return OneHeader
