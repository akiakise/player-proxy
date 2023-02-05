from PyQt5.QtCore import pyqtSlot, pyqtSignal
from PyQt5.QtWidgets import QDialog, QFileDialog, QMessageBox, QComboBox

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
        self.app = None
        self.combo_box_item_other = 'Select other application'

        self.draw_ui()
        self.connect()

    def draw_ui(self):
        self.label_folder_value.setText(self.folder)
        self.label_folder_value.setToolTip(self.folder)
        self.label_folder_value.setStyleSheet('QLabel{color:blue;padding-left:5px;}')
        self.combo_box = QComboBox()
        config = load_config()
        for app in config.apps:
            if app != self.app:
                self.combo_box.addItem(app)
        if self.app and self.app != self.combo_box_item_other:
            self.combo_box.addItem(self.app)
            self.combo_box.setCurrentText(self.app)
        self.combo_box.addItem(self.combo_box_item_other)
        self.app = self.combo_box.currentText()
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
            QMessageBox.critical(self, self.title, 'Please choose a folder!')
            self.draw_ui()
            return
        folder_path = get_windows_path(folder)
        if not is_folder(folder_path):
            QMessageBox.critical(self, self.title, f'Not a folder: {folder_path}!')
            self.draw_ui()
            return
        self.folder = folder_path
        self.draw_ui()

    @pyqtSlot()
    def slot_label_app_clicked(self):
        app = QFileDialog.getOpenFileName(filter='exe(*.exe)')[0]
        if not app:
            QMessageBox.critical(self, self.title, 'Please choose a player!')
            self.draw_ui()
            return
        app_path = get_windows_path(app)
        if not is_application(app_path):
            QMessageBox.critical(self, self.title, f'Not a valid player: {app_path}')
            self.draw_ui()
            return
        self.app = app_path
        self.draw_ui()

    @pyqtSlot()
    def slot_combo_box_activated(self):
        if self.combo_box_item_other != self.combo_box.currentText():
            self.chose_app = self.combo_box.currentText()
        else:
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
            self.app = app_path
            self.draw_ui()

    @pyqtSlot()
    def slot_button_confirm_clicked(self):
        if not is_folder(self.folder):
            QMessageBox.critical(self, self.title, 'Please choose a folder!')
            self.draw_ui()
            return
        if not is_application(self.app):
            QMessageBox.critical(self, self.title, f'Not a valid player: {self.app}')
            self.draw_ui()
            return

        config = load_config()
        # 1. handle rule add
        max_index = max([rule.index for rule in config.rules] + [-1])
        config.rules.append(Rule(max_index + 1, self.folder, self.app))
        # 2. update apps
        config.apps.append(self.app)
        # 3. update config
        write_config(config)
        self.slot_button_close_clicked()

    @pyqtSlot()
    def slot_button_close_clicked(self):
        self.closed.emit()
        self.close()
