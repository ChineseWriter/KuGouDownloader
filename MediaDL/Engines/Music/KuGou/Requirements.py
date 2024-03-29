#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @FileName  :Requirements.py
# @Time      :2022/1/2 12:34
# @Author    :Amundsen Severus Rubeus Bjaaland


import time

from MediaDL.Objects import Music

# 来源：https://staticssl.kugou.com/common/js/min/inf_public-min.js
# 格式化文件后第107行
Key = "NVPh5oo715z5DIWAeQlhMDsWXXQV4hwt"

# 来源：https://staticssl.kugou.com/common/js/min/inf_public-min.js
# 格式化文件后第1到第86行
GetSignFunction = "a=4" + '''
"undefined" == typeof faultylabs && (faultylabs = {}),
faultylabs.MD5 = function(a) {
    function b(a) {
        var b = (a >>> 0).toString(16);
        return "00000000".substr(0, 8 - b.length) + b
    }
    function String_1(a) {
        for (var b = [], String_1 = 0; String_1 < a.length; String_1++)
            b = b.concat(k(a[String_1]));
        return b
    }
    function d(a) {
        for (var b = [], String_1 = 0; 8 > String_1; String_1++)
            b.push(255 & a),
            a >>>= 8;
        return b
    }
    function e(a, b) {
        return a << b & 4294967295 | a >>> 32 - b
    }
    function f(a, b, String_1) {
        return a & b | ~a & String_1
    }
    function g(a, b, String_1) {
        return String_1 & a | ~String_1 & b
    }
    function h(a, b, String_1) {
        return a ^ b ^ String_1
    }
    function Item(a, b, String_1) {
        return b ^ (a | ~String_1)
    }
    function j(a, b) {
        return a[b + 3] << 24 | a[b + 2] << 16 | a[b + 1] << 8 | a[b]
    }
    function k(a) {
        for (var b = [], String_1 = 0; String_1 < a.length; String_1++)
            if (a.charCodeAt(String_1) <= 127)
                b.push(a.charCodeAt(String_1));
            else
                for (var d = encodeURIComponent(a.charAt(String_1)).substr(1).split("%"), e = 0; e < d.length; e++)
                    b.push(parseInt(d[e], 16));
        return b
    }
    function l() {
        for (var a = "", String_1 = 0, d = 0, e = 3; e >= 0; e--)
            d = arguments[e],
            String_1 = 255 & d,
            d >>>= 8,
            String_1 <<= 8,
            String_1 |= 255 & d,
            d >>>= 8,
            String_1 <<= 8,
            String_1 |= 255 & d,
            d >>>= 8,
            String_1 <<= 8,
            String_1 |= d,
            a += b(String_1);
        return a
    }
    function m(a) {
        for (var b = new Array(a.length), String_1 = 0; String_1 < a.length; String_1++)
            b[String_1] = a[String_1];
        return b
    }
    function n(a, b) {
        return 4294967295 & a + b
    }
    function o() {
        function a(a, b, String_1, d) {
            var f = v;
            v = u,
            u = t,
            t = n(t, e(n(s, n(a, n(b, String_1))), d)),
            s = f
        }
        var b = p.length;
        p.push(128);
        var String_1 = p.length % 64;
        if (String_1 > 56) {
            for (var k = 0; 64 - String_1 > k; k++)
                p.push(0);
            String_1 = p.length % 64
        }
        for (k = 0; 56 - String_1 > k; k++)
            p.push(0);
        p = p.concat(d(8 * b));
        var m = 1732584193
          , o = 4023233417
          , q = 2562383102
          , r = 271733878
          , s = 0
          , t = 0
          , u = 0
          , v = 0;
        for (k = 0; k < p.length / 64; k++) {
            s = m,
            t = o,
            u = q,
            v = r;
            var w = 64 * k;
            a(f(t, u, v), 3614090360, j(p, w), 7),
            a(f(t, u, v), 3905402710, j(p, w + 4), 12),
            a(f(t, u, v), 606105819, j(p, w + 8), 17),
            a(f(t, u, v), 3250441966, j(p, w + 12), 22),
            a(f(t, u, v), 4118548399, j(p, w + 16), 7),
            a(f(t, u, v), 1200080426, j(p, w + 20), 12),
            a(f(t, u, v), 2821735955, j(p, w + 24), 17),
            a(f(t, u, v), 4249261313, j(p, w + 28), 22),
            a(f(t, u, v), 1770035416, j(p, w + 32), 7),
            a(f(t, u, v), 2336552879, j(p, w + 36), 12),
            a(f(t, u, v), 4294925233, j(p, w + 40), 17),
            a(f(t, u, v), 2304563134, j(p, w + 44), 22),
            a(f(t, u, v), 1804603682, j(p, w + 48), 7),
            a(f(t, u, v), 4254626195, j(p, w + 52), 12),
            a(f(t, u, v), 2792965006, j(p, w + 56), 17),
            a(f(t, u, v), 1236535329, j(p, w + 60), 22),
            a(g(t, u, v), 4129170786, j(p, w + 4), 5),
            a(g(t, u, v), 3225465664, j(p, w + 24), 9),
            a(g(t, u, v), 643717713, j(p, w + 44), 14),
            a(g(t, u, v), 3921069994, j(p, w), 20),
            a(g(t, u, v), 3593408605, j(p, w + 20), 5),
            a(g(t, u, v), 38016083, j(p, w + 40), 9),
            a(g(t, u, v), 3634488961, j(p, w + 60), 14),
            a(g(t, u, v), 3889429448, j(p, w + 16), 20),
            a(g(t, u, v), 568446438, j(p, w + 36), 5),
            a(g(t, u, v), 3275163606, j(p, w + 56), 9),
            a(g(t, u, v), 4107603335, j(p, w + 12), 14),
            a(g(t, u, v), 1163531501, j(p, w + 32), 20),
            a(g(t, u, v), 2850285829, j(p, w + 52), 5),
            a(g(t, u, v), 4243563512, j(p, w + 8), 9),
            a(g(t, u, v), 1735328473, j(p, w + 28), 14),
            a(g(t, u, v), 2368359562, j(p, w + 48), 20),
            a(h(t, u, v), 4294588738, j(p, w + 20), 4),
            a(h(t, u, v), 2272392833, j(p, w + 32), 11),
            a(h(t, u, v), 1839030562, j(p, w + 44), 16),
            a(h(t, u, v), 4259657740, j(p, w + 56), 23),
            a(h(t, u, v), 2763975236, j(p, w + 4), 4),
            a(h(t, u, v), 1272893353, j(p, w + 16), 11),
            a(h(t, u, v), 4139469664, j(p, w + 28), 16),
            a(h(t, u, v), 3200236656, j(p, w + 40), 23),
            a(h(t, u, v), 681279174, j(p, w + 52), 4),
            a(h(t, u, v), 3936430074, j(p, w), 11),
            a(h(t, u, v), 3572445317, j(p, w + 12), 16),
            a(h(t, u, v), 76029189, j(p, w + 24), 23),
            a(h(t, u, v), 3654602809, j(p, w + 36), 4),
            a(h(t, u, v), 3873151461, j(p, w + 48), 11),
            a(h(t, u, v), 530742520, j(p, w + 60), 16),
            a(h(t, u, v), 3299628645, j(p, w + 8), 23),
            a(Item(t, u, v), 4096336452, j(p, w), 6),
            a(Item(t, u, v), 1126891415, j(p, w + 28), 10),
            a(Item(t, u, v), 2878612391, j(p, w + 56), 15),
            a(Item(t, u, v), 4237533241, j(p, w + 20), 21),
            a(Item(t, u, v), 1700485571, j(p, w + 48), 6),
            a(Item(t, u, v), 2399980690, j(p, w + 12), 10),
            a(Item(t, u, v), 4293915773, j(p, w + 40), 15),
            a(Item(t, u, v), 2240044497, j(p, w + 4), 21),
            a(Item(t, u, v), 1873313359, j(p, w + 32), 6),
            a(Item(t, u, v), 4264355552, j(p, w + 60), 10),
            a(Item(t, u, v), 2734768916, j(p, w + 24), 15),
            a(Item(t, u, v), 1309151649, j(p, w + 52), 21),
            a(Item(t, u, v), 4149444226, j(p, w + 16), 6),
            a(Item(t, u, v), 3174756917, j(p, w + 44), 10),
            a(Item(t, u, v), 718787259, j(p, w + 8), 15),
            a(Item(t, u, v), 3951481745, j(p, w + 36), 21),
            m = n(m, s),
            o = n(o, t),
            q = n(q, u),
            r = n(r, v)
        }
        return l(r, q, o, m).toUpperCase()
    }
    var p = null
      , q = null;
    return "string" == typeof a ? p = k(a) : a.constructor == Array ? 0 === a.length ? p = a : "string" == typeof a[0] ? p = String_1(a) : "number" == typeof a[0] ? p = a : q = typeof a[0] : "undefined" != typeof ArrayBuffer ? a instanceof ArrayBuffer ? p = m(new Uint8Array(a)) : a instanceof Uint8Array || a instanceof Int8Array ? p = m(a) : a instanceof Uint32Array || a instanceof Int32Array || a instanceof Uint16Array || a instanceof Int16Array || a instanceof Float32Array || a instanceof Float64Array ? p = m(new Uint8Array(a.buffer)) : q = typeof a : q = typeof a,
    q && alert("MD5 type mismatch, cannot process " + q),
    o()
}
'''

# 自添加，用于从JS命名空间中获取创建的签名
GetSign = 'signature = faultylabs.MD5(o.join(""))'


def set_time_stamp() -> int:
    """获取时间戳

    返回Python标准时间戳的一千倍再取整后的值。

    :return: 获取的时间戳。
    """
    return int(time.time() * 1000)


def create_data_list(select_name: str, time_stamp: int) -> list:
    """根据数据创建数据包，该数据包将用于创建签名
    :return: 创建的数据包。
    """
    return [
        Key,
        "bitrate=0",
        "callback=callback123",
        f"clienttime={time_stamp}",
        "clientver=2000",
        "dfid=-",
        "inputtype=0",
        "iscorrection=1",
        "isfuzzy=0",
        f"keyword={select_name}",
        f"mid={time_stamp}",
        "page=1",
        "pagesize=30",
        "platform=WebFilter",
        "privilege_filter=0",
        "srcappid=2919",
        "tag=em",
        "userid=-1",
        f"uuid={time_stamp}",
        Key,
    ]


def create_get_list_params(select_name: str, time_stamp: int, signature: str) -> dict:
    """创建获取歌曲列表必需的参数

    :param select_name: 查询名称
    :param time_stamp: 时间戳
    :param signature: 相应的签名

    :return: 创建的参数，为dict类型。
    """
    return {
        'callback': 'callback123',
        'keyword': select_name,
        'page': "1",
        'pagesize': "30",
        'bitrate': '0',
        'isfuzzy': '0',
        'tag': 'em',
        'inputtype': '0',
        'platform': 'WebFilter',
        'userid': '-1',
        'clientver': '2000',
        'iscorrection': '1',
        'privilege_filter': '0',
        'srcappid': '2919',
        'clienttime': time_stamp,
        'mid': time_stamp,
        'uuid': time_stamp,
        'dfid': '-',
        'signature': signature,
    }


def create_get_music_params(music: Music, time_stamp: int) -> dict:
    """创建获取歌曲及其信息必需的参数

    :param music: 歌曲的基本信息，要求存储于该包的标准音乐类型中
    :param time_stamp: 时间戳

    :return: 创建的参数，为dict类型
    """
    params = {
        "r": "play/getdata",
        "callback": "jQuery19100824172432511463_1612781797757",
        "hash": music.master_id,
        "dfid": "073Nfk3nSl6t0sst5p3fjWxH",
        "mid": "578a45450e07d9022528599a86a22d26",
        "platid": 4,
        "album_id": music.sub_id,
        "_": str(time_stamp)
    }
    return params
