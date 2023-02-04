import os
from pathlib import PureWindowsPath


def get_extension(file):
    path = os.path.abspath(file)
    split = path.split('.')
    return split[-1] if split else ''


def get_windows_path(path):
    return str(PureWindowsPath(path))


def get_short_name(path):
    return path.split('\\')[-1].split('.')[0]


def is_folder(path):
    return path and os.path.isdir(path)


def is_application(path: str):
    return path and os.path.isfile(path) and path.endswith('.exe') and os.access(path, os.X_OK)
