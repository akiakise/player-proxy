from PyQt5.QtCore import pyqtSlot, pyqtSignal
from PyQt5.QtWidgets import QDialog, QLineEdit, QMessageBox

from config import load_config, write_config
from ui.source.dialog_rule import Ui_Dialog


class DialogNewIndexWrapper(QDialog, Ui_Dialog):
    closed = pyqtSignal()

    def __init__(self, origin_index):
        super().__init__()
        self.setupUi(self)

        self.title = 'Change Index'
        self.lineEdit_NewIndex = QLineEdit()
        self.origin_index = origin_index

        self.draw_ui()
        self.connect()

    def draw_ui(self):
        self.setWindowTitle(self.title)
        self.label_folder.hide()
        self.label_folder_value.hide()
        self.label_app.setText('New index: ')
        self.gridLayout.removeWidget(self.label_app_value)
        self.gridLayout.addWidget(self.lineEdit_NewIndex, 1, 1, 1, 1)
        self.lineEdit_NewIndex.setFocus()

    def connect(self):
        self.pushButton_confirm.clicked.connect(self.slot_button_confirm_clicked)
        self.pushButton_cancel.clicked.connect(self.slot_button_cancel_clicked)

    @pyqtSlot()
    def slot_button_confirm_clicked(self):
        index = None
        text = self.lineEdit_NewIndex.text()

        # 1. Convert string index to int
        try:
            index = int(text)
        except:
            QMessageBox.critical(self, self.title, f'Invalid input: {text}!')
            self.lineEdit_NewIndex.setText('')
            self.lineEdit_NewIndex.setFocus()
            return

        # 2. Load config
        config = load_config()

        # 3. Check index range
        if index >= len(config.rules):
            QMessageBox.critical(self, self.title, f'Invalid index: {index}')
            self.lineEdit_NewIndex.setText('')
            self.lineEdit_NewIndex.setFocus()
            return

        # 4. Change index
        config.rules[index].index, config.rules[self.origin_index].index = config.rules[self.origin_index].index, config.rules[index].index
        write_config(config)

        # 5. Over
        self.slot_button_cancel_clicked()

    @pyqtSlot()
    def slot_button_cancel_clicked(self):
        self.closed.emit()
        self.close()
