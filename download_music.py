#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @FileName  :download_music.py
# @Time      :2022/2/7 13:07
# @Author    :Amundsen Severus Rubeus Bjaaland

import os
import sys

if os.getcwd() not in sys.path:
    sys.path.append(os.getcwd())

from MediaDL.Tools.LocalTools import music_cmd_downloader
from MediaDL.Tools import set_log

if __name__ == "__main__":
    set_log()
    music_cmd_downloader()
