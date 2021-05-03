#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @FileName  :setup.py
# @Time      :2021/5/2 11:21
# @Author    :Amundsen Severus Rubeus Bjaaland


from distutils.core import setup, Extension
from Cython.Build import cythonize

setup(name="Test", ext_modules=cythonize(
    Extension("Test", sources=["Test.pyx"], language='c', include_dirs=[], library_dirs=[], libraries=[],
              extra_compile_args=[], extra_link_args=[], )), language=3)
