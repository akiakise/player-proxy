import json
import os
from types import SimpleNamespace

DEFAULT_ENCODING = 'utf-8'
PROJECT_NAME = 'fae'
DIR_PROJECT = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
DIR_LOG = os.path.join(DIR_PROJECT, 'log')
FILENAME_CONFIG = os.path.join(DIR_PROJECT, f'{PROJECT_NAME}.json')
FILENAME_SAMPLE_CONFIG = os.path.join(DIR_PROJECT, f'{PROJECT_NAME}.sample.json')
KEY_CONFIG = 'config'

MB = 1024 * 1024
MINUTE = 60 * 1000
LOGFILE_COUNT = 5

DATE_FORMAT = '%Y-%m-%d'
DATE_TIME_FORMAT = '%Y-%m-%d %H:%M:%S'


def load_config():
    if os.path.exists(FILENAME_CONFIG):
        with open(FILENAME_CONFIG, mode='r', encoding=DEFAULT_ENCODING) as f:
            return json.loads(f.read(), object_hook=lambda data: SimpleNamespace(**data))