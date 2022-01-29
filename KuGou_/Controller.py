#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @FileName  :Controller.py
# @Time      :2021/8/18 12:11
# @Author    :Amundsen Severus Rubeus Bjaaland
"""集成该包的功能，提供下载函数，下载和歌单管理函数，根据歌单重新下载函数"""

# 导入所需要的库
import copy
import inspect
import logging
import os
import traceback

from .Tools import GetMusicInfo, GetMusicList
from .Tools import Music
from .Tools import MusicList

# 创建一个日志记录器
Logger = logging.getLogger(__name__)


def ReDownload(MusicSheetPath: str = "./KuGouMusicList.json", FilePath: str = "./",
               LrcFile: bool = True, ForceReplace: bool = False) -> None:
    """对歌单内的歌曲进行重新下载操作

    :param MusicSheetPath: 歌单文件路径，该路径必须存在，为str类型
    :param FilePath: 歌曲文件下载路径(将保存的目录)，该路径必须存在，为str类型
    :param LrcFile: 是否另存歌词文件，为bool类型
    :param ForceReplace: 是否强制替换已存在的歌曲文件，为bool类型
    :return: 无返回值
    """
    # 尝试创建歌曲文件夹(歌曲保存路径)，若存在则不创建
    try:
        os.mkdir(FilePath)
        Logger.debug("Create music file folder successfully .")
    except FileExistsError:
        Logger.debug("The music file folder has been created .")
    # 初始化一个歌单对象(MusicList)
    Musics = MusicList()
    # 加载歌单至歌单对象
    Musics.Load(MusicList.Json, MusicSheetPath)
    # 开始重新下载歌单内的歌曲
    Logger.info("Download the songs in the song list again .")
    Counter = 1
    for OneMusic in Musics.AllItem:
        OneMusic: Music
        Logger.info(f"This is the {Counter} Item ({OneMusic.Name}).")
        GetMusicInfo(OneMusic).Save(FilePath, LrcFile, ForceReplace)
        Counter += 1
    return None


def Download(MusicName: str, Selector=None, MusicSheetPath: str = "./KuGouMusicList.json", FilePath: str = "./",
             LrcFile: bool = False, ForceReplace: bool = False) -> list:
    """根据传入参数下载对应歌曲并保存信息至歌单中

    :param MusicName: 歌曲名称，为str类型
    :param Selector: 根据某种对应关系选择歌曲的函数，该函数输入一个以Music为元素的列表，输出其中一个或多个Music，为None或func类型
    :param MusicSheetPath: 歌单文件路径，该路径必须存在，为str类型
    :param FilePath: 歌曲文件下载路径(将保存的目录)，该路径必须存在，为str类型
    :param LrcFile: 是否另存歌词文件，为bool类型
    :param ForceReplace: 是否强制替换已存在的歌曲文件，为bool类型
    :raise ValueError: MusicName参数不为str类型，Selector参数不为func类型，Selector返回值不为list类型
    :return: 返回下载的歌曲(以Music为元素的列表)
    """
    # 尝试创建歌曲文件夹(歌曲保存路径)，若存在则不创建
    try:
        os.mkdir(FilePath)
        Logger.debug("Create music file folder successfully .")
    except FileExistsError:
        Logger.debug("The music file folder has been created .")
    # 检查是否指定选择器
    if Selector is None:
        Logger.info("The default song selector will be used .")

        # 若不指定，则使用默认选择器
        def Selector(x):
            # 返回列表第一项，即KuGou网站的第一个搜索结果
            return list(x[0])
    # 检查选择器是否为一个函数
    if not inspect.isfunction(Selector):
        Logger.critical("The Argument 'Selector' must be a function (Executable) .")
        raise ValueError("The Argument 'Selector' must be a function (Executable) .")
    if not MusicName:
        Logger.critical("The Argument 'data' must be a string (Not empty) .")
        raise ValueError("The Argument 'data' must be a string (Not empty) .")
    # 获取歌曲列表
    Result = GetMusicList(MusicName)
    # 获取Selector函数的返回值
    Result = Selector(Result)
    # 检查Selector函数的返回值(检查返回值是否为list)
    if not isinstance(Result, list):
        Logger.critical("The return value of the Function_1 'Selector' is incorrect .")
        raise ValueError("The return value of the Function_1 'Selector' is incorrect .")
    # 检查Selector函数的返回值(检查返回值是否为空)
    if len(Result) == 0:
        Logger.info("The return value of the Function_1 'Selector' is a empty list .")
        return None
    # 对每个歌曲进行下载
    Buffer = []
    Counter = 1  # 下载个数计数器
    for OneMusic in Result:
        OneMusic: Music  # 类型标注
        # 信息输出
        Logger.info(f"This is the {Counter} Item ({OneMusic.Name}).")
        # 下载歌曲并获取返回值(下载是否成功)
        SuccessFlag = DownloadMusic(OneMusic, FilePath, ForceReplace, LrcFile)
        if SuccessFlag:
            Buffer.append(SuccessFlag)
        Counter += 1
    # 获取下载好的歌曲组成的列表(list)
    Result = copy.deepcopy(Buffer)
    # 对Buffer该变量进行更新(清空)
    Buffer = []  # Buffer.clear()
    # 删除Result中的None(空值)
    for OneMusic in Result:
        if OneMusic is None:
            continue
        Buffer.append(OneMusic)
    # 初始化一个歌单对象(MusicList)
    Musics = MusicList()
    # 加载歌单至歌单对象
    Musics.Load(MusicList.Json, MusicSheetPath)
    # 添加歌曲到歌单中
    for OneMusic in Result:
        Musics.Append(OneMusic)
    # 保存该歌单
    Musics.Save(MusicList.Json, MusicSheetPath)
    return Result  # 返回该列表


def DownloadMusic(MusicItem: Music, FilePath: str = "./", ForceReplace: bool = False, LrcFile: bool = True) -> Music:
    """根据传入参数下载对应歌曲

    :param MusicItem: 根据将要下载的歌曲的对应网站的部分歌曲信息，为KuGou.Music类型
    :param FilePath: 歌曲文件下载路径(将保存的目录)，该路径必须存在，为str类型
    :param ForceReplace: 是否强制替换已存在的歌曲文件，为bool类型
    :param LrcFile: 是否另存歌词文件，为bool类型
    :return: 返回下载的歌曲，为KuGou.Music类型，与MusicItem参数的Object内存地址相同
    """
    # 获取歌曲信息，若失败则打印错误信息
    Logger.info(f"The name of the song to be downloaded: {MusicItem.Name}")
    try:
        Result = GetMusicInfo(MusicItem)
    except Exception:
        Logger.warning("获取歌曲信息失败：")
        traceback.print_exc()
        return None
    # 保存歌曲及歌曲信息
    SuccessFlag = Result.Save(FilePath, LrcFile, ForceReplace)
    if not SuccessFlag:
        Logger.warning("保存歌曲及其信息失败。")
        return None
    # 打印日志
    Logger.debug("Successful !")
    Logger.info(
        f"歌曲详细信息：歌曲名：{Result.Name}；所属专辑：{Result.Album}；"
        f"演唱者：{Result.Author.FreshNames}；来源网站：{Result.From}"
    )
    return Result
