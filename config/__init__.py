import json
import os
from typing import List

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


class Rule:
    def __init__(self, index, folder, app):
        self.index = index
        self.folder = folder
        self.app = app

    def to_dict(self):
        return {
            'index': self.index,
            'folder': self.folder,
            'app': self.app
        }

    @staticmethod
    def parse(d: dict):
        return Rule(d.get('index'), d.get('folder'), d.get('app'))


class Config:
    def __init__(self, rules: List[Rule], fallback: str, aliases: dict):
        self.rules = rules  # type: List[Rule]
        self.fallback = fallback  # type: str
        self.aliases = aliases  # type: dict

    def to_dict(self):
        return {
            'rules': [rule.to_dict() for rule in self.rules],
            'fallback': self.fallback,
            'aliases': self.aliases
        }

    @staticmethod
    def parse(d: dict):
        return Config(
            [Rule.parse(rule) for rule in d.get('rules')], d.get('fallback'), d.get('aliases'))


def load_config():
    if os.path.exists(FILENAME_CONFIG):
        with open(FILENAME_CONFIG, mode='r', encoding=DEFAULT_ENCODING) as f:
            config = Config.parse(json.load(f))
            config.rules.sort(key=lambda c: c.index, reverse=False)
            return config


def write_config(config: Config):
    with open(FILENAME_CONFIG, mode='w', encoding=DEFAULT_ENCODING) as f:
        f.write(json.dumps(config.to_dict(), default=lambda o: o.__dict__, indent=2))
