import sqlite3
import sys

from PyQt5 import uic
from PyQt5.QtSql import QSqlDatabase, QSqlTableModel
from PyQt5.QtWidgets import QApplication, QMainWindow, QTableView


class Linux(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('main.ui', self)
        self.con = sqlite3.connect('coffee.sqlite')
        self.initUI()

    def initUI(self):
        db = QSqlDatabase.addDatabase('QSQLITE')
        # Укажем имя базы данных
        db.setDatabaseName('coffee.sqlite')
        # И откроем подключение
        db.open()

        # QTableView - виджет для отображения данных из базы
        # Создадим объект QSqlTableModel,
        # зададим таблицу, с которой он будет работать,
        #  и выберем все данные
        model = QSqlTableModel(self, db)
        model.setTable('Кофе')
        model.select()

        # Для отображения данных на виджете
        # свяжем его и нашу модель данных
        self.tableView.setModel(model)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Linux()
    ex.show()
    sys.exit(app.exec_())