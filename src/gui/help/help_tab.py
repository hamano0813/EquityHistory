#!/usr/bin/env python
# -*- coding: utf-8 -*-

from PySide6 import QtWidgets

from resource import *


class HelpTab(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.help_text = QtWidgets.QTextEdit()
        self.help_text.setReadOnly(True)
        self.help_text.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)

        html = QtCore.QFile(':/README.html')
        html.open(QtCore.QFile.ReadOnly)
        self.help_text.setHtml(bytearray(html.readAll()).decode('UTF-8'))

        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(self.help_text)
        self.setLayout(layout)
