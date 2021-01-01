#!/usr/bin/env python
# -*- coding: utf-8 -*-
import json
import requests
from web.wxuser.WXBizDataCrypt import WXBizDataCrypt
from data.data_helper import load_config
from database.models.users.user import User
from database.models.transactions.transaction import Transaction


def utils_tran_add(wx_data):
    acc_user = wx_data['acc_user']
    data_tran = wx_data['data_tran']
    tran = Transaction(acc_user)
    tran.insert(data_tran)
    return {"A": 111}


def utils_tran_delete():
    pass


def utils_tran_show():
    pass


def utils_tran_update():
    pass

