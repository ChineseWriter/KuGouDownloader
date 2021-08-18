#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @FileName  :PreservationManager.py
# @Time      :2021/6/27 12:38
# @Author    :Amundsen Severus Rubeus Bjaaland


import json
import os
import time
import KuGou

from ..MusicSheet import VERSION
from .MusicItem import MusicItem


class Manager(object):
    def __init__(self, FilePath: str = "./") -> None:
        assert os.path.exists(os.path.dirname(os.path.realpath(FilePath)))
        self.__Path = os.path.realpath(FilePath)

    @property
    def Path(self):
        return self.__Path

    @Path.setter
    def Path(self, FilePath: str):
        assert os.path.exists(os.path.dirname(os.path.realpath(FilePath)))
        self.__Path = os.path.realpath(FilePath)

    def JsonSave(self, MusicSheet) -> bool:
        Object = dict()
        Object["Info"] = {
            "SelfVersion": MusicSheet.Information.Version,
            "DownloaderVersion": MusicSheet.Information.DownloaderVersion,
            "MaxNumber": MusicSheet.Information.MaxNumber,
            "CreateTime": MusicSheet.Information.CreateTime,
            "RevisionTime": MusicSheet.Information.RevisionTime,
            "Creator": MusicSheet.Information.Creator
        }
        Buffer = []
        for OneMusic in MusicSheet.AllItem:
            OneMusic: MusicItem
            Buffer.append(
                {
                    "From": OneMusic.From,
                    "FileId": OneMusic.FileId,
                    "MusicName": OneMusic.Name,
                    "AlbumId": OneMusic.AlbumID,
                    "MusicId": OneMusic.MusicId
                }
            )
        Object["Musics"] = Buffer
        with open(self.__Path, "w", encoding="UTF-8") as File:
            json.dump(Object, File)
        return True

    def JsonLoad(self, MusicSheet) -> bool:
        if not os.path.exists(self.__Path):
            Object = {
                "Info": {
                    "Creator": ["Machine", ],
                    "MaxNumber": 1000,
                    "SelfVersion": VERSION,
                    "DownloaderVersion": KuGou.Version,
                    "CreateTime": time.time(),
                    "RevisionTime": time.time()
                },
                "Musics": []
            }
            with open(self.__Path, "w", encoding="UTF-8") as File:
                json.dump(Object, File)
        with open(self.__Path, "r", encoding="UTF-8") as File:
            Object = json.load(File)
        Info = Object["Info"]
        MusicList = Object["Musics"]
        Info: dict
        MusicSheet.Information.MaxNumber = Info["MaxNumber"]
        MusicSheet.Information.CreateTime = Info["CreateTime"]
        MusicSheet.Information.SetChange()
        for OneMusic in Info["Creator"]:
            MusicSheet.Information.AddCreator(OneMusic)
        MusicSheet.Clear()
        for OneMusicInfo in MusicList:
            OneMusicInfo: dict
            OneMusic = MusicItem(
                Name=OneMusicInfo.get("MusicName") if OneMusicInfo.get("MusicName") else "",
                From=OneMusicInfo.get("From") if OneMusicInfo.get("From") else "",
                FileId=OneMusicInfo.get("FileId") if OneMusicInfo.get("FileId") else "",
                AlbumID=OneMusicInfo.get("AlbumId") if OneMusicInfo.get("AlbumId") else "",
                MusicId=OneMusicInfo.get("MusicId") if OneMusicInfo.get("MusicId") else ""
            )
            MusicSheet.Append(OneMusic)
        return True

    def SqliteSave(self, MusicSheet) -> bool:
        pass
