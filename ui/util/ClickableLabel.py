from PyQt5 import QtCore
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtGui import QMouseEvent, QFont
from PyQt5.QtWidgets import QLabel


class ClickableLabel(QLabel):
    clicked = pyqtSignal()

    def __init__(self, dialog) -> None:
        super().__init__()

    def mousePressEvent(self, ev: QMouseEvent) -> None:
        self.clicked.emit()

    def enterEvent(self, a0: QtCore.QEvent) -> None:
        font = QFont()
        font.setUnderline(True)
        font.setBold(True)
        self.setFont(font)
        super().enterEvent(a0)

    def leaveEvent(self, a0: QtCore.QEvent) -> None:
        font = QFont()
        font.setUnderline(False)
        self.setFont(font)
        super().leaveEvent(a0)
