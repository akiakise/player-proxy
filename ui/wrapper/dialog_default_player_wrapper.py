from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import QDialog, QFileDialog, QMessageBox

from config import load_config, write_config
from ui.source.dialog_default_player import Ui_Dialog
from util.file_util import get_windows_path, is_application


class DialogDefaultPlayerWrapper(QDialog, Ui_Dialog):
    def __init__(self) -> None:
        super().__init__()
        self.setupUi(self)

        self.title = 'Update default player'
        self.config = load_config()
        self.default_player = self.config.fallback

        self.draw_ui()
        self.connect()

    def draw_ui(self):
        if self.default_player:
            self.label_default_player.setText(self.default_player)
        else:
            self.label_default_player.setText('Please set default player')
        self.label_default_player.setStyleSheet('QLabel{color:blue;padding-left:5px;}')

    def connect(self):
        self.label_default_player.clicked.connect(self.slot_label_folder_clicked)
        self.button_confirm.clicked.connect(self.slot_button_confirm_clicked)
        self.button_cancel.clicked.connect(self.slot_button_cancel_clicked)

    @pyqtSlot()
    def slot_label_folder_clicked(self):
        app = QFileDialog.getOpenFileName()[0]
        if not app:
            QMessageBox.critical(self, self.title, 'Please choose a player!')
            self.draw_ui()
            return
        app_path = get_windows_path(app)
        if not is_application(app_path):
            QMessageBox.critical(self, self.title, f'Not a valid player: {app_path}')
            self.draw_ui()
            return
        self.default_player = app_path
        self.draw_ui()

    @pyqtSlot()
    def slot_button_confirm_clicked(self):
        if not is_application(self.default_player):
            QMessageBox.critical(self, self.title, f'Not a valid player: {self.default_player}')
            self.draw_ui()
            return
        current_config = load_config()
        current_config.fallback = self.default_player
        write_config(current_config)
        self.close()

    @pyqtSlot()
    def slot_button_cancel_clicked(self):
        self.close()
