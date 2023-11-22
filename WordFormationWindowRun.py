from PyQt5 import uic, QtWidgets
from PyQt5.QtWidgets import QApplication
import sys
import sqlite3

CONN = sqlite3.connect('DataBases/WordFormationProgress.db')


class WordFormationSelectionWindow(QtWidgets.QMainWindow):  # Выбор между теорией и практикой
    def __init__(self):
        super().__init__()
        uic.loadUi('Windows/WordFormationWindows/WordFormationSelectionWindow.ui', self)

        self.TheoryWindow = None
        self.TasksWindow = None
        self.StartWindow = None
        average_value = CONN.cursor().execute(f"SELECT value, count FROM Result").fetchone()

        try:
            self.label.setText(f"Средний результат: {average_value[0] // average_value[1]}/10")
        except ZeroDivisionError:
            self.label.setText('Средний результат: 0/10')

        self.pushButton.clicked.connect(self.open_TheoryWindow)
        self.pushButton_2.clicked.connect(self.open_TasksWindow)
        self.pushButton_3.clicked.connect(self.back)

    def open_TheoryWindow(self):
        self.close()
        self.TheoryWindow = TheoryWindow()
        self.TheoryWindow.show()

    def open_TasksWindow(self):
        self.close()
        self.TasksWindow = TasksWindow()
        self.TasksWindow.show()

    def back(self):
        from StartWindowRun import StartWindow
        self.close()
        self.StartWindow = StartWindow()
        self.StartWindow.show()


class TheoryWindow(QtWidgets.QMainWindow):  # Теория
    def __init__(self):
        super().__init__()
        uic.loadUi('Windows/WordFormationWindows/WordFormationTheoryWindow.ui', self)

        self.WordFormationSelectionWindow = None

        self.plainTextEdit.appendPlainText(CONN.cursor().execute(f"SELECT theory FROM Theory").fetchone()[0])

        self.pushButton.clicked.connect(self.back)

    def back(self):
        self.close()
        self.WordFormationSelectionWindow = WordFormationSelectionWindow()
        self.WordFormationSelectionWindow.show()


class TasksWindow(QtWidgets.QMainWindow):  # Практика
    def __init__(self):
        super().__init__()
        uic.loadUi('Windows/WordFormationWindows/WordFormationTasksWindow.ui', self)


def except_hook(cls, exception, traceback):
    sys.__excepthook__(cls, exception, traceback)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = WordFormationSelectionWindow()
    ex.show()
    sys.excepthook = except_hook
    sys.exit(app.exec_())
