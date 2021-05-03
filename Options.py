# coding = UTF-8


import KuGou


def Selector(MusicList: list):
    Buffer = None
    for i in MusicList:
        i: KuGou.Music
        if i.From == KuGou.Music.From_WangYiYun:
            Buffer = i
            break
    return Buffer


KuGou.Download(input("Music name : "), FilePath="./Music", LrcFile=True, DebugFlag=True, Selector=Selector)
