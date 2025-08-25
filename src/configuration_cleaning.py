#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2025/8/12 14:21
# @Author  : taknife
# @Project : CommandInjector
# @File    : configuration_cleaning.py

import re


class Configuration:
    # 初始化对象属性，主要属性为配置文件路径
    def __init__(self , config_file_path):
        self.__config_file_path = config_file_path

    # 配置识别正则表达式模板匹配函数，用来匹配每一个部分的配置内容
    @staticmethod
    def __config_module_template(module, config_file):
        # 配置识别模板，用字典加正则表达式来进行匹配
        module_template = {
            "address": r"\naddress\s+\S+\n.*?!",
            "interface": r"\ninterface\s+\S+\n.*?!",
            "service": r"\nservice\s+\S+\n.*?!",
            "policy": r"\npolicy\s.*?(?:deny|permit)\s\d+.*?(?=create-by\s\S+.*?|\npolicy|\Z)",
            "route": r"\nip\sroute.*?(?=[\n!])"
        }
        pattern = re.compile(module_template[module], re.DOTALL)
        blocks = pattern.findall(config_file.read())
        return blocks

    # 查找相应区域的配置文件
    def search_module(self, module_name):
        with open(self.__config_file_path, 'r', encoding="utf-8") as config_file:
            match module_name:
                case "address":
                    return self.__config_module_template(module_name, config_file)
                case "interface":
                    return self.__config_module_template(module_name, config_file)
                case "service":
                    return self.__config_module_template(module_name, config_file)
                case "policy":
                    return self.__config_module_template(module_name, config_file)
                case "route":
                    return self.__config_module_template(module_name, config_file)
                case _:
                    return None
