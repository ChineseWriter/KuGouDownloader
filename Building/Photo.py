# 百度搜索：
# coding=utf-8
# 此模块相对于mainstart的路径：.\tool\Baidu\Select.py


import os  # 用于创建和删除文件夹
import threading  # 用于提高下载效率
import time  # 用于检测下载时间
from multiprocessing import Queue  # 用于线程之间的通信

import requests  # 用于获取网址后下载


class photo(object):
    '''百度图片爬取器'''

    def __init__(self):
        '''
        初始化这个类并运行：
            创建文件以存储PID
            创建队列
            获取用户信息（查询关键词、查询页数、查询方法）
            启动运行
        返回值：None
        '''
        self.__private_header = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102'}
        self.__private_PhotoSelfMakeUrlQueue = Queue()  # 创建队列（用于传递原始URL）
        self.__private_PhotoRequestsUrlQueue = Queue()  # 创建队列（用于传递得到的URL）
        print('图片下载器初始化中 . . .')
        print('请输入将要下载的图片的关键词。')
        self.__private_Photokeyword = str(input('查询关键词：'))  # 获取查询关键词
        print('请输入您要下载的页数。（每页30或31张图片,至少为2页）')
        self.__private_Photopagenumber = int(input('查询页数：'))  # 获取查询页数
        self.__private_Photofilepath = './Affair_%s' % self.__private_Photokeyword
        print('图片将临时保存于“affair_%s”文件夹中。' % self.__private_Photokeyword)

    def __private_MakeUrls(self):
        '''制作伪装URL'''
        try:
            print('查找图片中......')  # 给出执行信息
            for PhotoNum in range(30, 30 * self.__private_Photopagenumber + 30, 30):  # 循环‘页数’次
                self.__private_PhotoSelfMakeUrlQueue.put({
                    'tn': 'resultjson_com',
                    'ipn': 'rj',
                    'ct': 201326592,
                    'is': '',
                    'fp': 'result',
                    'queryWord': self.__private_Photokeyword,
                    'cl': 2,
                    'lm': -1,
                    'ie': 'utf-8',
                    'oe': 'utf-8',
                    'adpicid': '',
                    'st': -1,
                    'z': '',
                    'ic': 0,
                    'word': self.__private_Photokeyword,
                    's': '',
                    'se': '',
                    'tab': '',
                    'width': '',
                    'height': '',
                    'face': 0,
                    'istype': 2,
                    'qc': '',
                    'nc': 1,
                    'fr': '',
                    'pn': PhotoNum,
                    'rn': 30,
                    'gsm': '1e',
                    '1488942260214': ''
                })
        except Exception as AllError:  # 防止程序崩溃退出
            print(repr(AllError))  # 打印错误信息
        finally:
            self.__private_PhotoSelfMakeUrlQueue.put('CLOSE')  # 放入停止flag
            return None

    def __private_GetImaUrl(self):
        '''请求百度图片的地址'''
        try:
            url = 'https://image.baidu.com/search/index'  # 预先确定地址
            while True:
                if self.__private_PhotoSelfMakeUrlQueue.empty():  # 反复检查队列是否为空
                    pass  # 如果为空就跳过
                else:
                    PhotoGetText = self.__private_PhotoSelfMakeUrlQueue.get()  # 取出地址或停止flag
                    if PhotoGetText == 'CLOSE':  # 是停止flag就退出循环
                        break
                    else:
                        try:
                            response = requests.get(url, params=PhotoGetText, headers=self.__private_header,
                                                    timeout=(5, 16))
                            responsejson = response.json()  # 解析JSON
                            responsedata = responsejson.get('data')  # 找到存储图片真实网址的部分
                            for dictionary in responsedata:  # 反复取出网址
                                PhotoUrl = dictionary.get('thumbURL')  # 找到图片真实网址
                                if PhotoUrl == None:  # 确认它不为空
                                    pass
                                else:
                                    self.__private_PhotoRequestsUrlQueue.put(PhotoUrl)
                        except Exception as e:  # 防止程序崩溃退出
                            print(repr(e))
                        finally:
                            pass
        except Exception as AllError:  # 防止程序崩溃退出
            AllError = repr(AllError)
            print('哎呀，有三十张图片的网址我貌似读不懂啊。')
        finally:
            self.__private_PhotoRequestsUrlQueue.put('CLOSE')  # 放入停止flag
            return None

    def __private_dawnload(self):
        '''下载图片'''
        try:
            os.mkdir(self.__private_Photofilepath)  # 创建事务文件夹
        except FileExistsError:  # 已经存在就不创建
            pass
        finally:
            print('开始下载图片！')  # 告诉用户开始下载
        AllPhotoTime = time.process_time()  # 开始计时（总时间）
        PhotoAbnormal = 0  # 设置下载异常（超时计数器）
        num1 = 1  # 将要显示的计数器
        while True:
            Flag = True
            if self.__private_PhotoRequestsUrlQueue.empty():  # 检查队列是否为空
                pass
            else:
                url = self.__private_PhotoRequestsUrlQueue.get()  # 取出数据
                if url == 'CLOSE':  # 确认是否为停止flag
                    break
                else:
                    print('准备下载第%s张图片，' % (num1), end='')  # 告诉用户正在下载第几张图片
                    print('其网址为：%s。' % (url))  # 并附上网址
                    PhotoAbnormalTime = time.process_time()  # 开始计时（单次下载时间）
                    try:
                        GotPhoto = requests.get(url, headers=self.__private_header, timeout=(5, 16))  # 获取照片
                    except Exception as AllError:
                        AllError = repr(AllError)
                        PhotoAbnormal += 1
                        Flag = False
                    finally:
                        pass
                    if Flag == True:
                        PhotoPath = self.__private_Photofilepath + '\\' + self.__private_Photokeyword + str(
                            num1) + '.jpg'
                        file = open(PhotoPath, 'wb')  # 创建JPG文件
                        file.write(GotPhoto.content)  # 写入二进制数据
                        file.close()  # 关闭文件
                        PhotoAbnormalTime = time.process_time() - PhotoAbnormalTime  # 结束计时（单次下载时间）
                        num1 += 1  # 计数器加一
                        if PhotoAbnormalTime > 0.1:  # 检测是否超时
                            PhotoAbnormal += 1  # 将超时计数器加一
        AllPhotoTime = time.process_time() - AllPhotoTime  # 结束计时（总时间）
        print('共成功下载了%s张图片。' % (len(os.listdir(self.__private_Photofilepath))))
        print('共耗时%s秒' % (AllPhotoTime))
        print('有%s张图片下载时出现超时异常。' % (PhotoAbnormal))
        print('请将爬取的图片保存至另一个文件夹。')
        PhotoBuffer = input('保存好了吗？')
        try:
            os.remove(self.__private_Photofilepath)  # 删除文件夹
        except PermissionError:
            print('移除文件夹失败，请手动移除文件夹，以免下次使用时图片混合。')
        finally:
            return None

    def Tcontrol(self):
        '''函数式启动'''
        self.__private_PhotoThread1 = threading.Thread(target=self.__private_MakeUrls, name='BaiduPhotoMakeUrlThread')
        self.__private_PhotoThread2 = threading.Thread(target=self.__private_GetImaUrl,
                                                       name='BaiduPhotoGetPhotoUrlThread')
        self.__private_PhotoThread3 = threading.Thread(target=self.__private_dawnload,
                                                       name='BaiduPhotoDawnloadPhotoThread')
        self.__private_PhotoThread1.start()
        self.__private_PhotoThread2.start()
        self.__private_PhotoThread3.start()
        self.__private_PhotoThread3.join()
        print('Press "Enter" to continue . . .', end='')
        input()
        return None

    def Fcontrol(self):
        '''线程式启动'''
        self.__private_MakeUrls()
        self.__private_GetImaUrl()
        self.__private_dawnload()
        print('Press "Enter" to continue . . .', end='')
        input()
        return None


def Controller(Method):
    Photo = photo()
    if Method == 'T':
        Photo.Tcontrol()
    elif Method == 'F':
        Photo.Fcontrol()
    else:
        print('指令错误。')
    return None


if __name__ == '__main__':
    try:
        FirstThread = threading.Thread(target=Controller, args=('T',), name='BaiduPhotoMainThread')
        FirstThread.start()
        FirstThread.join()
    except Exception as AllError:
        print('程序内部出错！')
        print(repr(AllError))
        print('Press "Enter" to continue . . .', end='')
        input()
    finally:
        pass
