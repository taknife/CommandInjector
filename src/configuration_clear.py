#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2025/8/12 14:21
# @Author  : taknife
# @Project : CommandInjector
# @File    : configuration_clear.py

import re


class Configuration:
    # 初始化对象属性，主要属性为配置文件路径
    def __init__(self , config_file_path):
        self.__config_file_path = config_file_path
        self.__config_list = []

    # 读取配置文件，将配置文件格式化为列表
    def read_config_file(self):
        with open(self.__config_file_path, 'r', encoding="utf-8") as config_file:
            for config_line in config_file:
                self.__config_list.append(config_line)

    @staticmethod
    def config_module_template(module, config_file):
        module_template = {
            "address": r"\naddress\s+\S+\n.*?!",
            "interface": r"\ninterface\s+\S+\n.*?!",
            "service": r"\nservice\s+\S+\n.*?!",
            "policy": r"\npolicy\s.*?(?:deny|permit)\s\d+.*?(?=create-by\s\S+.*?|\npolicy|\Z)",
            "route": r"\nip\sroute.*?(?=[\n!])"
        }
        pattern = re.compile(module_template[module], re.DOTALL)
        blocks = pattern.findall(config_file.read())
        # for block in blocks:
        #     print(block.strip())
        return blocks

    # 查找相应区域的配置文件
    def search_module(self, module_name):
        with open(self.__config_file_path, 'r', encoding="utf-8") as config_file:
            match module_name:
                case "address":
                    blocks = self.config_module_template("address", config_file)
                case "interface":
                    blocks = self.config_module_template("interface", config_file)
                case "service":
                    blocks = self.config_module_template("service", config_file)
                case "policy":
                    blocks = self.config_module_template("policy", config_file)
                case "route":
                    blocks = self.config_module_template("route", config_file)
                case _:
                    pass
            # print(config_file.read())




if __name__ == '__main__':
    config = Configuration("../input/startup-0.cfg")
    config.search_module("interface")