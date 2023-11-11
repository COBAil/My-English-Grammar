from TensesWindowRun import TensesWindow
from WordFormationWindowRun import WordFormationSelectionWindow
from PyQt5 import uic, QtWidgets
from PyQt5.QtWidgets import QApplication
import sys


class StartWindow(QtWidgets.QMainWindow):  # Выбор "категории"
    def __init__(self):
        super().__init__()
        uic.loadUi('Windows/StartWindow/StartWindow.ui', self)

        self.TensesWindow = None
        self.WordFormationSelectionWindow = None
        # sef._ = None

        self.pushButton.clicked.connect(self.open_TensesWindow)
        self.pushButton_2.clicked.connect(self.open_WordFormationWindow)
        # self.pushButton_3.clicked.connect(self.open_s)

    def open_TensesWindow(self):
        self.close()
        self.TensesWindow = TensesWindow()
        self.TensesWindow.show()

    def open_WordFormationWindow(self):
        self.close()
        self.WordFormationSelectionWindow = WordFormationSelectionWindow()
        self.WordFormationSelectionWindow.show()

    # def open_s(self):
    #     pass


def except_hook(cls, exception, traceback):
    sys.__excepthook__(cls, exception, traceback)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = StartWindow()
    ex.show()
    sys.excepthook = except_hook
    sys.exit(app.exec_())
