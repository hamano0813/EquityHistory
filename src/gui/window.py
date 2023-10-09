#!/usr/bin/env python
# -*- coding: utf-8 -*-

from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QMainWindow, QTabWidget

from .help import HelpTab
from .history import HistoryTab
from .preview import PreviewTab


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.tab_widget = QTabWidget()
        self.setCentralWidget(self.tab_widget)

        self.history_tab = HistoryTab()
        self.preview_tab = PreviewTab()
        self.help_tab = HelpTab()
        self.tab_widget.addTab(self.history_tab, '股权沿革')
        self.tab_widget.addTab(self.preview_tab, '预览导出')
        self.tab_widget.addTab(self.help_tab, '使用说明')

        self.history_tab.equity_table.model().dataChanged.connect(self.refresh_preview)

        self.setMinimumSize(1280, 800)
        self.setWindowTitle('股权沿革辅助整理工具')
        self.setWindowIcon(QIcon(':icon.png'))

    def refresh_preview(self):
        self.preview_tab.event_view.set_history(self.history_tab.equity_table.get_history(),
                                                self.history_tab.company_line.text())
        self.preview_tab.event_view.clicked.emit(self.preview_tab.event_view.currentIndex())
