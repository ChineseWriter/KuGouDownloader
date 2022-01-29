#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @FileName  :Options.py
# @Time      :2021/7/10 18:00
# @Author    :Amundsen Severus Rubeus Bjaaland


from MediaDL.Engines import MediaController

if __name__ == "__main__":
    Controller = MediaController()
    result_4 = Controller.select_music("我叫长安，你叫故里")
    result_5 = Controller.get_music_info(result_4[0])
    a = 0
