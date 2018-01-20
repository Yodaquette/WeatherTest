"""
    Andrew Goodman
    January 18, 2018

    The main entry point for the Weather Test app
"""
import sys
from PyQt5.QtWidgets import QApplication
from modules.application.MainWindow import MainWindow

app = QApplication(sys.argv)
main_window = MainWindow()
sys.exit(app.exec_())