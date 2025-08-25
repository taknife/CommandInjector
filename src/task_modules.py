#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2025/8/20 17:52
# @Author  : taknife
# @Project : CommandInjector
# @File    : task_modules.py

import re
import os
import device_link
from signal_modules import *
from PySide6.QtCore import QThread


# 下发命令线程类
class ExecutiveCommandThread(QThread):
    def __init__(self, ip, port, username, password, config_module, parent=None):
        super().__init__(parent)
        self.ip = ip
        self.port = port
        self.username = username
        self.password = password
        self.config_module = config_module

    # 运行函数，线程自动调用
    def run(self):
        try:
            with device_link.DeviceLink(self.ip, self.port, self.username, self.password) as link:
                console_signals.text_print.emit(self.parent().ui.console_log, link.executive_command("enable\n"))
                console_signals.text_print.emit(self.parent().ui.console_log, link.executive_command("configure terminal\n"))
                for config in self.config_module:
                    console_signals.text_print.emit(self.parent().ui.console_log, link.executive_command(config))
                console_signals.text_print.emit(self.parent().ui.console_log, link.executive_command("\n"))
                console_signals.text_print.emit(self.parent().ui.console_log, link.executive_command("end\n"))
                console_signals.text_print.emit(self.parent().ui.console_log, link.executive_command("save config\n"))
        except ConnectionError as e:
            console_signals.text_print.emit(self.parent().ui.console_log, f"连接错误: {e}")
        except Exception as e:
            console_signals.text_print.emit(self.parent().ui.console_log, f"其他错误: {e}")


# 自检输入参数线程类
class CheckInputDataThread(QThread):
    def __init__(self, ip, config_path, parent=None):
        super().__init__(parent)
        self.ip = ip
        self.config_path = config_path

    # 运行函数，线程自动调用
    def run(self):
        ip_statu = self.check_input_ip()
        path_statu = self.check_input_config_path()
        if ip_statu and path_statu:
            statu_signals.statu.emit(True)
        else:
            statu_signals.statu.emit(False)

    # 检查配置路径方法
    def check_input_config_path(self):
        """
        验证配置路径的有效性
        """
        # 1. 检查空路径
        if not self.config_path or self.config_path.isspace():
            error_msg = "配置路径不能为空"
            console_signals.text_print.emit(self.parent().ui.console_log, error_msg)
            return False

        # 2. 检查非法字符
        illegal_chars = r'[<>"|?*]'
        if re.search(illegal_chars, self.config_path):
            error_msg = f"路径包含非法字符: {self.config_path}"
            console_signals.text_print.emit(self.parent().ui.console_log, error_msg)
            return False

        try:
            # 3. 规范化路径
            abs_path = os.path.abspath(self.config_path)
            normalized_path = os.path.normpath(abs_path)

            # 4. 检查路径是否存在（可选）
            if not os.path.exists(normalized_path):
                # 如果路径不存在，可以询问是否创建或者直接返回错误
                error_msg = f"路径不存在: {normalized_path}"
                console_signals.text_print.emit(self.parent().ui.console_log, error_msg)
                return False

            # 5. 验证通过
            console_signals.text_print.emit(self.parent().ui.console_log, f"配置路径有效: {normalized_path}")
            return True

        except Exception as e:
            error_msg = f"路径处理异常: {str(e)}"
            console_signals.text_print.emit(self.parent().ui.console_log, error_msg)
            return False

    # 检查IP地址格式方法
    def check_input_ip(self):
        if self.ip:
            ipv4_pattern = r'^((25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$'
            pattern = re.compile(ipv4_pattern)
            if pattern.match(self.ip):
                console_signals.text_print.emit(self.parent().ui.console_log, "IP地址检查正确")
                return True
            else:
                console_signals.text_print.emit(self.parent().ui.console_log, "IP地址检查错误，请重新输入IP地址")
                return False
        else:
            console_signals.text_print.emit(self.parent().ui.console_log, "请输入IP地址")
            return False