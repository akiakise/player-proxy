# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'dialog_default_player.ui'
#
# Created by: PyQt5 UI code generator 5.15.8
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(250, 80)
        self.layoutWidget = QtWidgets.QWidget(Dialog)
        self.layoutWidget.setGeometry(QtCore.QRect(10, 10, 231, 61))
        self.layoutWidget.setObjectName("layoutWidget")
        self.gridLayout = QtWidgets.QGridLayout(self.layoutWidget)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.gridLayout.setObjectName("gridLayout")
        self.label = QtWidgets.QLabel(self.layoutWidget)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)
        self.label_default_player = ClickableLabel(self.layoutWidget)
        self.label_default_player.setObjectName("label_default_player")
        self.gridLayout.addWidget(self.label_default_player, 0, 1, 1, 1)
        self.button_confirm = QtWidgets.QPushButton(self.layoutWidget)
        self.button_confirm.setObjectName("button_confirm")
        self.gridLayout.addWidget(self.button_confirm, 1, 0, 1, 1)
        self.button_cancel = QtWidgets.QPushButton(self.layoutWidget)
        self.button_cancel.setObjectName("button_cancel")
        self.gridLayout.addWidget(self.button_cancel, 1, 1, 1, 1)

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Update default player"))
        self.label.setText(_translate("Dialog", "Application:"))
        self.label_default_player.setText(_translate("Dialog", "TextLabel"))
        self.button_confirm.setText(_translate("Dialog", "Confirm"))
        self.button_cancel.setText(_translate("Dialog", "Cancel"))


from ui.util.ClickableLabel import ClickableLabel
