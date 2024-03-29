#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @FileName  :Validators.py
# @Time      :2021/12/25 18:40
# @Author    :Amundsen Severus Rubeus Bjaaland


import re
from abc import ABC, abstractmethod
from typing import Any
from urllib.parse import urlparse

from .WebList import SupportWebList


class Validator(ABC):
    def __set_name__(self, owner, name):
        self.private_name = '_' + name

    def __get__(self, obj, objtype=None):
        return getattr(obj, self.private_name)

    def __set__(self, obj, value):
        validated_value = self.validate(value)
        if validated_value is not None:
            setattr(obj, self.private_name, validated_value)
        else:
            raise ValueError("The verified value is None.")

    @abstractmethod
    def validate(self, value):
        return value


class OneOf(Validator):
    def __init__(self, *options):
        self.options = set(options)

    def validate(self, value):
        if value not in self.options:
            raise ValueError(f'Expected {value!r} to be one of {self.options!r}')
        return value


class SourceWebSite(OneOf):
    def __init__(self):
        super(SourceWebSite, self).__init__(*SupportWebList)


class String(Validator):
    def __init__(self, minsize=None, maxsize=None, predicate=None):
        self.minsize = minsize
        self.maxsize = maxsize
        self.predicate = predicate

    def validate(self, value):
        if not isinstance(value, str):
            raise TypeError(f'Expected {value!r} to be an str')
        if self.minsize is not None and len(value) < self.minsize:
            raise ValueError(f'Expected {value!r} to be no smaller than {self.minsize!r}')
        if self.maxsize is not None and len(value) > self.maxsize:
            raise ValueError(f'Expected {value!r} to be no bigger than {self.maxsize!r}')
        if self.predicate is not None and not self.predicate(value):
            raise ValueError(f'Expected {self.predicate} to be true for {value!r}')
        return value


class URL(String):
    def validate(self, value):
        super(URL, self).validate(value)
        try:
            urlparse(value)
        except Exception:
            raise ValueError(f'Expected {value!r} to be a url')
        return value


class Lyrics(String):
    __ten_microsecond_accuracy = re.compile(r"(\[\d\d:\d\d\.\d\d])(.*?)(##Finish)")
    __one_microsecond_accuracy = re.compile(r"(\[\d\d:\d\d\.\d\d\d])(.*?)(##Finish)")

    def validate(self, value):
        super(Lyrics, self).validate(value)
        if not value:
            return ""
        value = value.replace("\r", "").replace("\n\n", "\n")
        lyric_list = []
        for item in value.split("\n"):
            test_item = item + "##Finish"
            if self.__ten_microsecond_accuracy.match(test_item):
                lyric_list.append(item)
            elif self.__one_microsecond_accuracy.match(test_item):
                lyric_list.append(item)
            else:
                pass
        return "\n".join(lyric_list)


class Number(Validator):
    def __init__(self, minvalue=None, maxvalue=None):
        self.minvalue = minvalue
        self.maxvalue = maxvalue

    def validate(self, value):
        if not isinstance(value, (int, float)):
            raise TypeError(f'Expected {value!r} to be an int or float')
        if self.minvalue is not None and value < self.minvalue:
            raise ValueError(
                f'Expected {value!r} to be at least {self.minvalue!r}'
            )
        if self.maxvalue is not None and value > self.maxvalue:
            raise ValueError(
                f'Expected {value!r} to be no more than {self.maxvalue!r}'
            )
        return value


class Bytes(Validator):
    def validate(self, value):
        if not isinstance(value, bytes):
            raise TypeError(f'Expected {value!r} to be bytes')
        return value


class List(Validator):
    def __init__(self, content: Any = None) -> None:
        self.content = content

    def validate(self, value):
        if not isinstance(value, list):
            raise TypeError(f'Excepted {value!r} to be list')
        if self.content:
            for i in value:
                if not isinstance(i, self.content):
                    raise TypeError(f'Excepted items of {value!r} to be a {self.content}')
        return value
