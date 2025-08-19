#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2025/8/12 10:53
# @Author  : taknife
# @Project : CommandInjector
# @File    : main.py
import sys
from threading import Thread

from PySide6 import QtGui
from PySide6.QtCore import QStandardPaths, QObject, Signal, QThread
from PySide6.QtGui import QIcon

import configuration_clear
import device_link
from functools import partial
from PySide6.QtWidgets import QApplication, QWidget, QFileDialog, QTextBrowser
from PySide6.QtUiTools import QUiLoader

# 自定义信号源对象类型，一定要继承自 QObject
class MySignals(QObject):
    # 定义一种信号，两个参数 类型分别是： QTextBrowser 和 字符串
    # 调用 emit方法 发信号时，传入参数 必须是这里指定的 参数类型
    text_print = Signal(QTextBrowser,str)
    # 还可以定义其他种类的信号
    update_table = Signal(str)
# 实例化
global_ms = MySignals()

class WorkerThread(QThread):
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
                global_ms.text_print.emit(self.parent().ui.console_log, link.executive_command("enable\n"))
                global_ms.text_print.emit(self.parent().ui.console_log, link.executive_command("configure terminal\n"))
                for config in self.config_module:
                    global_ms.text_print.emit(self.parent().ui.console_log, link.executive_command(config))
                global_ms.text_print.emit(self.parent().ui.console_log, link.executive_command("\n"))
                global_ms.text_print.emit(self.parent().ui.console_log, link.executive_command("end\n"))
                global_ms.text_print.emit(self.parent().ui.console_log, link.executive_command("save config\n"))
        except ConnectionError as e:
            global_ms.text_print.emit(self.parent().ui.console_log, f"连接错误: {e}")
        except Exception as e:
            global_ms.text_print.emit(self.parent().ui.console_log, f"其他错误: {e}")


class MainUI(QWidget):
    def __init__(self):
        super().__init__()
        self.ui = QUiLoader().load("../ui/main.ui")
        # self.ui = QUiLoader().load("./ui/main.ui")
        self.ui.config_path_button.clicked.connect(partial(self.upload_file))
        self.ui.module_select.addItems(["address", "service", "policy", "interface", "route"])
        self.ui.submit_button.clicked.connect(partial(self.submit_config))
        self.ui.clear_button.clicked.connect(partial(self.clear_text_button))
        self.ui.port.setValidator(QtGui.QIntValidator())
        global_ms.text_print.connect(self.update_console_log)

    @staticmethod
    def update_console_log(browser: QTextBrowser, text: str):
        browser.append(text)  # 追加文本
        browser.ensureCursorVisible()  # 确保光标可见（自动滚动）

    def upload_file(self):
        desktop_path = QStandardPaths.writableLocation(QStandardPaths.DesktopLocation) or "C:\\"
        filepath, _ = QFileDialog.getOpenFileName(
            self.ui,
            "选择你要上传的配置文件",
            desktop_path,
            "文本和配置文件 (*.txt *.cfg);;所有文件 (*)"
        )
        self.ui.config_path.setText(filepath)

    def submit_config(self):
        module_name = self.ui.module_select.currentText()
        config_path = self.ui.config_path.text()
        ip = self.ui.ip.text()
        port = int(self.ui.port.text())
        username = self.ui.username.text()
        password = self.ui.password.text()
        self.ui.console_log.setText("正在连接：{}:{}".format(ip, str(port)))
        config = configuration_clear.Configuration(config_path)
        config_module = config.search_module(module_name)

        thread = WorkerThread(ip, port, username, password, config_module, self)
        thread.start()

    def clear_text_button(self):
        self.ui.console_log.clear()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    # app.setWindowIcon(QIcon('./images/logo.png'))
    app.setWindowIcon(QIcon('../images/logo.png'))
    stats = MainUI()
    stats.ui.show()
    sys.exit(app.exec_())
