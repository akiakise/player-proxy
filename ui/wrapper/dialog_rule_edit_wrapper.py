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
        self.folder, self.app = folder, app
        self.chose_folder, self.chose_app = self.folder, self.app
        self.title = 'Rule Edit'
        self.combo_box_item_other = 'Select other application'

        self.draw_ui()
        self.connect()

    def draw_ui(self):
        if self.chose_folder:
            self.label_folder_value.setText(self.chose_folder)
            self.label_folder_value.setToolTip(self.chose_folder)
        else:
            self.label_folder_value.setText(self.folder)
            self.label_folder_value.setToolTip(self.folder)
        self.label_folder_value.setStyleSheet('QLabel{color:blue;padding-left:5px;}')
        self.combo_box = QComboBox()
        self.combo_box.addItem(self.app)
        self.combo_box.setCurrentText(self.app)
        config = load_config()
        for app in config.apps:
            if self.app != app:
                self.combo_box.addItem(app)
        if self.chose_app and self.chose_app != self.app:
            self.combo_box.addItem(self.chose_app)
            self.combo_box.setCurrentText(self.chose_app)
        self.combo_box.addItem(self.combo_box_item_other)
        self.combo_box.activated.connect(self.slot_combo_box_activated)
        self.gridLayout.addWidget(self.combo_box, 1, 1, 1, 1)

    def connect(self):
        self.label_folder_value.clicked.connect(self.slot_label_folder_clicked)
        self.pushButton_confirm.clicked.connect(self.slot_button_confirm_clicked)
        self.pushButton_cancel.clicked.connect(self.slot_button_close_clicked)

    @pyqtSlot()
    def slot_label_folder_clicked(self):
        folder = QFileDialog.getExistingDirectory()
        if not folder:
            return
        self.chose_folder = get_windows_path(folder)
        self.draw_ui()

    @pyqtSlot()
    def slot_combo_box_activated(self):
        if self.combo_box_item_other != self.combo_box.currentText():
            self.chose_app = self.combo_box.currentText()
        else:
            app = QFileDialog.getOpenFileName()[0]
            if not app:
                return
            self.chose_app = get_windows_path(app)
            self.draw_ui()

    @pyqtSlot()
    def slot_button_confirm_clicked(self):
        if not is_folder(self.chose_folder):
            QMessageBox.critical(self, self.title, 'Please choose a folder!')
            self.chose_folder = self.folder
            self.draw_ui()
            return
        if not is_application(self.chose_app):
            QMessageBox.critical(self, self.title, 'Please choose a valid player!')
            self.chose_app = self.app
            self.draw_ui()
            return

        config = load_config()
        # 1. handle rule change
        for rule_config in config.rules:
            if rule_config.index != self.index:
                continue
            rule_config.folder, rule_config.app = self.chose_folder, self.chose_app
            break
        # 2. check if apps updated
        if self.chose_app not in config.apps:
            config.apps.append(self.chose_app)
        # 3. update config
        write_config(config)
        self.slot_button_close_clicked()

    @pyqtSlot()
    def slot_button_close_clicked(self):
        self.closed.emit()
        self.close()
