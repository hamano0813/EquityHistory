#!/usr/bin/env python
# -*- coding: utf-8 -*-

from PySide6.QtCore import Qt, QAbstractTableModel, QModelIndex
from PySide6.QtGui import QFont, QAction
from PySide6.QtWidgets import QTableView, QHeaderView, QAbstractItemView, QMenu, QApplication


class ShareholdingModel(QAbstractTableModel):
    def __init__(self):
        super().__init__()
        self._shareholding = list()
        self._header = ['序号', '股东名称', '注册资本额\n（万元）', '持股比例\n（%）']

    def rowCount(self, parent=QModelIndex()):
        return len(self._shareholding)

    def columnCount(self, parent=QModelIndex()):
        return len(self._header)

    def headerData(self, section, orientation, role=Qt.DisplayRole):
        if role == Qt.DisplayRole:
            if orientation == Qt.Horizontal:
                return self._header[section]
        elif role == Qt.TextAlignmentRole:
            return Qt.AlignCenter

    def data(self, index, role=Qt.DisplayRole):
        if role == Qt.DisplayRole:
            row = index.row()
            col = index.column()
            return self._shareholding[row][col]
        elif role == Qt.TextAlignmentRole:
            col = index.column()
            if col == 0:
                return Qt.AlignCenter
            elif col == 1:
                return Qt.AlignLeft | Qt.AlignVCenter
            else:
                return Qt.AlignRight | Qt.AlignVCenter
        elif role == Qt.FontRole:
            row = index.row()
            if row == len(self._shareholding) - 1:
                font = QFont()
                font.setBold(True)
                return font

    def flags(self, index):
        return Qt.ItemIsEnabled | Qt.ItemIsSelectable

    def set_shareholding(self, shareholding):
        self.beginResetModel()
        self._shareholding = shareholding
        self.endResetModel()


class ShareholdingTable(QTableView):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.setAlternatingRowColors(True)
        self.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.setContextMenuPolicy(Qt.CustomContextMenu)
        self.customContextMenuRequested.connect(self.show_context_menu)
        self._copy_action = QAction('复制', self)
        self._copy_action.triggered.connect(self.copy_selection)
        self.addAction(self._copy_action)
        self._model = ShareholdingModel()
        self.setModel(self._model)
        self.setColumnWidth(0, 50)
        self.setColumnWidth(2, 100)
        self.setColumnWidth(3, 100)
        self.horizontalHeader().setSectionResizeMode(1, QHeaderView.Stretch)

    def set_shareholding(self, shareholding):
        self._model.set_shareholding(shareholding)

    def copy_selection(self):
        selection = self.selectionModel().selectedIndexes()
        if selection:
            rows = sorted(index.row() for index in selection)
            columns = sorted(index.column() for index in selection)
            row_count = rows[-1] - rows[0] + 1
            col_count = columns[-1] - columns[0] + 1
            table = [['' for j in range(col_count)] for i in range(row_count)]
            for index in selection:
                row = index.row() - rows[0]
                column = index.column() - columns[0]
                table[row][column] = str(index.data())
            text = '\n'.join(['\t'.join(row) for row in table])
            clipboard = QApplication.clipboard()
            clipboard.setText(text)

    def show_context_menu(self, pos):
        menu = QMenu(self)
        menu.addAction(self._copy_action)
        menu.exec_(self.viewport().mapToGlobal(pos))
