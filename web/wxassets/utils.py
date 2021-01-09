#!/usr/bin/env python
# -*- coding: utf-8 -*-
from database.models.assets.asset import Asset
from database.models.statistics.statistic import Statistic
from database.base.database_helper import DataBase


def utils_show_assets(wx_data, flag_default=False):
    if flag_default:
        acc_user = 'dbuser'
    else:
        acc_user = wx_data['token']
    df_assets = Asset(acc_user).show_assets()
    
    data = []
    for index in range(len(df_assets)):
        data.append(df_assets.iloc[index].to_dict())
    return {'assets': data}


def utils_add_assets(wx_data):
    acc_user = wx_data['token']
    del wx_data['token']
    wx_data['acc_user'] = acc_user
    type_amount = {'资产': 'asset', '负债': 'debt'}[wx_data['tye_asset']]
    amount = wx_data['amt_asset']

    sql_add_assets = Asset(acc_user).add_assets_transaction(wx_data)
    sql_update_statistics = Statistic(acc_user).update_statistics_transaction(type_amount, amount)

    conn = DataBase().connection()
    tran = conn.begin()
    try:
        conn.execute(sql_add_assets)
        conn.execute(sql_update_statistics)
        tran.commit()
        return {'result': True}
    except Exception as e:
        print(str(e))
        tran.rollback()
        return {'result': False}


def utils_update_assets(wx_data):
    acc_user = wx_data['token']
    result = Asset(acc_user).update_assets(wx_data)
    return {'result': result}


def utils_delete_assets(wx_data):
    acc_user = wx_data['token']
    result = Asset(acc_user).delete_assets(wx_data)
    return {'result': result}

