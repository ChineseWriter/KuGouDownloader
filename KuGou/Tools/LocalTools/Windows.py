#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @FileName  :Windows.py
# @Time      :2021/5/9 9:02
# @Author    :Amundsen Severus Rubeus Bjaaland


from tkinter import *
import KuGou


def MusicSelector(Musics):
    Window = Tk()
    Window.title("选择要下载的歌曲")
    Window.resizable(0, 0)

    List = Listbox(Window, width=90, height=30, selectmode=MULTIPLE)
    List.pack()
    for OneMusic in Musics:
        OneMusic: KuGou.Music
        List.insert("end", OneMusic.From + ": " + OneMusic.Name + " - " + OneMusic.AuthorName)

    Buffer = []

    def GetList():
        ListLength = List.size()
        for i in range(ListLength):
            if List.select_includes(i):
                Buffer.append(Musics[i])
        Window.destroy()

    Button(Window, text="下载", command=GetList).pack()

    Window.mainloop()

    return Buffer


def MusicListViewer():
    pass
