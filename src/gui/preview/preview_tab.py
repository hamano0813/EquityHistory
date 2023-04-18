# !/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import time

from PySide6 import QtWidgets, QtCore

from app.converter import convert_docx
from .event_list import EventView
from .shareholding_table import ShareholdingTable


class PreviewTab(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        left_layout = QtWidgets.QVBoxLayout()
        self.event_view = EventView()
        self.event_view.setFixedWidth(128)
        output_button = QtWidgets.QPushButton('导出文件')
        left_layout.addWidget(self.event_view)
        left_layout.addWidget(output_button)

        right_layout = QtWidgets.QVBoxLayout()
        self.overview_text = QtWidgets.QTextEdit()
        self.overview_text.setFixedHeight(150)
        self.shareholding_table = ShareholdingTable()
        right_layout.addWidget(self.overview_text)
        right_layout.addWidget(self.shareholding_table)

        main_layout = QtWidgets.QHBoxLayout()
        main_layout.addLayout(left_layout)
        main_layout.addLayout(right_layout)

        self.setLayout(main_layout)

        self.event_view.clicked.connect(self.event_switch)
        output_button.clicked.connect(self.output_docx)

    def event_switch(self):
        row = self.event_view.currentIndex().row()
        event = self.event_view.model().events[row]
        group = self.event_view.model().groups[event]
        self.overview_text.setText(group['overview'])
        self.shareholding_table.set_shareholding(group['shareholding'])

    def output_docx(self):
        file_path, _ = QtWidgets.QFileDialog.getSaveFileName(self, '导出文件', f'{self.event_view.company}',
                                                             'Docx Files (*.docx)')
        if file_path:
            if not self.event_view.groups:
                box = QtWidgets.QMessageBox(QtWidgets.QMessageBox.Warning, '', ' 没有股权变更记录 ',
                                            parent=self, flags=QtCore.Qt.FramelessWindowHint)
                box.addButton('返回', QtWidgets.QMessageBox.YesRole)
                box.exec()
                return False
            elif not self.event_view.company:
                box = QtWidgets.QMessageBox(QtWidgets.QMessageBox.Warning, '', ' 没有填写被评估单位 ',
                                            parent=self, flags=QtCore.Qt.FramelessWindowHint)
                box.addButton('返回', QtWidgets.QMessageBox.YesRole)
                box.exec()
                return False

            convert_docx(self.event_view.groups, self.event_view.company, file_path)
            box = QtWidgets.QMessageBox(QtWidgets.QMessageBox.Information, '', ' 导出完毕 ',
                                        parent=self, flags=QtCore.Qt.FramelessWindowHint)
            box.addButton('打开', QtWidgets.QMessageBox.YesRole)
            box.addButton('返回', QtWidgets.QMessageBox.NoRole)
            if not box.exec():
                os.system(f'start {file_path}')
