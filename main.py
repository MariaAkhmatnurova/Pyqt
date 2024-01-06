import sys
import random
import sqlite3
from PyQt5.QtGui import QPixmap, QFont, QTextCursor, QTextCharFormat, QColor
from PyQt5.QtWidgets import (
    QMainWindow,
    QTableWidgetItem,
    QTableWidget,
    QApplication,
    QWidget,
    QLabel,
    QPushButton,
    QVBoxLayout,
    QStackedWidget,
    QInputDialog,
    QRadioButton,
    QButtonGroup,
    QDialog,
    QTextEdit,
    QHBoxLayout,
    QMessageBox
)
from PyQt5.QtCore import Qt, QTime


# Главное окно приложения
class MainWindow(QWidget):
    def __init__(self, stacked_widget, typing_test_window):
        super().__init__()

        self.test_window = typing_test_window
        self.stacked_widget = stacked_widget
        self.init_ui()

    def init_ui(self):
        # Создаем виджеты и устанавливаем их параметры
        label_welcome = QLabel('Тест скорости печати')
        label_welcome.setFont(QFont('Arial', 20))
        label_welcome.setAlignment(Qt.AlignCenter)
        label_welcome.setStyleSheet("font: bold;")

        start_button = QPushButton('Начать тест')
        start_button.setFont(QFont('Arial', 17))
        start_button.clicked.connect(self.start_test)
        start_button.setStyleSheet("background-color: rgb(227, 184, 109); font: bold;")

        rating_button = QPushButton('Рейтинг')
        rating_button.setFont(QFont('Arial', 17))
        rating_button.clicked.connect(self.rating_table)
        rating_button.setStyleSheet("background-color: rgb(227, 184, 109); font: bold;")

        pixmap = QPixmap('speed.png')
        image = QLabel()
        image.setAlignment(Qt.AlignCenter)
        image.move(80, 60)
        image.resize(100, 100)
        image.setPixmap(pixmap)

        # Организуем компоновку
        layout = QVBoxLayout()
        layout.addWidget(label_welcome)
        layout.addWidget(image)
        layout.addWidget(start_button)
        layout.addSpacing(15)
        layout.addWidget(rating_button)
        layout.addSpacing(10)
        self.setLayout(layout)

    # Переключение на окно теста скорости печати
    def start_test(self):
        self.stacked_widget.setCurrentIndex(1)
        self.test_window.run()

    # Переключение на окно рейтинга
    def rating_table(self):
        self.stacked_widget.setCurrentIndex(2)


# Окно теста скорости печати
class TypingTestWindow(QWidget):
    def __init__(self, stacked_widget, dbsample, rating_window):
        super().__init__()

        self.rating_window = rating_window
        self.db = dbsample
        self.stacked_widget = stacked_widget
        self.init_ui()

    def init_ui(self):
        # Создаем виджеты и устанавливаем их параметры
        self.label_instruction = QLabel('Введите следующий текст:')
        self.label_instruction.setStyleSheet("""font: bold""")

        self.format = QTextCharFormat()
        self.format.setForeground(QColor("black"))

        self.format_green = QTextCharFormat()
        self.format_green.setForeground(QColor("green"))

        self.format_red = QTextCharFormat()
        self.format_red.setForeground(QColor("red"))

        self.text_for_typing = QTextEdit(self)
        self.text_for_typing.setEnabled(False)
        self.text_for_typing.setReadOnly(True)
        self.text_for_typing.setStyleSheet("""color: rgb(0,0,0)""")

        self.area_for_typing = QTextEdit(self)
        self.area_for_typing.setPlaceholderText('Введите текст...')
        self.area_for_typing.document().contentsChange.connect(self.check_text)

        self.start_button = QPushButton('Начать тест снова')
        self.start_button.clicked.connect(self.start_test)
        self.start_button.setStyleSheet('background: rgb(227,184,109)')

        self.backward_button = QPushButton('Назад')
        self.backward_button.clicked.connect(self.back)
        self.backward_button.setStyleSheet('background: rgb(227,184,109)')
        self.backward_button.setStyleSheet("background-color: rgb(227, 184, 109); font: bold;")

        self.result_label = QLabel('Результат: -')
        self.result_label.setStyleSheet("""font: bold""")

        self.best_result_label = QLabel('Лучший результат: -')
        self.best_result_label.setStyleSheet("""font: bold""")

        # Организуем компоновку
        layout = QVBoxLayout()
        layout.addWidget(self.label_instruction)
        layout.addWidget(self.text_for_typing)
        layout.addWidget(self.area_for_typing)
        layout.addWidget(self.start_button)
        layout.addWidget(self.result_label)
        layout.addWidget(self.best_result_label)
        layout.addWidget(self.backward_button)

        self.setLayout(layout)

        self.timer = QTime()
        self.elapsed_time = 0

        self.insert_russian_text()
        self.insert_english_text()

    # Диалоговое окно
    def run(self):
        self.text_for_typing.setText('')
        self.result_label.setText('Результат: -')
        self.best_result_label.setText('Лучший результат: -')

        self.name, ok_pressed = QInputDialog.getText(self, "Введите имя",
                                                "Как тебя зовут?")
        self.start_test()

    def insert_russian_text(self):
        try:
            file = open('texts.txt', 'w')
            file.write('Байкал всегда был привлекателен для туристов. С каждым годом интерес к самому '
                        'глубокому пресному озеру мира набирает обороты: создаются новые маршруты, '
                        'улучшается качество сервиса, оптимизируется транспортное сообщение.\n')
            file.write('Лев Николаевич Толстой - один из наиболее известных русских писателей и мыслителей, '
                        'один из величайших в мире писателей-романистов. Писатель, ещё при жизни признанный главой '
                       'русской литературы. Творчество Толстого ознаменовало новый этап в русском и мировом реализме.\n')
            file.write('Классицизм - художественный стиль и эстетическое направление в европейской культуре. '
                        'Классицизм является мировоззрением, идеологией, отражающей естественное стремление человека '
                        'к красоте, целостности, простоте и ясности содержания и формы.')
            file.close()
        except Exception as e:
            print(f"Error: {e}")

    def insert_english_text(self):
        try:
            file = open('texts2.txt', 'w')
            file.write('The River Thames, known alternatively in parts as the River Isis, is a river that '
                       'flows through southern England including London. At 215 miles, '
                       'it is the longest river entirely in England and the second-longest in the United Kingdom, '
                       'after the River Severn.\n')
            file.write('Pollution, also called environmental pollution, the addition of any substance'
                       ' or any form of energy to the environment at a rate faster than it can be dispersed, diluted, '
                       'decomposed, recycled, or stored in some harmless form.\n')
            file.write('Pablo Ruiz Picasso was a Spanish painter, sculptor, printmaker, ceramicist and theatre designer '
                       'who spent most of his adult life in France. One of the most influential artists of the 20th century, '
                       'he is known for co-founding the Cubist movement.')
            file.close()
        except Exception as e:
            print(f"Error: {e}")

    # Выбриаем текст
    def generate_random_text(self):
        try:
            if self.selected_language == 'Русский':
                file = open('texts.txt', 'r')
            else:
                file = open('texts2.txt', 'r')

            texts = ['\n'.join(el.split('\t')) for el in file.readlines()]
            file.close()
            #random_text = random.choice(texts)
            random_text = 'py'

        except Exception as e:
            print(f"Error: {e}")
            random_text = ''

        return random_text

    def start_test(self):
        language_selection_window = LanguageSelectionWindow(self)
        result = language_selection_window.exec_()

        self.show_result_message = True

        if result == QDialog.Accepted:
            try:
                self.selected_language = language_selection_window.selected_language

            except Exception as e:
                print(f"Error: {e}")
                self.selected_language = 'Русский'
        else:
            self.selected_language = 'Русский'

        self.text = self.generate_random_text()
        self.text_for_typing.setText(self.text)

        self.result_label.setText('Результат: -')
        self.best_result_label.setText('Лучший результат: -')
        self.area_for_typing.clear()
        self.area_for_typing.setFocus()

        self.flag = True
        self.area_for_typing.document().contentsChange.connect(self.timer_start)

    def timer_start(self):
        if self.flag:
            self.timer.start()
            self.flag = False

    # Вычисление результата
    def check_text(self,  position, charsRemoved, charsAdded):
        input_text = self.area_for_typing.toPlainText()
        cursor = self.text_for_typing.textCursor()
        if len(self.text) >= len(input_text):
            cursor.setPosition(position)
        end = cursor.movePosition(QTextCursor.NextCharacter, 1)

        # Меняем цвет удаленных символов
        if charsRemoved:
            if len(self.text) > len(input_text):
                cursor.setPosition(position + 1)
                cursor.movePosition(QTextCursor.Left, QTextCursor.KeepAnchor, charsRemoved)
                cursor.mergeCharFormat(self.format)
                end = False

        # Результат
        if input_text == self.text_for_typing.toPlainText():
            cursor.mergeCharFormat(self.format_green)
            self.elapsed_time = self.timer.elapsed() / 60000.0
            speed = int(len(input_text) / self.elapsed_time)
            speed_word = self.get_word_form(speed, 'символ')
            self.result_label.setText(f'Результат: {speed} {speed_word} в минуту')
            DBSample.insert_rating(self.db, self.name, speed, self.selected_language)
            db = sqlite3.connect('rating.db')

            cursor = db.cursor()
            cursor.execute(f"SELECT MAX(скорость) FROM рейтинг_{self.selected_language.lower()} WHERE имя = ?", (self.name,))
            result = cursor.fetchone()
            self.best_result_label.setText(f'Лучший результат: {result[0]} {speed_word} в минуту')
            self.rating_window.paint_table()

            # Всплывающее окно
            if self.show_result_message:
                result_message = QMessageBox(self)
                result_message.setWindowTitle('Результат теста')

                if speed <= 250:
                    result_message.setText(f'Ты хорош, но лучше еще немного потренироваться!\nТвой результат: {speed} {speed_word} в минуту')
                elif 250 < speed <= 300:
                    result_message.setText(f'Молодец! У тебя хороший уровень печати!\nТвой результат: {speed} {speed_word} в минуту')
                elif 300 < speed <= 500:
                    result_message.setText(f'Отлично! Твои результаты впечатляют!\nТвой результат: {speed} {speed_word} в минуту')
                else:
                    result_message.setText(f'Ты печатаешь со сверхзвуковой скоростью!\nТвой результат: {speed} {speed_word} в минуту')

                pixmap = QPixmap('zvezda.png')
                result_message.setIconPixmap(pixmap)

                result_message.exec_()
                self.show_result_message = False
        else:
            # Изменение цвета текста
            try:
                if end:
                    for i in range(min(len(input_text), len(self.text))):
                        if input_text[i] == self.text[i] and charsAdded:
                            cursor.mergeCharFormat(self.format_green)
                        else:
                            cursor.mergeCharFormat(self.format_red)
                    self.text_for_typing.show()
            except Exception as e:
                print(f"Error: {e}")

    def get_word_form(self, number, word):
        number = abs(number) % 100
        remainder = number % 10
        if 10 < number < 20:
            return word + 'ов'
        if 1 < remainder < 5:
            return word + 'а'
        if remainder == 1:
            return word
        return word + 'ов'

    # Переключение на основное окно
    def back(self):
        self.stacked_widget.setCurrentIndex(0)
        self.area_for_typing.clear()


# Окно выбора языка для прохожденя теста
class LanguageSelectionWindow(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.init_ui()

    def init_ui(self):
        # Создаем виджеты и устанавливаем их параметры
        self.setWindowTitle('Выбор языка')
        layout = QVBoxLayout()

        label = QLabel('Выберите язык для теста:')
        layout.addWidget(label)

        # Группа для радиокнопок
        group = QButtonGroup(self)

        russian_button = QRadioButton('Русский')
        layout.addWidget(russian_button)
        group.addButton(russian_button)

        english_button = QRadioButton('Английский')
        layout.addWidget(english_button)
        group.addButton(english_button)

        confirm_button = QPushButton('Продолжить')
        confirm_button.clicked.connect(self.confirm_selection)
        layout.addWidget(confirm_button)

        self.setLayout(layout)

    # Определение выбранного языка
    def confirm_selection(self):
        for button in self.findChildren(QRadioButton):
            if button.isChecked():
                self.selected_language = button.text()
                break

        self.accept()


# Окно рейтинга
class RatingWindow(QWidget):
    def __init__(self, stacked_widget, dbsample):
        super().__init__()

        self.db = dbsample
        self.stacked_widget = stacked_widget
        self.init_ui()

    def init_ui(self):
        # Создаем виджеты и устанавливаем их параметры
        label_rating = QLabel('Рейтинговая таблица')
        label_rating.setAlignment(Qt.AlignCenter)
        label_rating.setStyleSheet("""font: bold""")

        layout = QVBoxLayout()
        layout1 = QHBoxLayout()

        self.table_widget = QTableWidget(self)
        self.table_widget.setColumnCount(4)
        self.table_widget.setHorizontalHeaderLabels(['Имя (RU)', 'Скорость (RU)', 'Имя (EN)', 'Скорость (EN)'])

        self.db_connection = sqlite3.connect("rating.db")
        self.paint_table()

        self.backward_button = QPushButton('Назад')
        self.backward_button.clicked.connect(self.back)
        self.backward_button.setStyleSheet("background-color: rgb(227, 184, 109); font: bold;")

        self.clear_button = QPushButton('Очистить рейтинг')
        self.clear_button.clicked.connect(self.clear)
        self.clear_button.setStyleSheet('background: rgb(227,184,109)')

        # Организуем компоновку
        layout1.addWidget(self.backward_button)
        layout1.addWidget(self.clear_button)

        layout.addWidget(label_rating)
        layout.addWidget(self.table_widget, alignment=Qt.AlignHCenter)
        layout.addLayout(layout1)

        self.setLayout(layout)

    # Метод для отрисовки таблицы рейтинга
    def paint_table(self):
        cursor_ru = self.db_connection.cursor()
        cursor_ru.execute("SELECT * FROM рейтинг_русский ORDER BY скорость DESC LIMIT 10")  # Загружаем топ-10 рейтингов
        data_ru = cursor_ru.fetchall()

        cursor_en = self.db_connection.cursor()
        cursor_en.execute("SELECT * FROM рейтинг_английский ORDER BY скорость DESC LIMIT 10")  # Загружаем топ-10 рейтингов
        data_en = cursor_en.fetchall()

        max_len = max(len(data_ru), len(data_en))

        self.table_widget.setRowCount(max_len)

        for row_index in range(max_len):
            if row_index < len(data_ru):
                for col_index, col_data in enumerate(data_ru[row_index]):
                    item = QTableWidgetItem(str(col_data))
                    item.setFlags(item.flags() ^ Qt.ItemIsEditable)
                    self.table_widget.setItem(row_index, col_index, item)

            if row_index < len(data_en):
                for col_index, col_data in enumerate(data_en[row_index]):
                    item = QTableWidgetItem(str(col_data))
                    item.setFlags(item.flags() ^ Qt.ItemIsEditable)
                    self.table_widget.setItem(row_index, col_index + 2, item)

        self.table_widget.resizeColumnsToContents()
        self.table_widget.resizeRowsToContents()
        width = sum(self.table_widget.columnWidth(col) for col in range(4))
        self.table_widget.setFixedWidth(width + 20)

    # Переключение на основное окно
    def back(self):
        self.stacked_widget.setCurrentIndex(0)

    # Очистка рейтинговой таблицы
    def clear(self):
        try:
            with sqlite3.connect('rating.db') as connection:
                cursor = connection.cursor()
                cursor.execute(f"DELETE FROM рейтинг_английский")
                cursor.execute(f"DELETE FROM рейтинг_русский")
                connection.commit()
        except sqlite3.Error as e:
            print(f"Error clearing table: {e}")
        self.paint_table()


# Окно для работы с базой данных
class DBSample(QMainWindow):
    def __init__(self):
        super().__init__()
        try:
            self.connection = sqlite3.connect("rating.db")
            self.cursor = self.connection.cursor()
            # Создаем таблицы рейтинга, если ее нет
            self.cursor.execute('''CREATE TABLE IF NOT EXISTS рейтинг_английский (
                                                        имя TEXT,
                                                        скорость INTEGER)''')
            self.cursor.execute('''CREATE TABLE IF NOT EXISTS рейтинг_русский (
                                                        имя TEXT,
                                                        скорость INTEGER)''')
        except sqlite3.Error as e:
            print("Error creating table:", e)

        self.connection.commit()

    # Метод для добавления рейтинга в базу данных
    def insert_rating(self, username, speed, language):
        try:
            table_name = f"рейтинг_{language.lower()}"
            self.cursor.execute(f"INSERT INTO {table_name} (имя, скорость) VALUES (?, ?)", (username, speed))
            self.connection.commit()
        except sqlite3.Error as e:
            print("Error inserting rating:", e)

    # Закрытие базы данных при завершении работы приложения
    def close_database(self):
        if self.connection:
            self.connection.close()


if __name__ == '__main__':
    app = QApplication(sys.argv)

    dbsample = DBSample()

    stacked_widget = QStackedWidget()

    rating_window = RatingWindow(stacked_widget, dbsample)
    typing_test_window = TypingTestWindow(stacked_widget, dbsample, rating_window)
    welcome_window = MainWindow(stacked_widget, typing_test_window)

    stacked_widget.addWidget(welcome_window)
    stacked_widget.addWidget(typing_test_window)
    stacked_widget.addWidget(rating_window)

    stacked_widget.show()

    sys.exit(app.exec_())