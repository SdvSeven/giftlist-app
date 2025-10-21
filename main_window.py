from database import Database
from PyQt6.QtCore import Qt
from PyQt6 import uic
from PyQt6.QtWidgets import (
    QMainWindow, QDialog, QVBoxLayout, QFormLayout, QLineEdit, 
    QSpinBox, QCheckBox, QPushButton, QMessageBox, QTableWidgetItem
)

class GiftDialog(QDialog):
    def __init__(self, parent=None, data=None):
        super().__init__(parent)
        self.setWindowTitle("Идея подарка")
        self.data = data
        self.title = QLineEdit()
        self.person = QLineEdit()
        self.occasion = QLineEdit()
        self.priority = QSpinBox()
        self.priority.setRange(1, 5)
        self.purchased = QCheckBox("Куплено")

        form = QFormLayout()
        form.addRow("Название:", self.title)
        form.addRow("Кому:", self.person)
        form.addRow("Повод:", self.occasion)
        form.addRow("Приоритет:", self.priority)
        form.addRow(self.purchased)

        btnSave = QPushButton("Сохранить")
        btnSave.clicked.connect(self.accept)

        layout = QVBoxLayout()
        layout.addLayout(form)
        layout.addWidget(btnSave)
        self.setLayout(layout)

        if data:
            self.title.setText(data[1])
            self.person.setText(data[2])
            self.occasion.setText(data[3])
            self.priority.setValue(int(data[4]))
            self.purchased.setChecked(bool(data[5]))

    def get_data(self):
        return (
            self.title.text(),
            self.person.text(),
            self.occasion.text(),
            self.priority.value(),
            int(self.purchased.isChecked())
        )


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi("ui/main_window.ui", self)
        self.db = Database()
        self.load_data()

        # Кнопки
        self.btnAdd.clicked.connect(self.add_item)
        self.btnDelete.clicked.connect(self.delete_item)

        # Поиск
        self.searchBtn.clicked.connect(self.search)
        self.searchEdit.returnPressed.connect(self.search)

        # Редактирование по двойному клику
        self.tableWidget.itemDoubleClicked.connect(self.edit_item)

    def load_data(self, data=None):
        """Загрузка данных в таблицу. Если data не передано, загружаем все записи"""
        if data is None:
            data = self.db.fetch_all()

        self.tableWidget.setRowCount(0)
        self.tableWidget.setColumnCount(6)
        self.tableWidget.setHorizontalHeaderLabels(
            ["ID", "Название", "Кому", "Повод", "Приоритет", "Куплено"]
        )

        for row_data in data:
            row = self.tableWidget.rowCount()
            self.tableWidget.insertRow(row)
            for col, val in enumerate(row_data):
                self.tableWidget.setItem(row, col, QTableWidgetItem(str(val)))

        self.tableWidget.sortItems(4, Qt.SortOrder.DescendingOrder)

    def add_item(self):
        dlg = GiftDialog(self)
        if dlg.exec():
            data = dlg.get_data()
            if not data[0]:
                QMessageBox.warning(self, "Ошибка", "Название обязательно")
                return
            self.db.add(*data)
            self.load_data()

    def edit_item(self):
        row = self.tableWidget.currentRow()
        if row < 0:
            QMessageBox.information(self, "Редактировать", "Выберите запись")
            return
        gift_id = int(self.tableWidget.item(row, 0).text())
        data = [self.tableWidget.item(row, i).text() for i in range(6)]
        dlg = GiftDialog(self, data)
        if dlg.exec():
            new_data = dlg.get_data()
            self.db.update(gift_id, *new_data)
            self.load_data()

    def delete_item(self):
        row = self.tableWidget.currentRow()
        if row < 0:
            QMessageBox.information(self, "Удалить", "Выберите запись")
            return
        gift_id = int(self.tableWidget.item(row, 0).text())
        reply = QMessageBox.question(
            self, "Удаление", "Удалить запись?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        if reply == QMessageBox.StandardButton.Yes:
            self.db.delete(gift_id)
            self.load_data()

    def search(self):
        """Поиск по Названию, Кому или Поводу"""
        query = self.searchEdit.text().strip().lower()
        if not query:
            self.load_data()
            return

        all_data = self.db.fetch_all()
        filtered = [
            row for row in all_data
            if query in str(row[1]).lower()  # Название
            or query in str(row[2]).lower()  # Кому
            or query in str(row[3]).lower()  # Повод
        ]
        self.load_data(filtered)
