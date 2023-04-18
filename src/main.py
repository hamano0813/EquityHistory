#!/usr/bin/env python
# -*- coding: utf-8 -*-

if __name__ == '__main__':
    import sys
    from PySide6.QtWidgets import QApplication
    from gui.window import MainWindow
    import resource

    app = QApplication(sys.argv)
    app.setStyleSheet("QPushButton {height: 25px; width: 120px}")

    window = MainWindow()
    window.showNormal()

    sys.exit(app.exec())
