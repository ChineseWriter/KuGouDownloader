#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @FileName  :main.py
# @Time      :2021/7/10 14:44
# @Author    :Amundsen Severus Rubeus Bjaaland


import KuGou

# 下载歌曲
Result = KuGou.Download(KuGou.Tools.LocalTools.MusicNameGainer(), FilePath="./Music", LrcFile=True,  # DebugFlag=True,
                        Selector=KuGou.Tools.LocalTools.MusicSelector)

# 重新下载歌单中的歌曲
# KuGou.ReDownload(FilePath="./Music", LrcFile=True, DebugFlag=True)

# 检查歌曲文件夹中的歌曲
Check = KuGou.CheckMusic()
Check.DeleteLrcWithoutMusic()
Check.DeleteVIPMusic(DebugFlag=True)
Check.DeleteTooShortMusic(DebugFlag=True)

# 在命令行中等待退出
try:
    input("Finish .")
except Exception:
    pass
