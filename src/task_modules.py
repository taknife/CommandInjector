#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2025/8/20 17:52
# @Author  : taknife
# @Project : CommandInjector
# @File    : task_modules.py

import device_link
from signal_modules import *
from PySide6.QtCore import QThread

class ExecutiveCommandThread(QThread):
    def __init__(self, ip, port, username, password, config_module, parent=None):
        super().__init__(parent)
        self.ip = ip
        self.port = port
        self.username = username
        self.password = password
        self.config_module = config_module

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