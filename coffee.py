import sqlite3
from PyQt5 import QtWidgets, uic
import sys


class CoffeeApp(QtWidgets.QMainWindow):
    def __init__(self):
        super(CoffeeApp, self).__init__()
        uic.loadUi('main.ui', self)
        self.setWindowTitle("Эспрессо")
        self.queryButton.clicked.connect(self.load_data)
        self.coffeeTable.setColumnCount(7)
        self.coffeeTable.setHorizontalHeaderLabels(["ID", "Название сорта", "Степень обжарки", "Молотый/в зернах", "Описание вкуса", "Цена", "Объем упаковки"])
        self.coffeeTable.setRowCount(0)
        self.coffeeTable.setColumnWidth(0, 50)
        self.coffeeTable.setColumnWidth(2, 125)
        self.coffeeTable.setColumnWidth(3, 125)
        self.coffeeTable.setColumnWidth(4, 200)
        self.coffeeTable.setColumnWidth(5, 50)
        
    def load_data(self):
        connection = sqlite3.connect('coffee.sqlite')
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM coffee")
        rows = cursor.fetchall()

        for row in rows:
            row_position = self.coffeeTable.rowCount()
            self.coffeeTable.insertRow(row_position)
            for i, value in enumerate(row):
                self.coffeeTable.setItem(row_position, i, QtWidgets.QTableWidgetItem(str(value)))
        connection.close()


app = QtWidgets.QApplication(sys.argv)
window = CoffeeApp()
window.show()
sys.exit(app.exec_())
