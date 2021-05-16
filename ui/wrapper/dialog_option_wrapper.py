from PyQt5.QtCore import pyqtSignal, pyqtSlot, Qt
from PyQt5.QtWidgets import QDialog, QAbstractItemView, QHeaderView, QPushButton

from config import load_config
from ui.source.dialog_option import Ui_Dialog


class DialogOptionWrapper(QDialog, Ui_Dialog):
    closed = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.config = None
        self.column_count = 3
        self.column_key = 0
        self.column_value = 1
        self.column_operation = 2
        self.fallback = 'Please choose a application!'

        self.alias_add_button = QPushButton('+', self)
        self.alias_add_button_used = False
        self.alias_del_button = QPushButton('-', self)
        self.alias_del_button_used = False

        self.pre_draw_ui()
        self.draw_ui()
        self.post_draw_ui()
        self.connect()

    def pre_draw_ui(self):
        self.config = load_config()
        self.alias_add_button.setMinimumWidth(40)
        self.alias_add_button.setMaximumWidth(40)
        self.alias_add_button.setStyleSheet('QPushButton{margin:5px;}')

    def draw_ui(self):
        self.label_fallback_value.setText(self.fallback)
        self.label_fallback_value.setToolTip(self.fallback)
        self.label_fallback_value.setStyleSheet('QLabel{color:blue;padding-left:5px;}')
        # Alias table
        if not self.config.aliases:
            # Alias map is empty
            self.tableWidget.setRowCount(1)
            self.tableWidget.setColumnCount(self.column_count)
            self.tableWidget.setCellWidget(0, self.column_operation, self.alias_add_button)
            self.alias_add_button_used = True
            pass
        else:
            # Alias map is not empty
            self.tableWidget.setRowCount(len(self.config.aliases))
            self.tableWidget.setColumnCount(self.column_count)
            for k, v in self.config.aliases:
                pass
        self.tableWidget.verticalHeader().hide()
        self.tableWidget.horizontalHeader().setDefaultAlignment(Qt.AlignLeft)
        self.tableWidget.horizontalHeader().setSectionResizeMode(self.column_key, QHeaderView.ResizeToContents)
        self.tableWidget.horizontalHeader().setSectionResizeMode(self.column_value, QHeaderView.Stretch)
        self.tableWidget.horizontalHeader().setSectionResizeMode(self.column_operation, QHeaderView.ResizeToContents)
        self.tableWidget.horizontalHeader().setHighlightSections(False)
        self.tableWidget.setSelectionMode(QAbstractItemView.NoSelection)

    def post_draw_ui(self):
        if not self.alias_add_button_used:
            self.alias_add_button.hide()
        if not self.alias_del_button_used:
            self.alias_del_button.hide()

    def connect(self):
        self.label_fallback_value.clicked.connect(self.slot_fallback_clicked)
        if self.alias_add_button_used:
            self.alias_add_button.clicked.connect(self.slot_button_alias_add_clicked)
        if self.alias_del_button_used:
            self.alias_del_button.clicked.connect(self.slot_button_alias_del_clicked)
        self.button_confirm.clicked.connect(self.slot_button_confirm_clicked)
        self.button_cancel.clicked.connect(self.slot_button_cancel_clicked)

    @pyqtSlot()
    def slot_fallback_clicked(self):
        pass

    @pyqtSlot()
    def slot_button_alias_add_clicked(self):
        pass

    @pyqtSlot()
    def slot_button_alias_del_clicked(self):
        pass

    @pyqtSlot()
    def slot_button_confirm_clicked(self):
        pass

    @pyqtSlot()
    def slot_button_cancel_clicked(self):
        self.slot_button_close_clicked()

    @pyqtSlot()
    def slot_button_close_clicked(self):
        self.closed.emit()
        self.close()
