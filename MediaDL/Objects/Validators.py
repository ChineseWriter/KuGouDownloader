#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @FileName  :Validators.py
# @Time      :2021/12/25 18:40
# @Author    :Amundsen Severus Rubeus Bjaaland


from abc import ABC, abstractmethod
from urllib.parse import urlparse
from typing import Any

from .WebList import SupportWebList


class Validator(ABC):
    def __set_name__(self, owner, name):
        self.private_name = '_' + name

    def __get__(self, obj, objtype=None):
        return getattr(obj, self.private_name)

    def __set__(self, obj, value):
        self.validate(value)
        setattr(obj, self.private_name, value)

    @abstractmethod
    def validate(self, value):
        pass


class OneOf(Validator):
    def __init__(self, *options):
        self.options = set(options)

    def validate(self, value):
        if value not in self.options:
            raise ValueError(f'Expected {value!r} to be one of {self.options!r}')


class SourceWebSite(OneOf):
    def __init__(self):
        super(SourceWebSite, self).__init__(SupportWebList)


class String(Validator):
    def __init__(self, minsize=None, maxsize=None, predicate=None):
        self.minsize = minsize
        self.maxsize = maxsize
        self.predicate = predicate

    def validate(self, value):
        if not isinstance(value, str):
            raise TypeError(f'Expected {value!r} to be an str')
        if self.minsize is not None and len(value) < self.minsize:
            raise ValueError(
                f'Expected {value!r} to be no smaller than {self.minsize!r}'
            )
        if self.maxsize is not None and len(value) > self.maxsize:
            raise ValueError(
                f'Expected {value!r} to be no bigger than {self.maxsize!r}'
            )
        if self.predicate is not None and not self.predicate(value):
            raise ValueError(
                f'Expected {self.predicate} to be true for {value!r}'
            )


class URL(String):
    def validate(self, value):
        if not isinstance(value, str):
            raise TypeError(f'Expected {value!r} to be an str')
        if self.minsize is not None and len(value) < self.minsize:
            raise ValueError(
                f'Expected {value!r} to be no smaller than {self.minsize!r}'
            )
        if self.maxsize is not None and len(value) > self.maxsize:
            raise ValueError(
                f'Expected {value!r} to be no bigger than {self.maxsize!r}'
            )
        if self.predicate is not None and not self.predicate(value):
            raise ValueError(f'Expected {self.predicate} to be true for {value!r}')
        try:
            urlparse(value)
        except Exception:
            raise ValueError(f'Expected {value!r} to be a url')



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


class Bytes(Validator):
    def validate(self, value):
        if not isinstance(value, bytes):
            raise TypeError(f'Expected {value!r} to be bytes')


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
