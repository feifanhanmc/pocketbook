#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os


def get_export_path():
    """
    :return: 返回导出路径
    """
    path_base = os.path.dirname(__file__)
    path_export = os.path.abspath(os.path.join(path_base, "../../data/export"))
    if not os.path.exists(path_export):
        os.makedirs(path_export)
    return path_export


def utils_export():
    return get_export_path()


if __name__ == '__main__':
    print(utils_export())
