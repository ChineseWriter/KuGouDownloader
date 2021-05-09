#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @FileName  :Windows.py
# @Time      :2021/5/9 9:02
# @Author    :Amundsen Severus Rubeus Bjaaland


import tkinter
import KuGou


def MusicSelector(Musics):
    Window = tkinter.Tk()
    Window.title("选择要下载的歌曲")
    Window.resizable(0, 0)

    List = tkinter.Listbox(Window, width=90, height=30, selectmode=tkinter.MULTIPLE)
    List.pack()
    for OneMusic in Musics:
        OneMusic: KuGou.Music
        List.insert("end", OneMusic.From + ": " + OneMusic.Name + " - " + OneMusic.AuthorName)

    Buffer = []

    def GetList(event=None):
        ListLength = List.size()
        for i in range(ListLength):
            if List.select_includes(i):
                Buffer.append(Musics[i])
        Window.destroy()

    tkinter.Button(Window, text="下载", command=GetList).pack()
    Window.bind("<Key-Return>", GetList)

    Window.mainloop()

    return Buffer


def MusicNameGainer():
    Window = tkinter.Tk()
    Window.title("输入要下载的歌名")
    Window.resizable(0, 0)

    EntryVar = tkinter.StringVar()
    Entry = tkinter.Entry(Window, width=50, textvariable=EntryVar)
    Entry.pack()

    Text = []

    def GetText(event=None):
        Text.append(Entry.get())
        Window.destroy()

    tkinter.Button(Window, text="查找", command=GetText).pack()

    Window.bind("<Key-Return>", GetText)

    Window.mainloop()
    return Text[0]


def MusicListViewer():
    pass
