"""
Build: pyinstaller.exe --onedir --noconsole --noconfirm --add-data "fae.json;." configure.py
"""
import sys
import traceback

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QMessageBox

from log import logger
from ui.wrapper.main_wrapper import MainWrapper


def excepthook(_type, _value, _traceback):
    output = "".join(traceback.format_exception(_type, _value, _traceback))
    logger.error(f'Exception detected!\n{output}')
    QMessageBox.critical(None, 'System Exception', f'Exception detected!\n{output}')


if __name__ == '__main__':
    QApplication.setAttribute(Qt.AA_EnableHighDpiScaling)

    app = QApplication(sys.argv)

    main_wrapper = MainWrapper()
    main_wrapper.show()

    sys.excepthook = excepthook
    sys.exit(app.exec())
