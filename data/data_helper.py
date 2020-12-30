# -*- coding: utf-8 -*-
import os


def get_data_path():
    path = os.path.dirname(__file__)
    return path


if __name__ == '__main__':
    print(get_data_path())
