#!/usr/bin/env python
# -*- coding: utf-8 -*-
import datetime

from PySide6 import QtWidgets, QtGui

from resource import *


class CenterTopLabel(QtWidgets.QLabel):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setAlignment(QtCore.Qt.AlignTop | QtCore.Qt.AlignHCenter)
        self.setContentsMargins(0, 3, 0, 0)


class AmountSpin(QtWidgets.QDoubleSpinBox):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setRange(-2000000000, 2000000000)
        self.setDecimals(2)
        self.setLocale(QtCore.QLocale.Language.Chinese)
        self.setAlignment(QtCore.Qt.AlignRight)
        self.setSuffix(' 元')
        self.setButtonSymbols(QtWidgets.QDoubleSpinBox.NoButtons)
        self.setGroupSeparatorShown(True)


class HistoryDialog(QtWidgets.QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle('股权变更事件')
        self.setMaximumHeight(150)
        self.setWindowIcon(QtGui.QIcon(':icon.png'))
        self.setWindowFlags(QtCore.Qt.SubWindow)

        self.event_date = QtWidgets.QDateEdit()
        self.event_date.setCalendarPopup(True)
        self.event_date.setDisplayFormat('yyyy年MM月dd日')

        self.equity_event = QtWidgets.QComboBox()
        self.equity_event.addItems(['成立', '增资', '减资', '转让'])

        self.investor_name = QtWidgets.QLineEdit()
        self.divester_name = QtWidgets.QLineEdit()

        self.registered_capital = AmountSpin()
        self.paidin_capital = AmountSpin()

        self.way_method = QtWidgets.QComboBox()
        self.way_method.addItems(['货币', '有形动产', '不动产', '无形资产', '股权', '债权', '其他权益'])

        self.remark_text = QtWidgets.QLineEdit()

        event_date = CenterTopLabel('日期')
        equity_event = CenterTopLabel('事件')
        investor_name = CenterTopLabel('入资方')
        divester_name = CenterTopLabel('退资方')
        registered_capital = CenterTopLabel('注册资本')
        paidin_capital = CenterTopLabel('认缴资本')
        way_method = CenterTopLabel('出资方式')
        remark_text = CenterTopLabel('备注')

        accept_button = QtWidgets.QPushButton('确定')
        reject_button = QtWidgets.QPushButton('取消')
        button_box = QtWidgets.QDialogButtonBox()
        button_box.setOrientation(QtCore.Qt.Horizontal)
        button_box.addButton(accept_button, QtWidgets.QDialogButtonBox.AcceptRole)
        button_box.addButton(reject_button, QtWidgets.QDialogButtonBox.RejectRole)
        button_box.accepted.connect(self.accept)
        button_box.rejected.connect(self.reject)

        grid_layout = QtWidgets.QGridLayout()

        grid_layout.addWidget(event_date, 0, 0)
        grid_layout.addWidget(self.event_date, 0, 1)
        grid_layout.addWidget(equity_event, 0, 2)
        grid_layout.addWidget(self.equity_event, 0, 3)

        grid_layout.addWidget(investor_name, 1, 0)
        grid_layout.addWidget(self.investor_name, 1, 1, 1, 3)
        grid_layout.addWidget(divester_name, 2, 0)
        grid_layout.addWidget(self.divester_name, 2, 1, 1, 3)

        grid_layout.addWidget(registered_capital, 3, 0)
        grid_layout.addWidget(self.registered_capital, 3, 1)
        grid_layout.addWidget(paidin_capital, 3, 2)
        grid_layout.addWidget(self.paidin_capital, 3, 3)

        grid_layout.addWidget(way_method, 4, 2)
        grid_layout.addWidget(self.way_method, 4, 3)

        grid_layout.addWidget(remark_text, 5, 0)
        grid_layout.addWidget(self.remark_text, 5, 1, 1, 3)

        grid_layout.addWidget(button_box, 6, 1, 1, 3)
        self.setLayout(grid_layout)

        self.equity_event.currentTextChanged.connect(self.event_change)
        self.event_change()

    def event_change(self):
        event = self.equity_event.currentText()
        if event in ('成立', '增资'):
            self.investor_name.setEnabled(True)
            self.divester_name.setEnabled(False)
        elif event == '减资':
            self.investor_name.setEnabled(False)
            self.divester_name.setEnabled(True)
        else:
            self.investor_name.setEnabled(True)
            self.divester_name.setEnabled(True)

    def get_event(self, e: list = None):
        if e:
            self.event_date.setDate(e[0])
            self.equity_event.setCurrentText(e[1])
            self.investor_name.setText(e[2])
            self.divester_name.setText(e[3])
            self.registered_capital.setValue(e[4])
            self.paidin_capital.setValue(e[5])
            self.way_method.setCurrentText(e[6])
            self.remark_text.setText(e[7])
        if self.exec():
            date = self.event_date.date().toPython()
            event = self.equity_event.currentText()
            investor = self.investor_name.text().strip() if event != '减资' else ''
            divester = self.divester_name.text().strip() if event not in ('成立', '增资') else ''
            regist = self.registered_capital.value()
            paidin = self.paidin_capital.value()
            way = self.way_method.currentText()
            remark = self.remark_text.text().strip()
            if alert := self.check_alert(_e := [date, event, investor, divester, regist, paidin, way, remark]):
                box = QtWidgets.QMessageBox(QtWidgets.QMessageBox.Warning, '', alert,
                                            parent=self, flags=QtCore.Qt.FramelessWindowHint)
                box.addButton('继续', QtWidgets.QMessageBox.YesRole)
                box.exec()
                return self.get_event(_e)
            return _e
        return None

    @staticmethod
    def check_alert(e):
        date, event, investor, divester, regist, *_ = e
        if date == datetime.date(2000, 1, 1) or date > datetime.date.today():
            return '需要选择正确的股权变动日期'
        if event in ('成立', '增资'):
            if not investor:
                return f'事件为{event}时，入资方名称不可为空'
        elif event == '减资':
            if not divester:
                return f'事件为{event}时，退资方名称不可为空'
        elif event == '转让':
            if not investor and not divester:
                return f'事件为{event}时，入资方和退资方名称不可同时为空'
        if not (regist > 0.0):
            return '注册资本不可为空'
        return False
