#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @FileName  :Requirement.py
# @Time      :2022/1/30 13:14
# @Author    :Amundsen Severus Rubeus Bjaaland
import time


def create_params(select_name: str, page_number: int) -> dict:
    return {
        "tn": "resultjson_com",
        "logid": "10369733230352241675",
        "ipn": "rj",
        "ct": "201326592",
        "is": "",
        "fp": "result",
        "fr": "",
        "word": select_name,
        "cg": "brand",
        "queryWord": select_name,
        "cl": "2",
        "lm": "-1",
        "ie": "utf-8",
        "oe": "utf-8",
        "adpicid": "",
        "st": "",
        "z": "",
        "ic": "",
        "hd": "",
        "latest": "",
        "copyright": "",
        "s": "",
        "se": "",
        "tab": "",
        "width": "",
        "height": "",
        "face": "",
        "istype": "",
        "qc": "",
        "nc": "1",
        "expermode": "",
        "nojc": "",
        "isAsync": "",
        "pn": str(page_number * 30),
        "rn": "30",
        # "gsm": "50000001e",
        str(time.time()).replace(".", "")[:13]: ""
    }
