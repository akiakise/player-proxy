from PyQt5 import QtGui
from PyQt5.QtCore import Qt, pyqtSlot
from PyQt5.QtGui import QStandardItemModel, QStandardItem
from PyQt5.QtWidgets import QDialog, QHeaderView, QAbstractItemView, QMenu, QMessageBox

from config import load_config, write_config
from ui.source.dialog_known_player import Ui_Dialog
from util.file_util import get_short_name


class DialogKnownPlayerWrapper(QDialog, Ui_Dialog):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.title = 'Manage known players'
        self.config_map = {}

        self.draw_ui()
        self.connect()

    def draw_ui(self):
        self.config = load_config()
        model = QStandardItemModel(len(self.config.rules), 1)
        model.setHorizontalHeaderLabels(['Application'])
        for row, app in enumerate(self.config.apps):
            app_item = QStandardItem(app)
            app_item.setEditable(False)
            app_item.setToolTip(app)

            model.setItem(row, 0, app_item)
            self.config_map[row] = app
        self.tableView.setModel(model)
        self.tableView.verticalHeader().hide()
        self.tableView.horizontalHeader().setDefaultAlignment(Qt.AlignCenter)
        self.tableView.horizontalHeader().setSectionResizeMode(0, QHeaderView.Stretch)
        self.tableView.horizontalHeader().setHighlightSections(False)
        self.tableView.horizontalHeader().setSectionsClickable(False)
        self.tableView.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.tableView.setFocusPolicy(Qt.NoFocus)
        self.tableView.setSelectionMode(QAbstractItemView.NoSelection)

    def connect(self):
        self.tableView.setContextMenuPolicy(Qt.CustomContextMenu)
        self.tableView.customContextMenuRequested.connect(self.slot_tableView_customContextMenuRequested)

    def slot_tableView_customContextMenuRequested(self):
        menu_top = QMenu(self)
        menu_main = menu_top.addMenu('Menu')

        menu_del_action = menu_main.addAction('Del')
        menu_del_action.triggered.connect(self.slot_table_menu_del_action_triggered)
        menu_main.exec_(QtGui.QCursor.pos())

    @pyqtSlot()
    def slot_table_menu_del_action_triggered(self):
        if not self.config_map:
            QMessageBox.critical(self, self.title, 'No known players!')
            return
        app = self.config_map[self.tableView.currentIndex().row()]
        if not app:
            QMessageBox.critical(self, self.title, f'Unknown app: {app}')
            return
        config = load_config()
        config.apps.remove(app)
        write_config(config)
        QMessageBox.information(self, self.title, 'Successfully deleted!')
        self.close()
