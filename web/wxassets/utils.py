#!/usr/bin/env python
# -*- coding: utf-8 -*-
from database.models.assets.asset import Asset
from database.models.statistics.statistic import Statistic
from database.models.transactions.transaction import Transaction, dic_trans4assets_adjust
from database.base.database_helper import DataBase
import pandas as pd
import time
import copy


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


def utils_add_assets(wx_data, is_transaction=False):
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

    if not is_transaction:
        return {'result': DataBase().transaction(dfinfo_list, sql_list)}
    else:
        return sql_list, dfinfo_list


# modify asset拆解为delete asset + add asset + add trans
def utils_modify_assets(wx_data):
    acc_user = wx_data['token']
    acc_asset = wx_data['acc_asset']
    
    sql_list, dfinfo_list =[], []
    df_asset = Asset(acc_user).show_assets(acc_asset=acc_asset, need_index=False)
    if not df_asset.empty:
        dict_asset = df_asset.iloc[0].to_dict()

        # delete asset
        wx_data_delete = {'token': wx_data['token'], 'acc_asset': acc_asset}
        sql_delete_list, dfinfo_delete_list = utils_delete_assets(wx_data_delete, df_asset=df_asset, is_transaction=True)
        sql_list.extend(sql_delete_list)
        dfinfo_list.extend(dfinfo_delete_list)

        # add asset
        wx_data_add = copy.deepcopy(dict_asset)
        for key in wx_data.keys():
            wx_data_add[key] = wx_data[key]
        sql_add_list, dfinfo_add_list = utils_add_assets(wx_data_add, is_transaction=True)
        sql_list.extend(sql_add_list)
        dfinfo_list.extend(dfinfo_add_list)

        # add trans
        if dict_asset['tye_asset'] == 'debt':
            amount = -1 * float(wx_data['amt_asset'])
        else:
            amount = float(wx_data['amt_asset'])
        amt_trans = amount - float(dict_asset['amt_asset']) 
        if amt_trans != 0:  # 资产金额有变动时，新增一笔资金调整的交易记录
            dict_trans = copy.deepcopy(dic_trans4assets_adjust)
            for key in list(set(dict_asset.keys()) & set(dict_trans.keys())):
                dict_trans[key] = dict_asset[key]
            dict_trans['dte_trans'] = time.strftime("%Y%m%d", time.localtime())
            dict_trans['amt_trans'] = amt_trans
            df_trans, table_trans, index_trans, if_exists_trans = Transaction(acc_user).add_trans(dict_trans, is_transaction=True)
            dfinfo_list.append([df_trans, table_trans, index_trans, if_exists_trans])

        return {'result': DataBase().transaction(dfinfo_list, sql_list)}
    return {'result': False}


# 删除账户后，对应的资产负债要变化
def utils_delete_assets(wx_data, df_asset=pd.DataFrame(), is_transaction=False):
    acc_user = wx_data['token']
    acc_asset = wx_data['acc_asset']

    a = Asset(acc_user)
    sql_delete_asset = a.delete_assets(acc_asset, is_transaction=True)
    if df_asset.empty:
        df_asset = a.show_assets(acc_asset=acc_asset, need_index=False)

    if not df_asset.empty:
        df_asset = df_asset.iloc[:1]
        tye_asset = df_asset['tye_asset'][0]
        tye_amount = 'asset'
        amount = df_asset['amt_asset'][0]
        sql_update_statistics = Statistic(acc_user).update_statistics(tye_amount, amount, tye_asset=tye_asset, tye_update='delete_asset', is_transaction=True)

    dfinfo_list = []
    sql_list = [sql_delete_asset, sql_update_statistics]
    if not is_transaction:
        return {'result': DataBase().transaction(dfinfo_list, sql_list)}
    else:
        return sql_list, dfinfo_list

