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

    # 查找相应区域的配置文件
    def search_module(self, module_name):
        with open(self.__config_file_path, 'r', encoding="utf-8") as config_file:
            match module_name:
                case "address":
                    address_pattern = re.compile(r"\naddress\s+\S+\n.*?!", re.DOTALL)
                    address_blocks = address_pattern.findall(config_file.read())
                    for block in address_blocks:
                        print(block.strip())  # 去除前后空白字符
                case "interface":
                    interface_pattern = re.compile(r'\ninterface\s+\S+\n.*?!', re.DOTALL)
                    interface_blocks = interface_pattern.findall(config_file.read())
                    for block in interface_blocks:
                        print(block.strip())
                case "service":
                    service_pattern = re.compile(r"\nservice\s+\S+\n.*?!", re.DOTALL)
                    service_blocks = service_pattern.findall(config_file.read())
                    for block in service_blocks:
                        print(block.strip())  # 去除前后空白字符
                case "policy":
                    policy_pattern = re.compile(r"\npolicy\s.*?(?:deny|permit)\s\d+.*?(?=create-by\s\S+.*?|\npolicy|\Z)", re.DOTALL)
                    policy_blocks = policy_pattern.findall(config_file.read())
                    print(policy_blocks)
                    for block in policy_blocks:
                        print(block.strip())
                case _:
                    pass
            # print(config_file.read())




if __name__ == '__main__':
    config = Configuration("../input/startup-0.cfg")
    config.search_module("policy")