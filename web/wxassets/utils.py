#!/usr/bin/env python
# -*- coding: utf-8 -*-
from database.models.assets.asset import Asset
from database.models.statistics.statistic import Statistic
from database.models.transactions.transaction import Transaction, dic_trans4assets_adjust
from database.base.database_helper import DataBase
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


def utils_modify_assets(wx_data):
    acc_user = wx_data['token']
    acc_asset = wx_data['acc_asset']
    amt_asset = wx_data['amt_asset']
    rmk_asset = wx_data['rmk_asset']

    df_asset = Asset(acc_user).show_assets(acc_asset=acc_asset, need_index=False)
    if not df_asset.empty:
        df_asset = df_asset.iloc[:1]

        amount = float(wx_data['amt_asset']) - float(df_asset['amt_asset'][0])
        tye_amount = df_asset['tye_asset'][0]
        df_asset['amt_asset'] = amt_asset
        df_asset['rmk_asset'] = rmk_asset

        dict_trans = copy.deepcopy(dic_trans4assets_adjust)
        for key in list(set(df_asset.keys()) & set(dict_trans.keys())):
            dict_trans[key] = df_asset[key][0]
        dict_trans['dte_trans'] = time.strftime("%Y%m%d", time.localtime())
        dict_trans['amt_trans'] = -1*amount

        sql_delete_asset, table_asset, index_asset, if_exists_asset = Asset(acc_user).modify_assets(acc_asset, df_asset, is_transaction=True)
        sql_update_statistics = Statistic(acc_user).update_statistics(tye_amount=tye_amount, amount=amount, is_transaction=True)
        df_trans, table_trans, index_trans, if_exists_trans = Transaction(acc_user).add_trans(dict_trans, is_transaction=True)

        sql_list = [sql_delete_asset, sql_update_statistics]
        dfinfo_list = [
            [df_asset, table_asset, index_asset, if_exists_asset],
            [df_trans, table_trans, index_trans, if_exists_trans]]
        
        print(sql_list, dfinfo_list)
        return {'result': DataBase().transaction(dfinfo_list, sql_list)}
    return {'result': False}


def utils_delete_assets(wx_data):
    acc_user = wx_data['token']
    result = Asset(acc_user).delete_assets(wx_data)
    return {'result': result}

