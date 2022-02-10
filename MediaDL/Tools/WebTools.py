#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @FileName  :WebTools.py
# @Time      :2022/1/2 13:06
# @Author    :Amundsen Severus Rubeus Bjaaland


import logging
import traceback
from typing import Union, Any
from urllib.parse import urlparse

import requests
import urllib3

_Logger = logging.getLogger(__name__)


def create_user_agent():
    """创建HTTP请求头中的User-Agent字段"""
    # TODO 将该函数的功能彻底实现
    return "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36" \
           " (KHTML, like Gecko) Chrome/91.0.4472.77 " \
           "Safari/537.36 Edg/91.0.864.37"


def get_response(url: str, params: dict = {}, header: dict = {},
                 retry: int = 5, method: str = "get", data: Any = None) -> Union[requests.Response, None]:
    """获取HTTP连接及数据

    :param url: 将要获取的HTTP连接的地址
    :param params: 将要获取的HTTP连接的负载数据
    :param header: 将要获取的HTTP连接的请求头
    :param retry: 出错重试的次数
    :param method: HTTP请求方法
    :param data: POST方法需要的数据
    :return: 获取的HTTP连接
    """
    method = method.lower()
    if "User-Agent" not in header:
        header["User-Agent"] = create_user_agent()
    for i in range(0, retry):
        try:
            if method == "get":
                response = requests.get(url, headers=header, params=params, data=data)
            elif method == "post":
                response = requests.post(url, headers=header, params=params, data=data)
            else:
                _Logger.warning(f"不支持的HTTP方法: {method}.")
                return None
        except urllib3.exceptions.ProtocolError:
            _Logger.warning("远程主机强迫关闭了一个现有的连接(请求过于频繁)")
        except requests.exceptions.ConnectionError:
            _Logger.warning("网络连接错误")
        except urllib3.exceptions.MaxRetryError:
            _Logger.warning("多次尝试连接失败")
        except urllib3.exceptions.NewConnectionError:
            _Logger.warning("无法创建新的连接")
        except TimeoutError:
            _Logger.warning("连接两方均没有反应")
        except Exception:
            _Logger.warning(f"未知的网络错误:\n{traceback.format_exc()}")
        else:
            url = urlparse(response.url)
            _Logger.info(f"成功从{url.scheme}://{url.netloc + url.path}处获取数据")
            return response
    else:
        _Logger.error(f"发生错误次数过多，该次请求将被取消")
        return None
