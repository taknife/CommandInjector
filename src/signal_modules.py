#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2025/8/20 17:46
# @Author  : taknife
# @Project : CommandInjector
# @File    : signal_modules.py

from PySide6.QtCore import QObject, Signal
from PySide6.QtWidgets import QTextBrowser


# 自定义信号源对象类型，一定要继承自 QObject
class ConsoleSignals(QObject):
    text_print = Signal(QTextBrowser,str)


console_signals = ConsoleSignals()
