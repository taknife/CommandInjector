#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2025/8/25 14:30
# @Author  : taknife
# @Project : CommandInjector
# @File    : text_config_cleaning.py

import re

class TextConfig:
    def __init__(self, text_config_file_path):
        self.__text_config_file_path = text_config_file_path

    def check_text_config(self):
        with open(self.__text_config_file_path, 'r', encoding="utf-8") as text_file:
            module_template = r"<\[config_start\]>(.*?)<\[config_end\]>"
            pattern = re.compile(module_template, re.DOTALL)
            blocks = pattern.findall(text_file.read())
            return blocks
