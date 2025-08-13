#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2025/8/12 10:54
# @Author  : taknife
# @Project : CommandInjector
# @File    : device_link.py

import paramiko
import time

class DeviceLink:
    def __init__(self, ip: str, port: int, username: str, password: str) -> None:
        self.__ip = ip
        self.__username = username
        self.__password = password
        self.__transport = paramiko.Transport((ip, port))
        self.__transport.connect(username=self.__username, password=self.__password)
        self.__ssh = paramiko.SSHClient()
        self.__ssh._transport = self.__transport
        self.__ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        self.__shell = self.__ssh.invoke_shell()

    def executive_command(self):
        self.__shell.send(bytes("show ip interface brief\n", "utf-8"))
        time.sleep(0.2)

    def __del__(self):
        self.__transport.close()