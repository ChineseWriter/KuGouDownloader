#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @FileName  :main.py
# @Time      :2021/7/10 14:44
# @Author    :Amundsen Severus Rubeus Bjaaland


import KuGou

Result = KuGou.Download(KuGou.Tools.LocalTools.MusicNameGainer(), FilePath="./Music", LrcFile=True,  # DebugFlag=True,
                        Selector=KuGou.Tools.LocalTools.MusicSelector)
# KuGou.ReDownload(FilePath="./Music", LrcFile=True, DebugFlag=True)
Check = KuGou.CheckMusic()
Check.DeleteLrcWithoutMusic()
Check.DeleteVIPMusic(DebugFlag=True)
Check.DeleteTooShortMusic(DebugFlag=True)

try:
    input("Finish .")
except Exception:
    pass