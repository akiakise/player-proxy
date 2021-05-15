import os
from logging import Formatter, StreamHandler, getLogger, DEBUG
from logging.handlers import RotatingFileHandler
from sys import stdout

from config import MB, PROJECT_NAME, PATH_LOG_DIR, DEFAULT_ENCODING

__log_file = os.path.join(PATH_LOG_DIR, f'{PROJECT_NAME.lower()}.log')
if not os.path.exists(PATH_LOG_DIR):
    os.makedirs(PATH_LOG_DIR)

# File logger
__file_handler = RotatingFileHandler(__log_file, maxBytes=10 * MB, backupCount=5, encoding=DEFAULT_ENCODING)
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
