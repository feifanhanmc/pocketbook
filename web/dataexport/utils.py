#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os


def utils_export():
    path_base = os.path.dirname(__file__)
    path_userdata = 'userdata'
    return os.path.join(path_base, path_userdata)
