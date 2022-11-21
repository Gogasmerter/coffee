import os
import sqlite3
import sys

import pandas as pd
from PyQt5 import uic
from PyQt5.QtSql import QSqlDatabase, QSqlTableModel
from PyQt5.QtWidgets import QApplication, QMainWindow, QTableView, QMessageBox, QTableWidgetItem, QInputDialog, \
    QTableWidget

from windows import MainWindowFORM, AddEditCoffeeFORM


class Linux(QMainWindow, MainWindowFORM):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setFixedSize(self.size())
        self.tableWidget: QTableWidget
        self.connection = sqlite3.connect('data/coffee.sqlite')
        self.pushButton.clicked.connect(self.to_create)
        self.pushButton_2.clicked.connect(self.save_results)
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

    def save_results(self):
        proceed = QMessageBox.question(self,
                                       'Information',
                                       'Have you Verified your Data?',
                                       QMessageBox.Yes | QMessageBox.No,
                                       QMessageBox.No)
        if proceed != QMessageBox.Yes:
            return

        self.saveToDb()

    def saveToDb(self):
        d = {}
        columns = ['id', 'название_сорта', 'степень_обжарки', 'молотый', 'описание_вкуса', 'цена', 'объем_упаковки_в_мл']
        print(self.tableWidget)
        for i in range(self.tableWidget.columnCount()):
            l = []
            for j in range(self.tableWidget.rowCount()):
                it = self.tableWidget.item(j, i)
                l.append(it.text() if it is not None else "")
            print(l)
            h_item = self.tableWidget.horizontalHeaderItem(i)
            n_column = columns[i]
            d[n_column] = l
        print(d)
        df = pd.DataFrame(data=d)
        print(df)
        self.connection.close()
        os.remove('data/coffee.sqlite')
        engine = sqlite3.connect('data/coffee.sqlite')
        print(engine)
        df.to_sql('Кофе', con=engine, index=False)
        self.restart()

    def to_create(self):
        self.w1 = AddEditCoffee()
        self.w1.main_label.setText('Создайте новый вид кофе')
        self.w1.show()
        self.close()

    def restart(self):
        self.w1 = Linux()
        self.w1.show()
        self.close()

    def closeEvent(self, event):
        self.connection.close()


class AddEditCoffee(QMainWindow, AddEditCoffeeFORM):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.connection = sqlite3.connect('data/coffee.sqlite')
        self.setFixedSize(self.size())
        self.pushButton.clicked.connect(self.addcoffee)
        self.back_button.clicked.connect(self.back)

    def addcoffee(self):
        cur = self.connection.cursor()

        index = int(sorted(cur.execute('''SELECT id FROM Кофе''').fetchall(), key=lambda x: int(x[0]))[-1][0]) + 1

        sname = self.lineEdit.text()
        cb = self.comboBox.currentText()
        ck = self.checkBox.isChecked()
        te = self.textEdit.toPlainText()
        price = self.lineEdit_2.text()
        V = self.lineEdit_3.text()
        if not sname:
            self.statusbar.showMessage('Введите название сорта')
            return
        if not price:
            self.statusbar.showMessage('Введите цену')
            return
        if not V:
            self.statusbar.showMessage('Введите объём')
            return
        if not price.isdigit():
            self.statusbar.showMessage('Цена должна быть числом')
            return
        if not V.isdigit():
            self.statusbar.showMessage('Объём должен быть числом')
            return

        print(1)
        cur.execute(f"""INSERT INTO Кофе VALUES('{index}', '{sname}', '{cb}', '{1 if ck else 0}', '{te}', '{price}', '{V}')""")
        print(2)
        self.connection.commit()

        self.back()

    def back(self):
        self.w1 = Linux()
        self.w1.show()
        self.close()

    def closeEvent(self, event):
        self.connection.close()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Linux()
    ex.show()
    sys.exit(app.exec_())
