import sqlite3
import sys

from PyQt5 import uic
from PyQt5.QtSql import QSqlDatabase, QSqlTableModel
from PyQt5.QtWidgets import QApplication, QMainWindow, QTableView, QMessageBox, QTableWidgetItem


class Linux(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('main.ui', self)
        self.connection = sqlite3.connect('coffee.sqlite')
        self.pushButton.clicked.connect(self.to_create)
        self.pushButton_2.clicked.connect(self.save_results)
        self.modified = {}
        self.titles = ['id', 'название сорта', 'степень обжарки', 'молотый',
                       'описание вкуса', 'цена', 'объем упаковки(в мл)']
        self.select_data()

    def select_data(self):
        # Получим результат запроса,
        # который ввели в текстовое поле
        query = 'SELECT * FROM Кофе'
        res = self.connection.cursor().execute(query).fetchall()
        # Заполним размеры таблицы
        self.tableWidget.setColumnCount(7)
        self.tableWidget.setRowCount(0)
        # Заполняем таблицу элементами
        for i, row in enumerate(res):
            self.tableWidget.setRowCount(
                self.tableWidget.rowCount() + 1)
            for j, elem in enumerate(row):
                self.tableWidget.setItem(
                    i, j, QTableWidgetItem(str(elem)))
        self.tableWidget.itemChanged.connect(self.item_changed)

    def to_create(self):
        self.w1 = AddEditCoffee()
        self.w1.main_label.setText('Создайте новый вид кофе')
        self.w1.show()
        self.close()

    def item_changed(self, item):
        print(self.modified)
        # Если значение в ячейке было изменено,
        # то в словарь записывается пара: название поля, новое значение
        self.modified[self.titles[item.column()]] = item.text()


    def save_results(self):
        if self.modified:
            cur = self.connection.cursor()
            que = "UPDATE films SET\n"
            que += ", ".join([f"{key}='{self.modified.get(key)}'"
                              for key in self.modified.keys()])
            print(que)
            cur.execute(que)
            self.connection.commit()
            self.modified.clear()

    def closeEvent(self, event):
        # При закрытии формы закроем и наше соединение
        # с базой данных
        self.connection.close()


class AddEditCoffee(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('addEditCoffeeForm.ui', self)
        self.pushButton.clicked.connect(self.addcoffee)

    def addcoffee(self):
        pass


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Linux()
    ex.show()
    sys.exit(app.exec_())