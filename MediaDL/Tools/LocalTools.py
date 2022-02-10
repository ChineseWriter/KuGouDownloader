#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @FileName  :LocalTools.py
# @Time      :2022/1/8 19:16
# @Author    :Amundsen Severus Rubeus Bjaaland


import logging
import os
import re
import time
from logging import handlers

from prettytable import PrettyTable

_Logger = logging.getLogger(__name__)
_INVALID_CHAR_LIST = ["*", ".", '"', "'", "/", "\\", "[", "}", ":", ";", "|", ",", "<", ">", "?"]
_INVALID_PATTERN_LIST = ["<.*?>", "</.*?>"]


class Printer(object):
    DISPLAY_MODE_DEFAULT = "0"
    DISPLAY_MODE_HIGHLIGHT = "1"
    DISPLAY_MODE_NOT_BOLD = "22"
    DISPLAY_MODE_UNDERLINE = "4"
    DISPLAY_MODE_NON_UNDERLINE = "24"
    DISPLAY_MODE_TWINKLE = "5"
    DISPLAY_MODE_NON_TWINKLE = "25"
    DISPLAY_MODE_REVERSE_DISPLAY = "7"
    DISPLAY_MODE_NON_REFLEXIVE = "27"
    FOREGROUND_BLACK = "30"
    FOREGROUND_RED = "31"
    FOREGROUND_GREEN = "32"
    FOREGROUND_YELLOW = "33"
    FOREGROUND_BLUE = "34"
    FOREGROUND_MAGENTA = "35"
    FOREGROUND_CYAN = "36"
    FOREGROUND_WHITE = "37"
    BACKGROUND_BLACK = "40"
    BACKGROUND_RED = "41"
    BACKGROUND_GREEN = "42"
    BACKGROUND_YELLOW = "43"
    BACKGROUND_BLUE = "44"
    BACKGROUND_MAGENTA = "45"
    BACKGROUND_CYAN = "46"
    BACKGROUND_WHITE = "47"

    @classmethod
    def print_str(cls, content, display_mode="0", foreground="37", background="40"):
        return f"\033[{display_mode};{foreground};{background}m{content}\033[0m"


def set_log(level: int = logging.WARNING) -> bool:
    """设置全局日志格式"""
    try:
        os.mkdir("logs")
    except FileExistsError:
        pass
    # 获取该包的根记录器
    package_logger = logging.getLogger("MediaDL")  # 获取记录器
    package_logger.setLevel(logging.DEBUG)  # 设置记录级别为DEBUG
    # 设置记录信息的格式
    formatter = logging.Formatter("[%(asctime)s](%(levelname)s)%(name)s: %(message)s")
    # 初始化控制台输出处理器
    stream_handler = logging.StreamHandler()  # 创建一个控制台输出处理器
    stream_handler.setLevel(logging.INFO)  # 设置输出级别为INFO
    stream_handler.setFormatter(formatter)  # 设置输出的格式
    # 初始化文件输出处理器
    file_handler = handlers.TimedRotatingFileHandler("./logs/程序日志.log",
                                                     when="D",
                                                     encoding="UTF-8",
                                                     backupCount=5
                                                     )  # 创建一个文件输出处理器
    file_handler.setLevel(level)  # 设置输出级别为参数指定级别
    file_handler.setFormatter(formatter)  # 设置输出的格式
    # 添加处理器到记录器
    package_logger.addHandler(stream_handler)
    package_logger.addHandler(file_handler)
    return True


def replace(string: str) -> str:
    for i in _INVALID_PATTERN_LIST:
        string = re.sub(i, "", string)
    for i in _INVALID_CHAR_LIST:
        string = string.replace(i, "")
    return string


def music_cmd_downloader():
    from MediaDL.Engines import MediaController
    controller = MediaController()
    print(Printer.print_str("开始运行",
                            foreground=Printer.FOREGROUND_RED,
                            background=Printer.BACKGROUND_BLUE
                            ))
    music_name = input("输入你要下载的歌曲名：")
    if not music_name:
        _Logger.debug("未输入任何查询字符导致退出程序")
        print("您没有输入任何字符，下载器即将退出 . . .")
        input("按'Enter'键以退出 . . .")
        return None
    print("查找中，请稍等 . . .")
    select_start_time = time.time()
    select_result_list = controller.select_music(music_name)
    select_finish_time = time.time()
    print(f"查找完成！耗时约{round(select_finish_time - select_start_time, 2)}秒。")
    _Logger.debug(
        f"该次查询耗时{select_finish_time - select_start_time}秒，"
        f"共有{len(select_result_list)}个结果"
    )
    counter = 1
    print_table = PrettyTable()
    print_table.field_names = ("编号", "名称", "演唱者", "专辑", "来源网站")
    for one_music in select_result_list:
        print_table.add_row((counter,
                             one_music.name,
                             one_music.singer_list.name_list,
                             one_music.album,
                             one_music.source_site
                             ))
        counter += 1
    print(print_table)
    id = input("选择您要下载的歌曲的编号（若要下载多首，请用“，”隔开）：")
    id_list = [int(one_id) for one_id in re.findall("\d+", id)]
    if not id_list:
        _Logger.debug(f"未选择任何歌曲导致退出程序")
        print("您没有选择任何歌曲，下载器即将退出 . . .")
        input("按'Enter'键以退出 . . .")
        return None
    id_buffer = []
    for one_id in id_list:
        if 0 < one_id <= len(select_result_list):
            id_buffer.append(one_id)
    print("开始下载歌曲，请稍等 . . .")
    download_start_time = time.time()
    music_list = [controller.get_music_info(select_result_list[one_id - 1]) for one_id in id_buffer]
    download_finish_time = time.time()
    print(f"歌曲下载完成！耗时约{round(download_finish_time - download_start_time, 2)}秒")
    _Logger.debug(f"该次下载{len(music_list)}首歌曲共耗时{download_finish_time - download_start_time}秒")
    for one_music in music_list:
        one_music.save("./Music")
    print(f"歌曲保存完成！")
    input("按'Enter'键以退出 . . .")
    return None
