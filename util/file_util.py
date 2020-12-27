import os


def get_extension(file):
    path = os.path.abspath(file)
    split = path.split('.')
    return split[-1] if split else ''
