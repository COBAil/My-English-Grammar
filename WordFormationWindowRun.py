from PyQt5 import uic, QtWidgets
from PyQt5.QtWidgets import QApplication
import sys
import sqlite3
from random import choice

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
            self.label.setText(f"Средний результат: {average_value[0] / average_value[1]:.2f}/10")
        except ZeroDivisionError:
            self.label.setText('Средний результат: 0.00/10')

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

        self.pushButton.clicked.connect(self.back)

    def back(self):
        self.close()
        self.WordFormationSelectionWindow = WordFormationSelectionWindow()
        self.WordFormationSelectionWindow.show()


class TasksWindow(QtWidgets.QMainWindow):  # Практика
    def __init__(self):
        super().__init__()
        uic.loadUi('Windows/WordFormationWindows/WordFormationTasksWindow.ui', self)

        self.ResultWindow = None
        self.number_question = 1
        self.quantity_correct_answer = 0
        self.list_words = [sentence[0] for sentence in CONN.cursor().execute(
            f"SELECT word FROM WordFormationTasks").fetchall()]
        self.word = choice(self.list_words)

        self.display_question_and_answers()

        self.pushButton.clicked.connect(self.check_answer)

    def check_answer(self):
        self.plainTextEdit.clear()

        if self.buttonGroup.checkedButton() and self.pushButton.text() == 'Проверить':
            if self.buttonGroup.checkedButton().text() == CONN.cursor().execute(
                    f"SELECT correct_answer FROM WordFormationTasks WHERE word = '{self.word}'").fetchone()[0]:
                self.plainTextEdit.appendPlainText('Ответ Верный!')
                self.quantity_correct_answer += 1
            else:
                self.plainTextEdit.appendPlainText(CONN.cursor().execute(
                    f"SELECT explanation FROM WordFormationTasks WHERE word = '{self.word}'").fetchone()[0])

            self.list_words.remove(self.word)
            try:
                self.word = choice(self.list_words)
            except IndexError:
                pass
            self.number_question += 1
            self.pushButton.setText('Дальше') if self.number_question != 11 else self.pushButton.setText('Закончить')

        elif self.pushButton.text() == 'Дальше':
            self.pushButton.setText('Проверить')
            self.display_question_and_answers()

        elif self.pushButton.text() == 'Закончить':
            self.close()
            self.ResultWindow = ResultWindow(self.quantity_correct_answer)
            self.ResultWindow.show()

        else:
            self.plainTextEdit.appendPlainText('Вы не ответили на вопрос!')

    def display_question_and_answers(self):
        self.label_3.setText(f"Вопрос {self.number_question}/10")
        self.label_2.setText(self.word)
        list_answer_numbers = [1, 2, 3, 4]

        for radioButton in [self.radioButton, self.radioButton_2, self.radioButton_3, self.radioButton_4]:
            answer_number = choice(list_answer_numbers)
            radioButton.setText(CONN.cursor().execute(
                f"SELECT answer_{answer_number} FROM WordFormationTasks WHERE word = '{self.word}'").fetchone()[0])
            list_answer_numbers.remove(answer_number)


class ResultWindow(QtWidgets.QMainWindow):  # Результаты
    def __init__(self, quantity_correct_answer):
        super().__init__()
        uic.loadUi('Windows/WordFormationWindows/WordFormationResultWindow.ui', self)

        self.WordFormationSelectionWindow = None

        self.label.setText(f"Правильных ответов: {quantity_correct_answer}/10")
        CONN.cursor().execute(f"UPDATE Result SET value = value + {quantity_correct_answer}, count = count + 1")

        CONN.commit()

        self.pushButton.clicked.connect(self.back)

    def back(self):
        self.close()
        self.WordFormationSelectionWindow = WordFormationSelectionWindow()
        self.WordFormationSelectionWindow.show()


def except_hook(cls, exception, traceback):
    sys.__excepthook__(cls, exception, traceback)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = WordFormationSelectionWindow()
    ex.show()
    sys.excepthook = except_hook
    sys.exit(app.exec_())
