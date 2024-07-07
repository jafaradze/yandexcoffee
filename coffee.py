import sqlite3
from PyQt5 import QtWidgets, uic
import sys


class CoffeeApp(QtWidgets.QMainWindow):
    def __init__(self):
        super(CoffeeApp, self).__init__()
        uic.loadUi('main.ui', self)
        self.setWindowTitle("Капучино")
        self.queryButton.clicked.connect(self.load_data)
        self.addButton.clicked.connect(self.open_add_edit_form)
        self.editButton.clicked.connect(self.open_add_edit_form)
        self.coffeeTable.setColumnCount(7)
        self.coffeeTable.setHorizontalHeaderLabels(['ID', 'Название сорта', 'Степень обжарки', 'Молотый/в зернах', 'Описание вкуса', 'Цена', 'Объем упаковки'])
        self.coffeeTable.setRowCount(0)
        self.coffeeTable.setColumnWidth(0, 50)
        self.coffeeTable.setColumnWidth(2, 125)
        self.coffeeTable.setColumnWidth(3, 125)
        self.coffeeTable.setColumnWidth(4, 200)
        self.coffeeTable.setColumnWidth(5, 50)

        self.load_data()


    def open_add_edit_form(self):
        button = self.sender()
        add_mode = button == self.addButton
        dialog = AddEditCoffeeForm(add_mode, self)
        dialog.exec_()

        
    def load_data(self):
        con = sqlite3.connect('coffee.sqlite')
        cur = con.cursor()
        cur.execute('SELECT * FROM coffee')
        rows = cur.fetchall()

        self.coffeeTable.clearContents()
        self.coffeeTable.setRowCount(0)

        for row in rows:
            row_position = self.coffeeTable.rowCount()
            self.coffeeTable.insertRow(row_position)
            for i, value in enumerate(row):
                self.coffeeTable.setItem(row_position, i, QtWidgets.QTableWidgetItem(str(value)))
        con.close()


class AddEditCoffeeForm(QtWidgets.QDialog):
    def __init__(self, add_mode, parent=None):
        super(AddEditCoffeeForm, self).__init__(parent)
        uic.loadUi('addEditCoffeeForm.ui', self)
        
        self.add_mode = add_mode
        self.parent = parent
        
        if not self.add_mode:
            selected_row = self.parent.coffeeTable.currentRow()
            if selected_row < 0:
                self.close()
                return

            self.coffee_id = self.parent.coffeeTable.item(selected_row, 0).text()
            self.nameEdit.setText(self.parent.coffeeTable.item(selected_row, 1).text())
            self.roastDegreeEdit.setText(self.parent.coffeeTable.item(selected_row, 2).text())
            self.groundOrBeansEdit.setText(self.parent.coffeeTable.item(selected_row, 3).text())
            self.descriptionEdit.setText(self.parent.coffeeTable.item(selected_row, 4).text())
            self.priceEdit.setValue(float(self.parent.coffeeTable.item(selected_row, 5).text()))
            self.packageSizeEdit.setText(self.parent.coffeeTable.item(selected_row, 6).text())
        
        self.saveButton.clicked.connect(self.save_data)

    def save_data(self):
        
        name = self.nameEdit.text()
        roast_degree = self.roastDegreeEdit.text()
        ground_or_beans = self.groundOrBeansEdit.text()
        description = self.descriptionEdit.text()
        price = self.priceEdit.value()
        package_size = self.packageSizeEdit.text()

        con = sqlite3.connect('coffee.sqlite')
        cur = con.cursor()
        if self.add_mode:
            cur.execute('INSERT INTO coffee (name, roast_degree, ground_or_beans, description, price, package_size) VALUES (?, ?, ?, ?, ?, ?)',
                           (name, roast_degree, ground_or_beans, description, price, package_size))
        else:
            cur.execute('UPDATE coffee SET name=?, roast_degree=?, ground_or_beans=?, description=?, price=?, package_size=? WHERE id=?',
                           (name, roast_degree, ground_or_beans, description, price, package_size, self.coffee_id))
        
        con.commit()
        con.close()
        
        self.parent.load_data()
        self.close()


app = QtWidgets.QApplication(sys.argv)
window = CoffeeApp()
window.show()
sys.exit(app.exec_())
