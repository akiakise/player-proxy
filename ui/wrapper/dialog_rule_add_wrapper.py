from PyQt5.QtCore import pyqtSlot, pyqtSignal
from PyQt5.QtWidgets import QDialog, QFileDialog, QMessageBox

from config import load_config, write_config, Rule
from ui.source.dialog_rule import Ui_Dialog
from util.file_util import get_windows_path, is_folder, is_application


class DialogRuleAddWrapper(QDialog, Ui_Dialog):
    closed = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.title = 'Add Rule'
        self.folder = 'Please choose a folder'
        self.app = 'Please choose a application to open videos under the folder'

        self.draw_ui()
        self.connect()

    def draw_ui(self):
        self.label_folder_value.setText(self.folder)
        self.label_folder_value.setToolTip(self.folder)
        self.label_folder_value.setStyleSheet('QLabel{color:blue;padding-left:5px;}')
        self.label_app_value.setText(self.app)
        self.label_app_value.setToolTip(self.app)
        self.label_app_value.setStyleSheet('QLabel{color:blue;padding-left:5px;}')

    def connect(self):
        self.label_folder_value.clicked.connect(self.slot_label_folder_clicked)
        self.label_app_value.clicked.connect(self.slot_label_app_clicked)
        self.pushButton_confirm.clicked.connect(self.slot_button_confirm_clicked)
        self.pushButton_cancel.clicked.connect(self.slot_button_close_clicked)

    @pyqtSlot()
    def slot_label_folder_clicked(self):
        folder = QFileDialog.getExistingDirectory()
        if not folder:
            return
        self.folder = get_windows_path(folder)
        self.draw_ui()

    @pyqtSlot()
    def slot_label_app_clicked(self):
        app = QFileDialog.getOpenFileName(filter='exe(*.exe)')[0]
        if not app:
            return
        self.app = get_windows_path(app)
        self.draw_ui()

    @pyqtSlot()
    def slot_button_confirm_clicked(self):
        if not is_folder(self.folder):
            QMessageBox.critical(self, self.title, 'Please choose a folder!')
            return
        if not is_application(self.app):
            QMessageBox.critical(self, self.title, 'Please choose a application!')
            return
        config = load_config()
        max_index = max([rule.index for rule in config.rules] + [-1])
        config.rules.append(Rule(max_index + 1, self.folder, self.app))
        write_config(config)
        self.slot_button_close_clicked()

    @pyqtSlot()
    def slot_button_close_clicked(self):
        self.closed.emit()
        self.close()
