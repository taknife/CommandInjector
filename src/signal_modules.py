#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2025/8/20 17:46
# @Author  : taknife
# @Project : CommandInjector
# @File    : signal_modules.py

from PySide6.QtCore import QObject, Signal
from PySide6.QtWidgets import QTextBrowser


# 串口打印信号
class ConsoleSignals(QObject):
    text_print = Signal(QTextBrowser,str)


# 输入检查状态信号
class CheckStatuSignals(QObject):
    statu = Signal(bool)


# 实例化对象
console_signals = ConsoleSignals()
statu_signals = CheckStatuSignals()