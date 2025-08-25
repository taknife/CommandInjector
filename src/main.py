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
from PySide6.QtUiTools import QUiLoader
from PySide6.QtCore import QStandardPaths
from PySide6.QtGui import QIcon, QIntValidator
from PySide6.QtWidgets import QApplication, QWidget, QFileDialog, QTextBrowser


class MainUI(QWidget):
    def __init__(self):
        super().__init__()
        # 动态调用UI
        self.ui = QUiLoader().load("../ui/main.ui")
        # self.ui = QUiLoader().load("./ui/main.ui")
        self.ui.config_path_button.clicked.connect(partial(self.upload_file))
        self.ui.module_select.addItems(["address", "service", "policy", "interface", "route"])
        self.ui.submit_button.clicked.connect(partial(self.submit_config))
        self.ui.clear_button.clicked.connect(partial(self.clear_text_button))
        self.ui.port.setValidator(QIntValidator())
        self.check_input_statu = None
        # 存储当前提交的数据，以便在信号处理中使用
        self.current_submit_data = {}
        # 初始化提交数据
        self.current_module_name = ""
        self.current_config_path = ""
        self.current_ip = ""
        self.current_port = 0
        self.current_username = ""
        self.current_password = ""

        # 信号连接槽函数
        console_signals.text_print.connect(self.update_console_log)
        statu_signals.statu.connect(self.on_input_check_complete)



    @staticmethod
    def update_console_log(browser: QTextBrowser, text: str):
        browser.append(text)  # 追加文本
        browser.ensureCursorVisible()  # 确保光标可见（自动滚动）

    def on_input_check_complete(self, statu: bool):
        """输入检查完成后的回调函数"""
        if not statu:
            console_signals.text_print.emit(self.ui.console_log, "输入数据验证失败")
            return

        # 使用存储的类属性
        console_signals.text_print.emit(self.ui.console_log, f"正在连接：{self.current_ip}:{self.current_port}")

        try:
            # 开始对配置文件进行数据清洗
            config = configuration_clear.Configuration(self.current_config_path)
            config_module = config.search_module(self.current_module_name)

            # 启动配置导入线程
            thread = ExecutiveCommandThread(
                self.current_ip,
                self.current_port,
                self.current_username,
                self.current_password,
                config_module, self
            )
            thread.start()

        except Exception as e:
            console_signals.text_print.emit(self.ui.console_log, f"配置处理错误: {str(e)}")

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
        """提交配置，启动输入验证"""
        self.current_module_name = self.ui.module_select.currentText()
        self.current_config_path = self.ui.config_path.text()
        self.current_ip = self.ui.ip.text()
        self.current_username = self.ui.username.text()
        self.current_password = self.ui.password.text()

        # 获取并验证端口
        port_text = self.ui.port.text()
        if not port_text.isdigit():
            console_signals.text_print.emit(self.ui.console_log, "端口必须是数字")
            return
        self.current_port = int(port_text)

        # 基本非空验证
        if not all([self.current_config_path, self.current_ip, self.current_username, self.current_password]):
            console_signals.text_print.emit(self.ui.console_log, "请填写所有必填字段")
            return

        # 显示验证提示
        console_signals.text_print.emit(self.ui.console_log, "正在验证输入数据...")

        # 启动验证线程
        thread_0 = CheckInputDataThread(self.current_ip, self.current_config_path, self)
        thread_0.start()

    def clear_text_button(self):
        self.ui.console_log.clear()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    # app.setWindowIcon(QIcon('./images/logo.png'))
    app.setWindowIcon(QIcon('../images/logo.png'))
    stats = MainUI()
    stats.ui.show()
    sys.exit(app.exec())
