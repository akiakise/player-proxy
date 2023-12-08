"""
Build: pyinstaller.exe --onedir --noconsole --noconfirm --icon './resources/icon.ico' --add-data 'resources/icon.ico;resources/' player-proxy.py
"""
import os
import subprocess
import sys
import traceback
from logging import Formatter, StreamHandler, getLogger, DEBUG
from logging.handlers import RotatingFileHandler

import win32api
import win32con
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont, QIcon
from PyQt5.QtWidgets import QApplication, QMessageBox

from config import MB, PROJECT_NAME, DEFAULT_ENCODING, get_log_file
from config import load_config, get_config_file
from ui.wrapper.main_wrapper import MainWrapper
from util import get_extension


def get_logger():
    __file_handler = RotatingFileHandler(get_log_file(), maxBytes=10 * MB, backupCount=5, encoding=DEFAULT_ENCODING)
    __fmt = '%(asctime)s - %(threadName)s(%(thread)d) - %(filename)s:%(lineno)s - %(levelname)s - %(message)s'
    __formatter = Formatter(__fmt)
    __file_handler.setFormatter(__formatter)
    # Console logger
    __console_handler = StreamHandler(sys.stdout)

    # Final logger
    logger = getLogger(f'{PROJECT_NAME}Logger')
    logger.addHandler(__file_handler)
    logger.addHandler(__console_handler)
    logger.setLevel(DEBUG)
    return logger


if __name__ == '__main__':
    logger = get_logger()
    argv_length = len(sys.argv)
    if argv_length == 1:
        # Only one argument, configure proxy rule
        QApplication.setAttribute(Qt.AA_EnableHighDpiScaling)

        app = QApplication(sys.argv)
        font = QFont()
        font.setFamily("Microsoft YaHei UI")
        font.setHintingPreference(QFont.PreferNoHinting)
        app.setFont(font)
        app.setWindowIcon(QIcon('resources/icon.ico'))

        main_wrapper = MainWrapper()
        main_wrapper.show()


        def excepthook(_type, _value, _traceback):
            output = "".join(traceback.format_exception(_type, _value, _traceback))
            logger.error(f'Exception detected!\n{output}')
            QMessageBox.critical(None, 'System Exception', f'Exception detected!\n{output}')


        sys.excepthook = excepthook
        sys.exit(app.exec())
    elif argv_length == 2:
        # Two arguments, open video with rule
        logger.info(r'''
     ____.         .___                 _________ __                 __
    |    |__ __  __| _/ ____   ____    /   _____//  |______ ________/  |_
    |    |  |  \/ __ | / ___\_/ __ \   \_____  \\   __\__  \\_  __ \   __\
/\__|    |  |  / /_/ |/ /_/  >  ___/   /        \|  |  / __ \|  | \/|  |
\________|____/\____ |\___  / \___  > /_______  /|__| (____  /__|   |__|
                    \/_____/      \/          \/           \/
        ''')
        file_path = os.path.abspath(sys.argv[1])
        extension = get_extension(file_path)
        logger.info(f'config file: {get_config_file()}')
        logger.info(f'current file: {__file__}')
        logger.info(f'executable: {sys.executable}')
        config = load_config()
        # Run with rule
        for rule in config.rules:
            if rule.folder.upper() in file_path.upper():
                try:
                    logger.info(f'matched, rule: {rule}')
                    command = f'{rule.app} "{file_path}"'
                    logger.info(f'command: {command}')
                    subprocess.run(command)
                    sys.exit(0)
                except Exception as e:
                    win32api.MessageBoxEx(0, 'Failed to open file, navigate to logs for more details', 'Critical',
                                          win32con.MB_OK)
                    logger.error('Failed to open file', e)
                    sys.exit(1)
        # Run fallback
        logger.info(f'no rule matched, use fallback player: {config.fallback}')
        command = f'{config.fallback} "{file_path}"'
        logger.info(f'run command: {command}')
        subprocess.run(command)
        sys.exit(0)
    else:
        # If there is more than two arguments, warn and exit
        win32api.MessageBoxEx(0, f'Invalid argument count, only support zero or one argument, '
                                 f'current argument count: {argv_length}', 'Warning', win32con.MB_OK)
        sys.exit(2)
