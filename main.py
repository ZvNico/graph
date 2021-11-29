import sys

from PyQt5.QtWidgets import QApplication

from classes.App import App

if __name__ == '__main__':
    app = QApplication(sys.argv)
    fen = App()
    app.exec()
