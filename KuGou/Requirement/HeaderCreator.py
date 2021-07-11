#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @FileName  :HeaderCreator.py
# @Time      :2021/6/2 20:01
# @Author    :Amundsen Severus Rubeus Bjaaland


class UserAgentCreator(object):
    @classmethod
    def GetUserAgent(cls):
        return "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.77 " \
               "Safari/537.36 Edg/91.0.864.37"


class Header(object):
    HOST_KUGOU = "www.kugou.com"
    HOST_WANGYIYUN = "music.163.com"
    HOST_QQ = "y.qq.com"
    ORIGIN_KUGOU = "https://www.kugou.com"
    ORIGIN_WANGYIYUN = "https://music.163.com"
    ORIGIN_QQ = "https://y.qq.com"
    REFERRER_KUGOU_MAIN = "https://www.kugou.com/"
    REFERRER_WANGYIYUN_MAIN = "https://music.163.com/"
    REFERRER_QQ_MAIN = "https://y.qq.com/"
    REFERRER_KUGOU_SEARCH = "https://www.kugou.com/"
    REFERRER_KUGOU_GETINFO = "https://www.kugou.com/"
    REFERRER_KUGOU_SONGERINFO = "https://www.kugou.com/song/"
    REFERRER_WANGYIYUN_SEARCH = "https://music.163.com/"
    REFERRER_WANGYIYUN_GETINFO = "https://music.163.com/search/"
    REFERRER_QQ_SEARCH = "https://y.qq.com/"

    HOST_LIST = [HOST_KUGOU, HOST_WANGYIYUN, HOST_QQ]
    ORIGIN_LIST = [ORIGIN_KUGOU, ORIGIN_WANGYIYUN, ORIGIN_QQ]
    REFERRER_LIST = [
        REFERRER_KUGOU_SEARCH,
        REFERRER_WANGYIYUN_SEARCH,
        REFERRER_QQ_SEARCH,
        REFERRER_KUGOU_GETINFO,
        REFERRER_WANGYIYUN_GETINFO
    ]

    @classmethod
    def GetHeader(cls, Host=None, Origin=None, Referrer=None, UserAgent=None):
        OneHeader = {"User-Agent": UserAgentCreator.GetUserAgent()}
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
