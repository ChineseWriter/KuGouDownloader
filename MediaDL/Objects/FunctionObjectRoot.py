#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @FileName  :FunctionObjectRoot.py
# @Time      :2022/1/2 12:11
# @Author    :Amundsen Severus Rubeus Bjaaland


from abc import ABC, abstractmethod
from typing import List, Optional

from .CirculationObjectsRoot import Music


class Function(ABC):
    pass


class GetList(Function):
    def __init__(self) -> None:
        pass

    @abstractmethod
    def __call__(self, *args, **kwargs) -> List[Optional[Music]]:
        if "music_name" not in kwargs:
            raise TypeError("GetList() missing required argument 'select_name'")
        return []

    @abstractmethod
    def get_list(self, select_name: str) -> List[Optional[Music]]:
        return []
