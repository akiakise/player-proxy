import os
from logging import Formatter, StreamHandler, getLogger, DEBUG
from logging.handlers import RotatingFileHandler
from sys import stdout

from config import MB, LOGFILE_COUNT, PROJECT_NAME, DIR_LOG, DEFAULT_ENCODING

log_file = os.path.join(DIR_LOG, f'{PROJECT_NAME.lower()}.log')
if not os.path.exists(DIR_LOG):
    os.makedirs(DIR_LOG)

file_handler = RotatingFileHandler(log_file, maxBytes=10 * MB, backupCount=LOGFILE_COUNT, encoding=DEFAULT_ENCODING)
fmt = '%(asctime)s - %(threadName)s(%(thread)d) - %(filename)s:%(lineno)s - %(levelname)s - %(message)s'
formatter = Formatter(fmt)
file_handler.setFormatter(formatter)
console_handler = StreamHandler(stdout)

logger = getLogger(f'{PROJECT_NAME}Logger')
logger.addHandler(file_handler)
logger.addHandler(console_handler)
logger.setLevel(DEBUG)
