import json
import os
from typing import List, AnyStr

from PyQt5.QtWidgets import QMessageBox

DEFAULT_ENCODING = 'utf-8'
PROJECT_NAME = 'fae'
MB = 1024 * 1024
MINUTE = 60 * 1000
DATE_FORMAT = '%Y-%m-%d'
DATE_TIME_FORMAT = '%Y-%m-%d %H:%M:%S'


def get_project_path():
    os.chdir(os.path.join(os.path.dirname(__file__), '../'))
    return os.path.abspath(os.getcwd())


def get_config_file():
    return os.path.join(get_project_path(), f'{PROJECT_NAME}.json')


def get_log_file():
    return os.path.join(get_project_path(), f'{PROJECT_NAME}.log')


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

    def __repr__(self):
        return f'Rule[folder={self.folder}, app={self.app}]'

    @staticmethod
    def parse(d: dict):
        return Rule(d.get('index'), d.get('folder'), d.get('app'))


class Config:
    def __init__(self, rules: List[Rule], fallback: AnyStr, apps: List[AnyStr] = None):
        self.rules = rules  # type: List[Rule]
        if apps is None:
            self.apps = []  # type: List[AnyStr]
        else:
            self.apps = apps  # type: List[AnyStr]
        self.fallback = fallback  # type: AnyStr

    def to_dict(self):
        return {
            'rules': [rule.to_dict() for rule in self.rules],
            'apps': self.apps,
            'fallback': self.fallback,
        }

    def __repr__(self):
        return f'Config[rules={self.rules}, apps={self.apps}, fallback={self.fallback}]'

    @staticmethod
    def parse(d: dict):
        return Config([Rule.parse(rule) for rule in d.get('rules')],
                      d.get('fallback'),
                      d.get('apps'))


def load_config():
    if os.path.exists(get_config_file()):
        with open(get_config_file(), mode='r', encoding=DEFAULT_ENCODING) as f:
            try:
                config = Config.parse(json.load(f))
                config.rules.sort(key=lambda c: c.index, reverse=False)
                return config
            except Exception as e:
                QMessageBox.critical(None, 'System error', f'Parse config failed: {str(e)}')
    else:
        # generate default config
        config = Config([], '', [])
        write_config(config)
        return config


def write_config(config: Config):
    config.apps = list(set(config.apps))
    with open(get_config_file(), mode='w', encoding=DEFAULT_ENCODING) as f:
        f.write(json.dumps(config.to_dict(), default=lambda o: o.__dict__, indent=2))
