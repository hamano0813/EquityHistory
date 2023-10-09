#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pickle

from PySide6 import QtWidgets, QtCore

from .history_table import HistoryTable


# noinspection PyUnresolvedReferences
class HistoryTab(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.company_label = QtWidgets.QLabel('被评估单位')
        self.company_line = QtWidgets.QLineEdit()
        self.equity_table = HistoryTable()

        repeat_button = QtWidgets.QPushButton('复制(C)')
        insert_button = QtWidgets.QPushButton('插入(I)')
        modify_button = QtWidgets.QPushButton('编辑(M)')
        remove_button = QtWidgets.QPushButton('删除(D)')
        append_button = QtWidgets.QPushButton('新增(N)')

        repeat_button.setShortcut('Ctrl+C')
        insert_button.setShortcut('Ctrl+I')
        modify_button.setShortcut('Ctrl+M')
        remove_button.setShortcut('Ctrl+D')
        append_button.setShortcut('Ctrl+N')

        sort_button = QtWidgets.QPushButton('自动排序')
        up_button = QtWidgets.QPushButton('上移一行')
        down_button = QtWidgets.QPushButton('下移一行')
        save_button = QtWidgets.QPushButton('保存记录')
        load_button = QtWidgets.QPushButton('载入记录')

        repeat_button.clicked.connect(self.equity_table.repeat)
        insert_button.clicked.connect(self.equity_table.insert)
        modify_button.clicked.connect(self.equity_table.modify)
        remove_button.clicked.connect(self.equity_table.remove)
        append_button.clicked.connect(self.equity_table.append)

        sort_button.clicked.connect(self.equity_table.sorted)
        up_button.clicked.connect(self.equity_table.move_up)
        down_button.clicked.connect(self.equity_table.move_down)
        save_button.clicked.connect(self.save_history)
        load_button.clicked.connect(self.load_data)

        button_layout = QtWidgets.QGridLayout()
        button_layout.addItem(
            QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum), 0, 0)
        button_layout.addWidget(repeat_button, 0, 1)
        button_layout.addWidget(insert_button, 0, 2)
        button_layout.addWidget(modify_button, 0, 3)
        button_layout.addWidget(remove_button, 0, 4)
        button_layout.addWidget(append_button, 0, 5)

        button_layout.addWidget(sort_button, 1, 1)
        button_layout.addWidget(up_button, 1, 2)
        button_layout.addWidget(down_button, 1, 3)
        button_layout.addWidget(load_button, 1, 4)
        button_layout.addWidget(save_button, 1, 5)

        main_layout = QtWidgets.QVBoxLayout()
        company_layout = QtWidgets.QHBoxLayout()
        company_layout.addWidget(self.company_label)
        company_layout.addWidget(self.company_line)
        main_layout.addLayout(company_layout)
        main_layout.addWidget(self.equity_table)
        main_layout.addLayout(button_layout)
        self.setLayout(main_layout)

    def save_history(self):
        file_path, _ = QtWidgets.QFileDialog.getSaveFileName(self, '保存记录', self.company_line.text(),
                                                             'Pickle Files (*.ehpk)')
        if file_path:
            company = self.company_line.text()
            history = self.equity_table.model().get_history()
            with open(file_path, 'wb') as f:
                pickle.dump((company, history), f)
            box = QtWidgets.QMessageBox(QtWidgets.QMessageBox.Information, '', ' 保存完毕 ',
                                        parent=self, flags=QtCore.Qt.FramelessWindowHint)
            box.addButton('确定', QtWidgets.QMessageBox.YesRole)
            box.exec()

    def load_data(self):
        file_path, _ = QtWidgets.QFileDialog.getOpenFileName(self, '载入记录', self.company_line.text(),
                                                             'Pickle Files (*.ehpk)')
        if file_path:
            with open(file_path, 'rb') as f:
                company, history = pickle.load(f)
            self.company_line.setText(company)
            self.equity_table.model().set_history(history)
