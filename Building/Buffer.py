#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @FileName  :Buffer.py
# @Time      :2021/5/2 12:36
# @Author    :Amundsen Severus Rubeus Bjaaland


def __CleanData(self):
    Buffer = []
    for OneMusic in self.__GetData:
        OneMusicInfo = KuGou.Music()
        OneMusicInfo.From = KuGou.Music.From_WangYiYun
        OneMusicInfo.Name = OneMusic["name"]
        OneMusicInfo.FileId = OneMusic["id"]
        if OneMusic.get("al"):
            OneMusicInfo.AlbumID = str(OneMusic["al"]["id"])
            OneMusicInfo.PictureSource = OneMusic["al"]["picUrl"]
        else:
            OneMusicInfo.AlbumID = ""
        OneMusicInfo.AuthorName = OneMusic["ar"][0]["name"]
        OneMusicInfo.AuthorId = OneMusic["ar"][0]["id"]
        self.__GetLyrics(OneMusicInfo, str(OneMusicInfo.FileId))
        self.__GetMusicSource(OneMusicInfo, OneMusicInfo.FileId)
        Buffer.append(OneMusicInfo)
    self.__CleanedData = Buffer
    return None


def __GetLyrics(self, OneMusic, MusicId):
    OneMusic: KuGou.Music
    try:
        Params = {"id": str(MusicId), "lv": -1, "tv": -1, "csrf_token": ""}
        Params = json.dumps(Params)
        Params = self.KeyCreator.GetParams(Params)
        Response = requests.post(self.LyricUrl, data=Params, headers=self.__Headers)
        JsonData = Response.json()
        if JsonData["code"] != 200:
            raise Exception()
        if JsonData.get("nolyric"):
            OneMusic.Lyrics = "[00:00.00]纯音乐，请欣赏。"
        else:
            OneMusic.Lyrics = JsonData['lrc']['lyric']
    except Exception:
        OneMusic.Lyrics = "[00:00.00]纯音乐，请欣赏。"
    finally:
        return None


def __GetMusicSource(self, OneMusic, MusicId):
    OneMusic: KuGou.Music
    try:
        Params = {"ids": [int(MusicId)], "br": 128000, "csrf_token": ""}
        Params = json.dumps(Params)
        Params = self.KeyCreator.GetParams(Params)
        Response = requests.post(self.MusicSourceUrl, data=Params, headers=self.__Headers)
        JsonData = Response.json()
        OneMusic.MusicSource = JsonData['data'][0]['url']
    except Exception:
        pass
    finally:
        return None
