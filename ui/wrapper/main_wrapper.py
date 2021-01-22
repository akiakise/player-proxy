from pathlib import PureWindowsPath

from PyQt5.QtCore import pyqtSlot
from PyQt5.QtGui import QStandardItemModel, QStandardItem
from PyQt5.QtWidgets import QDialog, QHeaderView, QMessageBox, QFileDialog

from config import load_config, write_config
from ui.source.main import Ui_Dialog


class MainWrapper(QDialog, Ui_Dialog):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.config = None
        self.config_map = {}
        self.column_folder = 0
        self.column_app = 1

        self.draw_ui()
        self.connect()

    def draw_ui(self):
        self.config = load_config()
        model = QStandardItemModel(len(self.config['rules']), 2)
        model.setHorizontalHeaderLabels(['Folder', 'Application'])
        for row, rule in enumerate(self.config['rules']):
            folder_item = QStandardItem(rule['folder'])
            folder_item.setEditable(False)
            folder_item.setToolTip(rule['folder'])

            app_item = QStandardItem(rule['app'])
            app_item.setEditable(False)
            app_item.setToolTip(rule['app'])

            model.setItem(row, self.column_folder, folder_item)
            model.setItem(row, self.column_app, app_item)
            self.config_map[row] = rule
        self.tableView.setModel(model)
        self.tableView.verticalHeader().hide()
        self.tableView.horizontalHeader().setSectionResizeMode(self.column_folder, QHeaderView.ResizeToContents)
        self.tableView.horizontalHeader().setSectionResizeMode(self.column_app, QHeaderView.Stretch)

    def connect(self):
        self.tableView.doubleClicked.connect(self.slot_tableView_doubleClicked)

    @pyqtSlot()
    def slot_tableView_doubleClicked(self):
        if self.tableView.currentIndex().column() == self.column_app:
            rule_tmp = self.config_map[self.tableView.currentIndex().row()]
            app = QFileDialog.getOpenFileName(self, f'Choose an app to open the videos under {rule_tmp["folder"]}')[0]
            res = QMessageBox.question(self, 'Confirm',
                                       f'Are you sure for using \n'
                                       f'[{app}]\n'
                                       f'to open videos under\n'
                                       f'[{rule_tmp["folder"]}]?')
            if res == QMessageBox.Yes:
                for rule_config in self.config['rules']:
                    if rule_config['folder'] == rule_tmp['folder']:
                        rule_config['app'] = str(PureWindowsPath(app))
                write_config(self.config)
                QMessageBox.information(self, 'Notify', f'Successfully update the app connect to {rule_tmp["folder"]}')
