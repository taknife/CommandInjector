#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2025/8/12 10:53
# @Author  : taknife
# @Project : CommandInjector
# @File    : main.py

import configuration_clear
import device_link

if __name__ == '__main__':
    module_name = "service"
    config_path = "../input/startup-0.cfg"
    config = configuration_clear.Configuration(config_path)
    config_module = config.search_module(module_name)
    device_link.main("192.168.211.101", 22, "admin", "admin.123", config_module)
