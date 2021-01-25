import os
from pathlib import PureWindowsPath


def get_extension(file):
    path = os.path.abspath(file)
    split = path.split('.')
    return split[-1] if split else ''


def get_windows_path(path):
    return str(PureWindowsPath(path))


def is_folder(path):
    return os.path.isdir(path)


def is_application(path: str):
    return os.path.isfile(path) and path.endswith('.exe') and os.access(path, os.X_OK)
