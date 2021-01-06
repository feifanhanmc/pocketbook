#!/usr/bin/env python
# -*- coding: utf-8 -*-
from database.models.transactions.transaction import Transaction


def utils_show_trans(wx_data):
    acc_user = wx_data['token']
    acc_asset = wx_data.get('acc_asset', None)
    df_trans = Transaction(acc_user).show_trans(acc_asset)
    print('AAAAaaaa', wx_data, df_trans)
    data = []
    for index in range(len(df_trans)):
        data.append(df_trans.iloc[index].to_dict())
    return {'trans': data}


def utils_add_trans(wx_data):
    acc_user = wx_data['token']
    del wx_data['token']
    wx_data['acc_user'] = acc_user
    result = Transaction(acc_user).add_trans(wx_data)
    return {'result': result}


def utils_update_trans():
    pass


def utils_delete_trans():
    pass



