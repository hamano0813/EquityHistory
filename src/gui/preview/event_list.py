#!/usr/bin/env python
# -*- coding: utf-8 -*-

from PySide6 import QtWidgets, QtCore

from app.generator import generate_group


class EventModel(QtCore.QAbstractListModel):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.history = list()
        self.company = ''
        self.events = list()
        self.groups = dict()

    def rowCount(self, parent=QtCore.QModelIndex()):
        return len(self.groups)

    def data(self, index, role=QtCore.Qt.DisplayRole):
        if not index.isValid():
            return None
        event = self.events[index.row()]
        event_date, event_name = event
        if role == QtCore.Qt.DisplayRole:
            return f'{event_date.strftime("%Y年%m月")} {event_name}'
        elif role == QtCore.Qt.UserRole:
            return self.groups[event]
        elif role == QtCore.Qt.TextAlignmentRole:
            return QtCore.Qt.AlignCenter
        return None

    def set_history(self, history, company):
        self.beginResetModel()
        self.history = history
        self.company = company
        self.groups = generate_group(history, company)
        self.events = list(self.groups.keys())
        self.endResetModel()


class EventView(QtWidgets.QListView):
    def __init__(self, parent=None):
        super().__init__(parent)
        self._model = EventModel()
        self.setModel(self._model)
        self.setSelectionMode(QtWidgets.QAbstractItemView.SingleSelection)

    def set_history(self, history, company):
        self._model.set_history(history, company)
        self.setCurrentIndex(self._model.createIndex(0, 0))

    @property
    def groups(self):
        return self._model.groups

    @property
    def company(self):
        return self._model.company
