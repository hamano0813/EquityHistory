#!/usr/bin/env python
# -*- coding: utf-8 -*-

import datetime

from PySide6 import QtCore


def span_changed(func):
    def wrapper(*args, **kwargs):
        self = args[0]
        old_history = self._history.copy()
        func(*args, **kwargs)
        new_history = self._history
        if old_history != new_history:
            self.reset_span()
            self.dataChanged.emit(self._history)

    return wrapper


class HistoryModel(QtCore.QAbstractTableModel):
    spanChanged = QtCore.Signal(int, int, int, int)
    dataChanged = QtCore.Signal(list)

    def __init__(self):
        super().__init__()
        self._history = list()
        self._header = ('日期', '事件', '入资方', '退资方',
                        '注册资本\n（人民币元）', '认缴资本\n（人民币元）', '出资方式', '备注')
        self._span = (0, 1, 7)

    def headerData(self, section, orientation, role=QtCore.Qt.DisplayRole):
        if role == QtCore.Qt.DisplayRole and orientation == QtCore.Qt.Horizontal:
            return self._header[section]
        return None

    def rowCount(self, parent=QtCore.QModelIndex()):
        return len(self._history)

    def columnCount(self, parent=QtCore.QModelIndex()):
        return len(self._header)

    def data(self, index, role=QtCore.Qt.DisplayRole):
        if not index.isValid():
            return None

        row = index.row()
        col = index.column()
        item = self._history[row][col]

        if role == QtCore.Qt.DisplayRole:
            if col == 0:
                if item == datetime.date(2000, 1, 1):
                    return ''
                return item.strftime('%Y年%m月%d日')
            elif col in [4, 5]:
                return '{:,.2f}'.format(item)
            else:
                return str(item)
        elif role == QtCore.Qt.TextAlignmentRole:
            if col < 2 or col == 6:
                return QtCore.Qt.AlignCenter
            elif col in [4, 5]:
                return QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter
            else:
                return QtCore.Qt.AlignLeft | QtCore.Qt.AlignVCenter
        else:
            return None

    def flags(self, index):
        if index.column() in self._span:
            return QtCore.Qt.ItemFlag.NoItemFlags
        return QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsSelectable

    @span_changed
    def set_history(self, history):
        self.beginResetModel()
        self._history = history
        self.endResetModel()

    def get_history(self):
        return self._history

    @span_changed
    def append(self, event):
        self.beginInsertRows(QtCore.QModelIndex(), len(self._history), len(self._history))
        self._history.append(event)
        self.endInsertRows()

    @span_changed
    def insert(self, row, event):
        self.beginInsertRows(QtCore.QModelIndex(), row, row)
        self._history.insert(row, event)
        self.endInsertRows()

    @span_changed
    def remove(self, row):
        self.beginRemoveRows(QtCore.QModelIndex(), row, row)
        del self._history[row]
        self.endRemoveRows()

    @span_changed
    def sorted(self):
        self.beginResetModel()
        self._history.sort(key=lambda x: x[1])
        self._history.sort(key=lambda x: x[0])
        self.endResetModel()

    @span_changed
    def move_up(self, row):
        if row > 0:
            self.beginMoveRows(QtCore.QModelIndex(), row, row, QtCore.QModelIndex(), row - 1)
            self._history[row], self._history[row - 1] = self._history[row - 1], self._history[row]
            self.endMoveRows()

    @span_changed
    def move_down(self, row):
        if row < len(self._history) - 1:
            self.beginMoveRows(QtCore.QModelIndex(), row, row, QtCore.QModelIndex(), row + 2)
            self._history[row], self._history[row + 1] = self._history[row + 1], self._history[row]
            self.endMoveRows()

    def reset_span(self):
        date, event = None, None
        span = [0, 0]
        for rid, row in enumerate(self._history):
            if (date, event) != (row[0], row[1]):
                if rid != 0:
                    [self.spanChanged.emit(span[0], col, span[-1] - span[0] + 1, 1) for col in self._span]
                date, event = row[0: 2]
                span = list()
                span.append(rid)
            else:
                span.append(rid)
        [self.spanChanged.emit(span[0], col, span[-1] - span[0] + 1, 1) for col in self._span]
