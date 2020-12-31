# -*- coding: utf-8 -*-
import os
import json


def get_data_path():
    path = os.path.dirname(__file__)
    return path


def get_backup_path():
    path = os.path.join(os.path.dirname(__file__), 'backup')
    return path


def load_config(filename_config):
    path = os.path.join(os.path.dirname(__file__), 'config')
    filename_full = os.path.join(path, filename_config)
    with open(filename_full, 'r') as fp:
        config = json.load(fp)
        return config


if __name__ == '__main__':
    print(get_backup_path())
    print(load_config('dbconfig.json'))
