from logging import Formatter, StreamHandler, getLogger, DEBUG
from logging.handlers import RotatingFileHandler
from sys import stdout

from config import MB, PROJECT_NAME, DEFAULT_ENCODING, get_log_file


# File logger
def get_logger():
    __file_handler = RotatingFileHandler(get_log_file(), maxBytes=10 * MB, backupCount=5, encoding=DEFAULT_ENCODING)
    __fmt = '%(asctime)s - %(threadName)s(%(thread)d) - %(filename)s:%(lineno)s - %(levelname)s - %(message)s'
    __formatter = Formatter(__fmt)
    __file_handler.setFormatter(__formatter)
    # Console logger
    __console_handler = StreamHandler(stdout)

    # Final logger
    logger = getLogger(f'{PROJECT_NAME}Logger')
    logger.addHandler(__file_handler)
    logger.addHandler(__console_handler)
    logger.setLevel(DEBUG)
    return logger
