from PyQt5.QtCore import pyqtSlot, pyqtSignal
from PyQt5.QtWidgets import QDialog, QFileDialog

from config import load_config, write_config
from ui.source.dialog_rule import Ui_Dialog
from util.file_util import get_windows_path


class DialogRuleEditWrapper(QDialog, Ui_Dialog):
    closed = pyqtSignal()

    def __init__(self, folder, app):
        super().__init__()
        self.setupUi(self)

        self.folder = folder
        self.app = app

        self.draw_ui()
        self.connect()

    def draw_ui(self):
        self.label_folder_value.setText(self.folder)
        self.label_folder_value.setToolTip(self.folder)
        self.label_app_value.setText(self.app)
        self.label_app_value.setToolTip(self.app)
        self.label_app_value.setStyleSheet('QLabel{color:blue;padding-left:5px;}')

    def connect(self):
        self.label_app_value.clicked.connect(self.slot_label_app_clicked)
        self.pushButton_confirm.clicked.connect(self.slot_button_confirm_clicked)
        self.pushButton_cancel.clicked.connect(self.slot_button_close_clicked)

    @pyqtSlot()
    def slot_label_app_clicked(self):
        app = QFileDialog.getOpenFileName()[0]
        if not app:
            return
        self.app = get_windows_path(app)
        self.draw_ui()

    @pyqtSlot()
    def slot_button_confirm_clicked(self):
        config = load_config()
        for rule_config in config['rules']:
            if rule_config['folder'] == self.folder:
                rule_config['app'] = get_windows_path(self.app)
        write_config(config)
        self.slot_button_close_clicked()

    @pyqtSlot()
    def slot_button_close_clicked(self):
        self.closed.emit()
        self.close()
