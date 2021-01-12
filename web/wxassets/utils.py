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
    tye_amount = wx_data['tye_asset']
    if tye_amount == 'debt':
        wx_data['amt_asset'] = -1 * float(wx_data['amt_asset'])
    amount = wx_data['amt_asset']

    df_asset, table_asset, index_asset, if_exists_asset = Asset(acc_user).add_assets(wx_data, is_transaction=True)
    sql_update_statistics = Statistic(acc_user).update_statistics(tye_amount, amount, is_transaction=True)

    dfinfo_list = [[df_asset, table_asset, index_asset, if_exists_asset]]
    sql_list = [sql_update_statistics]
    return {'result': DataBase().transaction(dfinfo_list, sql_list)}


def utils_update_assets(wx_data):
    acc_user = wx_data['token']
    result = Asset(acc_user).update_assets(wx_data)
    return {'result': result}


def utils_delete_assets(wx_data):
    acc_user = wx_data['token']
    result = Asset(acc_user).delete_assets(wx_data)
    return {'result': result}

