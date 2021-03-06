#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @FileName  :WangYiYunAES.py
# @Time      :2021/8/19 19:32
# @Author    :Amundsen Severus Rubeus Bjaaland


"""爬取网易云网站时需要的密钥构造函数(采用AES的CBC模式加密)。"""

# 导入所需要的库
import random
import base64
import os
from binascii import hexlify

# Python3安装Crypto是: pip3 install pycryptodome
from Crypto.Cipher import AES


class AESKey(object):
    """网易云音乐网站所需AES密钥构造"""

    def __init__(self) -> None:
        self.Text = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'
        self.Item = ''.join(random.sample(self.Text, 16))  # 16为随机数
        self.Item = hexlify(os.urandom(16))[:16].decode('utf -8')  # 16为随机数bytes
        self.FirstKey = '0CoJUm6Qyw8W8jud'

    def GetParams(self, MusicName: str) -> dict:
        """获取加密的参数

        :param MusicName: 搜索的歌曲名
        :return: params是两次加密的，encSecKey是密钥，由上述两变量组成一个dict
        """
        ResKey = self.__CreateParams(MusicName, self.FirstKey)
        Params = self.__CreateParams(ResKey, self.Item)
        encSecKey = self.__CreateKey()
        return {'params': Params, 'encSecKey': encSecKey}

    def __CreateParams(self, data: str, key: str) -> str:
        """创建密钥,加密字符长度要是16的倍数

        :param data:
        :param key:
        :return:
        """
        iv = '0102030405060708'
        num = 16 - len(data) % 16
        data = data + num * chr(num)  # 补足
        cipher = AES.new(key.encode(), AES.MODE_CBC, iv.encode())
        result = cipher.encrypt(data.encode())
        result_str = base64.b64encode(result).decode('utf-8')
        return result_str

    def __CreateKey(self):
        """ 获取encSecKey，256个字符串
        hexlify--->转换为bytes类型
        pow--->两个参数是幂,三个参数是先幂在取余
        format(rs, 'x').zfill(256)-->256位的16进制 :return: """
        enc_key = '010001'
        modulus = '00e0b509f6259df8642dbc35662901477df22677ec152b5ff68ace' \
                  '615bb7b725152b3ab17a876aea8a5aa76d2e417629ec4ee341f56135fccf695' \
                  '280104e0312ecbda92557c93870114af6c9d05c4f7f0c3685b7a46bee255932575c' \
                  'ce10b424d813cfe4875d3e82047b97ddef52741d546b8e289dc6935b3ece0462db0a22b8e7'
        rs = pow(int(hexlify(self.Item[::-1].encode('utf-8')), 16), int(enc_key, 16), int(modulus, 16))
        return format(rs, 'x').zfill(256)

