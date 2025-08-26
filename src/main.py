#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2025/8/12 10:53
# @Author  : taknife
# @Project : CommandInjector
# @File    : main.py

import sys
import text_config_cleaning
import configuration_cleaning
from task_modules import *
from functools import partial
from local_config_manager import *
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
        self.check_config_suffix()
        self.config_manager = ConfigManager("../config/sysconfig.yaml")
        # self.config_manager = ConfigManager("./config/sysconfig.yaml")
        self.ui.config_path_button.clicked.connect(partial(self.upload_file))
        self.ui.config_path.setText(self.config_manager.get('config_file.path'))
        self.ui.config_path.textChanged.connect(self.check_config_suffix)
        self.ui.module_select.setEnabled(self.config_manager.get('config_file.statu'))
        self.ui.module_select.addItems(["address", "service", "policy", "interface", "route"])
        self.ui.submit_button.clicked.connect(partial(self.submit_config))
        self.ui.clear_button.clicked.connect(partial(self.clear_text_button))
        self.ui.ip.setText(self.config_manager.get('network.default_ip'))
        self.ui.port.setValidator(QIntValidator())
        self.ui.port.setText(self.config_manager.get('network.default_port'))
        self.ui.username.setText(self.config_manager.get('authentication.username'))
        self.ui.password.setText(self.config_manager.get('authentication.password'))
        # 存储当前提交的数据，以便在信号处理中使用
        self.current_submit_data = {}
        # 初始化提交数据
        self.current_module_name = ""
        self.current_config_path = ""
        self.current_ip = ""
        self.current_port = 0
        self.current_username = ""
        self.current_password = ""
        self.__suffix = ""
        # 初始化配置参数
        self.check_input_statu = None
        # 信号连接槽函数
        console_signals.text_print.connect(self.update_console_log)
        statu_signals.statu.connect(self.on_input_check_complete)

    @staticmethod
    def update_console_log(browser: QTextBrowser, text: str):
        browser.append(text)  # 追加文本
        browser.ensureCursorVisible()  # 确保光标可见（自动滚动）

    # 自检输入参数是否存在问题
    def on_input_check_complete(self, statu: bool):
        """输入检查完成后的回调函数"""
        if not statu:
            console_signals.text_print.emit(self.ui.console_log, "输入数据验证失败")
            return

        # 将输入内容添加到配置文件
        self.config_manager.set('config_file.path', self.ui.config_path.text())
        self.config_manager.set('network.default_ip', self.ui.ip.text())
        self.config_manager.set('network.default_port', self.ui.port.text())
        self.config_manager.set('authentication.username', self.ui.username.text())
        self.config_manager.set('authentication.password', self.ui.password.text())
        self.config_manager.save()

        # 使用存储的类属性
        console_signals.text_print.emit(self.ui.console_log, f"正在连接：{self.current_ip}:{self.current_port}")

        try:
            config_module = None
            # 开始对配置文件进行数据清洗
            if self.__suffix == ".cfg":
                config = configuration_cleaning.Configuration(self.current_config_path)
                config_module = config.search_module(self.current_module_name)
            elif self.__suffix == ".txt":
                config = text_config_cleaning.TextConfig(self.current_config_path)
                config_module = config.check_text_config()

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

    # 检查配置文件后缀名，如果为.cfg则开启模块选择窗口，如果为.txt则关闭模块选择窗口
    def check_config_suffix(self):
        """检查配置文件后缀名并设置模块选择窗口状态"""
        config_path = self.ui.config_path.text()

        if not config_path:
            self.ui.module_select.setEnabled(False)
            return

        try:
            # 使用pathlib获取后缀名
            self.__suffix = Path(config_path).suffix.lower()

            if self.__suffix == '.cfg':
                self.ui.module_select.setEnabled(True)
                self.config_manager.set('config_file.statu', True)
            elif self.__suffix == '.txt':
                self.ui.module_select.setEnabled(False)
                self.config_manager.set('config_file.statu', False)
            else:
                self.ui.module_select.setEnabled(False)
                self.config_manager.set('config_file.statu', False)

        except Exception as e:
            console_signals.text_print.emit(self.ui.console_log, f"路径解析错误: {str(e)}")
            self.ui.module_select.setEnabled(False)

    # 文件上传方法
    def upload_file(self):
        desktop_path = QStandardPaths.writableLocation(QStandardPaths.DesktopLocation) or "C:\\"
        filepath, _ = QFileDialog.getOpenFileName(
            self.ui,
            "选择你要上传的配置文件",
            desktop_path,
            "文本和配置文件 (*.txt *.cfg);;所有文件 (*)"
        )
        self.ui.config_path.setText(filepath)

    # 点击提交按钮后执行的方法
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

    # 清空打印框内的全部数据
    def clear_text_button(self):
        self.ui.console_log.clear()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    # app.setWindowIcon(QIcon('./ui/images/logo.png'))
    app.setWindowIcon(QIcon('../ui/images/logo.png'))
    stats = MainUI()
    stats.ui.show()
    sys.exit(app.exec())
