#!/usr/bin/env python
# -*- coding: utf-8 -*-
from database.models.transactions.transaction import Transaction
from database.models.statistics.statistic import Statistic
from database.models.assets.asset import Asset
from database.base.database_helper import DataBase


def utils_show_trans(wx_data):
    acc_user = wx_data['token']
    acc_asset = wx_data.get('acc_asset', None)
    df_trans = Transaction(acc_user).show_trans(acc_asset)
    df_trans['amt_trans'] = df_trans['amt_trans'].apply(abs)    # 为方便前台显示，统一为正值
    data = []
    for index in range(len(df_trans)):
        data.append(df_trans.iloc[index].to_dict())
    return {'trans': data}


def utils_add_trans(wx_data):
    acc_user = wx_data['token']
    del wx_data['token']
    wx_data['acc_user'] = acc_user

    tye_flow = wx_data['tye_flow']
    acc_asset = wx_data['acc_asset']
    tye_asset = wx_data['tye_asset']
    acc_asset_related = wx_data.get('acc_asset_related', '')
    tye_asset_related = wx_data.get('tye_asset_related', '')
    cod_trans_type = wx_data.get('cod_trans_type', '')
    if tye_flow == 'expend':
        wx_data['amt_trans'] = -1 * float(wx_data['amt_trans'])
    amount = wx_data['amt_trans']

    df_trans, table_trans, index_trans, if_exists_trans = Transaction(acc_user).add_trans(wx_data, is_transaction=True)
    sql_update_statistics = Statistic(acc_user).update_statistics(tye_flow, amount, cod_trans_type=cod_trans_type, tye_asset=tye_asset, tye_asset_related=tye_asset_related, is_transaction=True)
    sql_update_assets, sql_update_assets_related = Asset(acc_user).update_assets(tye_flow, amount, acc_asset, tye_asset, acc_asset_related, tye_asset_related, is_transaction=True)
    
    dfinfo_list = [[df_trans, table_trans, index_trans, if_exists_trans]]
    sql_list = [sql_update_statistics, sql_update_assets]
    if sql_update_assets_related:
        sql_list.append(sql_update_assets_related)
    return {'result': DataBase().transaction(dfinfo_list, sql_list)}


def utils_show_report(wx_data):
    acc_user = wx_data['token']
    df_report = Transaction(acc_user).show_report()
    data = []
    for index in range(len(df_report)):
        data.append(df_report.iloc[index].to_dict())
    return {'report': data}

def utils_update_trans():
    pass


def utils_delete_trans():
    pass



