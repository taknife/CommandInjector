#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2025/8/12 10:53
# @Author  : taknife
# @Project : CommandInjector
# @File    : main.py
import sys
import configuration_clear
from task_modules import *
from functools import partial
from PySide6.QtCore import QStandardPaths
from PySide6.QtGui import QIcon, QIntValidator
from PySide6.QtWidgets import QApplication, QWidget, QFileDialog, QTextBrowser
from PySide6.QtUiTools import QUiLoader


class MainUI(QWidget):
    def __init__(self):
        super().__init__()
        self.ui = QUiLoader().load("../ui/main.ui")
        # self.ui = QUiLoader().load("./ui/main.ui")
        self.ui.config_path_button.clicked.connect(partial(self.upload_file))
        self.ui.module_select.addItems(["address", "service", "policy", "interface", "route"])
        self.ui.submit_button.clicked.connect(partial(self.submit_config))
        self.ui.clear_button.clicked.connect(partial(self.clear_text_button))
        self.ui.port.setValidator(QIntValidator())
        console_signals.text_print.connect(self.update_console_log)

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

        thread = ExecutiveCommandThread(ip, port, username, password, config_module, self)
        thread.start()

    def clear_text_button(self):
        self.ui.console_log.clear()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    # app.setWindowIcon(QIcon('./images/logo.png'))
    app.setWindowIcon(QIcon('../images/logo.png'))
    stats = MainUI()
    stats.ui.show()
    sys.exit(app.exec())
