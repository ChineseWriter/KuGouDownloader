# cython: language_level=3
#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @FileName  :Test.py
# @Time      :2021/5/2 11:21
# @Author    :Amundsen Severus Rubeus Bjaaland


cimport cython

@cython.boundscheck(False)
@cython.wraparound(False)
cdef int _Sum_(int a, int b):
    return a + b

def Sum(a, b):
    return _Sum_(a, b)
