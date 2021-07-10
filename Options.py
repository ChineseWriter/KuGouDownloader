#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @FileName  :Options.py
# @Time      :2021/7/10 18:00
# @Author    :Amundsen Severus Rubeus Bjaaland


import KuGou


def Selector(MusicList: list):
    Buffer = None
    for i in MusicList:
        i: KuGou.Music
        if i.From == KuGou.Music.From_WangYiYun:
            Buffer = i
            break
    return Buffer


# KuGou.Download(input("Music name : "), FilePath="./Music", LrcFile=True, DebugFlag=True, Selector=lambda x: x)
# Check = KuGou.CheckMusic("./Music")
# Check.DeleteVIPMusic(DebugFlag=True)
KuGou.Download("大鱼 周深", FilePath="./Music", LrcFile=True, DebugFlag=True,
               Selector=KuGou.Tools.LocalTools.MusicSelector)
