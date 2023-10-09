#!/usr/bin/env python
# -*- coding: utf-8 -*-

from PySide6.QtCore import Qt
from PySide6.QtWidgets import QTableView

from .history_dialog import HistoryDialog
from .history_model import HistoryModel


# noinspection PyUnresolvedReferences
class HistoryTable(QTableView):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setSelectionBehavior(QTableView.SelectRows)
        self.setSelectionMode(QTableView.SingleSelection)
        self.setWordWrap(True)

        self.verticalHeader().hide()
        self._model = HistoryModel()
        self.setModel(self._model)
        self._model.spanChanged[int, int, int, int].connect(self.setSpan)

        self.setColumnWidth(0, 100)
        self.setColumnWidth(1, 50)
        self.setColumnWidth(2, 320)
        self.setColumnWidth(3, 320)
        self.setColumnWidth(4, 105)
        self.setColumnWidth(5, 105)
        self.horizontalHeader().setStretchLastSection(True)

        self.doubleClicked.connect(self.modify)

    def mouseDoubleClickEvent(self, event):
        index = self.indexAt(event.pos())
        if not index.isValid():
            return self.append()
        if event.button() == Qt.RightButton and event.modifiers() == Qt.NoModifier:
            return self.remove()
        super().mouseDoubleClickEvent(event)

    def set_history(self, history):
        self._model.set_history(history)

    def get_history(self):
        return self._model.get_history()

    def sorted(self):
        self._model.sorted()

    def move_up(self):
        if self.selectedIndexes():
            self._model.move_up(self.selectedIndexes()[0].row())

    def move_down(self):
        if self.selectedIndexes():
            self._model.move_down(self.selectedIndexes()[0].row())

    def append(self):
        if event := HistoryDialog().get_event():
            self._model.append(event)

    def insert(self):
        if self.selectedIndexes():
            row = self.selectedIndexes()[0].row()
            if event := HistoryDialog().get_event():
                self._model.insert(row, event)

    def remove(self):
        if self.selectedIndexes():
            self._model.remove(self.selectedIndexes()[0].row())

    def modify(self):
        if self.selectedIndexes():
            row = self.selectedIndexes()[0].row()
            e = self._model.get_history()[row]
            if event := HistoryDialog().get_event(e):
                self._model.remove(row)
                self._model.insert(row, event)

    def repeat(self):
        if self.selectedIndexes():
            row = self.selectedIndexes()[0].row()
            self._model.insert(row, self._model.get_history()[row])
