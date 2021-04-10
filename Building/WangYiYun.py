# coding  = UTF-8
# 该文件等待重构 . . .


import base64
import random
import os
from binascii import hexlify
from Crypto.Cipher import AES
import json
import requests


class GetMusic:
    def __init__(self):
        self.key = GetParamsAndEncSecKey()
        self.headers = {
            'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                          "(KHTML, like Gecko) Chrome/89.0.4389.114 Safari/537.36 Edg/89.0.774.68",
            'Referer': 'http://music.163.com/'
        }
        self.session = requests.Session()
        self.session.headers = self.headers
        self.conmment_url = 'https://music.163.com/weapi/v1/resource/comments/R_SO_4_{}?csrf_token='  # 评论
        self.lyric_url = 'https://music.163.com/weapi/song/lyric?csrf_token='  # 歌词
        self.music_url = 'https://music.163.com/weapi/song/enhance/player/url?csrf_token='  # 歌曲
        self.url = 'https://music.163.com/weapi/cloudsearch/get/web?csrf_token='  # 搜索歌曲列表，无歌曲链接

    def get_params_and_encSecKey(self, song=None):
        ''' 获取什么就返回所需要两个参数 1. 歌曲 2. 歌词 3. 评论  默认 4. 搜索的歌曲列表 :param song: :return: '''
        if isinstance(song, int):
            data = {"ids": [song], "br": 128000, "csrf_token": ""}
        elif isinstance(song, str) and song.isdigit():
            data = {"id": song, "lv": -1, "tv": -1, "csrf_token": ""}
        elif song is None:
            data = {}
        else:
            data = {
                "hlpretag": "",
                "hlposttag": "",
                "s": song,
                "type": "1",
                "offset": "0",
                "total": "true",
                "limit": "30",
                "csrf_token": ""
            }
        song = json.dumps(data)
        data = self.key.get(song)
        return data

    def get_music_list_info(self, name):
        ''' 获取歌曲详情：歌名+歌曲id+作者 :param name: :return: '''
        data = self.get_params_and_encSecKey(name)
        res = self.session.post(self.url, data=data)  # 歌曲
        song_info = res.json()['result']['songs']
        for song in song_info:
            song_name = song['name']
            song_id = song['id']
            songer = song['ar'][0]['name']
            print(song_name, '\t', song_id, '\t', songer)
            self.get_music_url(song_id)
            self.get_music_lyric(song_id)
            self.get_music_comment(song_id)
            break

    def get_music_url(self, id):
        ''' 获取歌曲URL链接 :param id: :return: '''
        data = self.get_params_and_encSecKey(id)
        res = self.session.post(self.music_url, data=data)
        song_url = res.json()['data'][0]['url']
        print(song_url)

    def get_music_lyric(self, id_str):
        ''' 获取歌词 :param id_str: :return: '''
        data = self.get_params_and_encSecKey(str(id_str))
        res = self.session.post(self.lyric_url, data=data)
        lyric = res.json()['lrc']['lyric']
        print(lyric)

    def get_music_comment(self, song_id):
        ''' 获取歌曲评论: 评论人+内容+头像 :param song_id: :return: '''
        data = self.get_params_and_encSecKey()
        comment = self.session.post(self.conmment_url.format(str(song_id)), data=data)
        com_list = comment.json()['hotComments']
        for com in com_list:
            content = com['content']
            nickname = com['user']['nickname']
            user_img = com['user']['avatarUrl']
            print(nickname, '!!!!' + content + '!!!!', user_img)


class GetParamsAndEncSecKey:
    def __init__(self):
        self.txt = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'
        self.i = ''.join(random.sample(self.txt, 16))  # 16为随机数
        self.i = hexlify(os.urandom(16))[:16].decode('utf -8')  # 16为随机数bytes
        self.first_key = '0CoJUm6Qyw8W8jud'

    def get(self, song):
        ''' 获取加密的参数 params是两次加密的 :param song: :return: '''
        res = self.get_params(song, self.first_key)
        params = self.get_params(res, self.i)
        encSecKey = self.get_encSecKey()
        return {'params': params, 'encSecKey': encSecKey}

    def get_params(self, data, key):
        ''' 获得params,加密字符长度要是16的倍数 :param data: :param key: :return: '''
        iv = '0102030405060708'
        num = 16 - len(data) % 16
        data = data + num * chr(num)  # 补足
        cipher = AES.new(key.encode(), AES.MODE_CBC, iv.encode())
        result = cipher.encrypt(data.encode())
        result_str = base64.b64encode(result).decode('utf-8')
        return result_str

    def get_encSecKey(self):
        ''' 获取encSecKey，256个字符串
        hexlify--->转换为btyes类型
        pow--->两个参数是幂,三个参数是先幂在取余
        format(rs, 'x').zfill(256)-->256位的16进制 :return: '''
        enc_key = '010001'
        modulus = '00e0b509f6259df8642dbc35662901477df22677ec152b5ff68ace' \
                  '615bb7b725152b3ab17a876aea8a5aa76d2e417629ec4ee341f56135fccf695' \
                  '280104e0312ecbda92557c93870114af6c9d05c4f7f0c3685b7a46bee255932575c' \
                  'ce10b424d813cfe4875d3e82047b97ddef52741d546b8e289dc6935b3ece0462db0a22b8e7'
        rs = pow(int(hexlify(self.i[::-1].encode('utf-8')), 16), int(enc_key, 16), int(modulus, 16))
        return format(rs, 'x').zfill(256)


if __name__ == '__main__':
    Music = GetMusic()
    Music.get_music_list_info("所念皆星河 CMJ")
