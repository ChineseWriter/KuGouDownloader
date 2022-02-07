#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @FileName  :Options.py
# @Time      :2021/7/10 18:00
# @Author    :Amundsen Severus Rubeus Bjaaland


from MediaDL.Engines import MediaController

if __name__ == "__main__":
    Controller = MediaController()
    result_1 = Controller.select_music("吹灭小山河 国风堂、司南")
    result_2 = Controller.get_music_info(result_1[0])
    result_3 = result_2.save("./Music")
