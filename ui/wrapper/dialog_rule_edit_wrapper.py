from PyQt5.QtCore import pyqtSlot, pyqtSignal
from PyQt5.QtWidgets import QDialog, QFileDialog, QMessageBox, QComboBox

from config import load_config, write_config
from ui.source.dialog_rule import Ui_Dialog
from util.file_util import get_windows_path, is_folder, is_application


class DialogRuleEditWrapper(QDialog, Ui_Dialog):
    closed = pyqtSignal()

    def __init__(self, index, folder, app):
        super().__init__()
        self.setupUi(self)

        self.index = index
        self.folder = folder
        self.app = app
        self.title = 'Rule Edit'
        self.combo_box_item_other = 'Select other application'

        self.draw_ui()
        self.connect()

    def draw_ui(self):
        self.label_folder_value.setText(self.folder)
        self.label_folder_value.setToolTip(self.folder)
        self.label_folder_value.setStyleSheet('QLabel{color:blue;padding-left:5px;}')
        self.combo_box = QComboBox()
        self.combo_box.addItem(self.app)
        config = load_config()
        for k, v in config.aliases.items():
            if self.app != v:
                self.combo_box.addItem(k)
        self.combo_box.addItem(self.combo_box_item_other)
        self.gridLayout.addWidget(self.combo_box, 1, 1, 1, 1)

    def connect(self):
        self.label_folder_value.clicked.connect(self.slot_label_folder_clicked)
        self.combo_box.activated.connect(self.slot_combo_box_activated)
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
    def slot_combo_box_activated(self):
        if self.combo_box_item_other != self.combo_box.currentText():
            self.app = self.combo_box.currentText()
        else:
            app = QFileDialog.getOpenFileName()[0]
            if not app:
                return
            self.app = get_windows_path(app)
            self.draw_ui()

    @pyqtSlot()
    def slot_button_confirm_clicked(self):
        if not is_folder(self.folder):
            QMessageBox.critical(self, self.title, 'Please choose a folder!')
            return
        config = load_config()
        is_alias = False
        real_app = None
        if not is_application(self.app):
            for k, v in config.aliases.items():
                if self.app == k:
                    is_alias = True
                    real_app = v
                    break
            if not is_alias:
                QMessageBox.critical(self, self.title, 'Please choose a application!')
                return

        for rule_config in config.rules:
            if rule_config.index == self.index:
                rule_config.folder = self.folder
                if is_alias:
                    rule_config.app = real_app
                else:
                    rule_config.app = self.app
                break
        write_config(config)
        self.slot_button_close_clicked()

    @pyqtSlot()
    def slot_button_close_clicked(self):
        self.closed.emit()
        self.close()
