#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @FileName  :Options.py
# @Time      :2021/7/10 18:00
# @Author    :Amundsen Severus Rubeus Bjaaland


import KuGou
import logging

logging.basicConfig(level=logging.INFO)

# from Building import QQ
# Result = KuGou.Download("朱砂", FilePath="./Music", LrcFile=True, Selector=KuGou.Tools.LocalTools.MusicSelector)
KuGou.ReDownload(FilePath="./Music")
