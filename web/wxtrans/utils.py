#!/usr/bin/env python
# -*- coding: utf-8 -*-
from database.models.transactions.transaction import Transaction
from database.models.statistics.statistic import Statistic
from database.models.assets.asset import Asset
from database.base.database_helper import DataBase
from tools.toolkit import gen_short_uuid
from web.dexport.utils import get_export_path
import time
import calendar
import pandas as pd
import numpy as np
import os
import copy


url_base = 'https://sun.liuyihua.com'


def utils_show_trans(wx_data):
    acc_user = wx_data['token']
    acc_asset = wx_data.get('acc_asset', None)
    df_trans = Transaction(acc_user).show_trans(acc_asset)
    # 为方便前台显示，除资金调整外，统一为正值，用颜色予以区分
    df_trans.loc[(df_trans['tye_flow']!='adjust'), 'amt_trans'] = df_trans['amt_trans'].apply(abs)

    data = []
    for index in range(len(df_trans)):
        data.append(df_trans.iloc[index].to_dict())
    return {'trans': data}


def utils_add_trans(wx_data, is_transaction=False):
    acc_user = wx_data['token']
    del wx_data['token']
    wx_data['acc_user'] = acc_user

    tye_flow = wx_data['tye_flow']
    acc_asset = wx_data['acc_asset']
    tye_asset = wx_data['tye_asset']
    acc_asset_related = wx_data.get('acc_asset_related', '')
    tye_asset_related = wx_data.get('tye_asset_related', '')
    cod_trans_type = wx_data.get('cod_trans_type', '')
    # 从前台返回的数据是经过调整后的绝对值等，需要处理后才能存入数据库
    if tye_flow == 'expend':
        wx_data['amt_trans'] = -1 * float(wx_data['amt_trans'])
    amount = wx_data['amt_trans']

    df_trans, table_trans, index_trans, if_exists_trans = Transaction(acc_user).add_trans(wx_data, is_transaction=True)
    sql_update_statistics = Statistic(acc_user).update_statistics(tye_flow, amount, cod_trans_type=cod_trans_type, tye_asset=tye_asset, tye_asset_related=tye_asset_related, is_transaction=True)
    sql_update_assets, sql_update_assets_related = Asset(acc_user).update_assets(tye_flow, amount, acc_asset, tye_asset, acc_asset_related, tye_asset_related, is_transaction=True)
    
    dfinfo_list = [[df_trans, table_trans, index_trans, if_exists_trans]]
    sql_list = [sql_update_statistics, sql_update_assets]
    
    if not is_transaction:
        if sql_update_assets_related:
            sql_list.append(sql_update_assets_related)
        return {'result': DataBase().transaction(dfinfo_list, sql_list)}
    else:
        return sql_list, dfinfo_list


def utils_show_flow(wx_data):
    acc_user = wx_data['token']
    month_now = time.strftime("%Y%m", time.localtime())
    df_report = Transaction(acc_user).show_flow(month_now)
    num_days = calendar.monthrange(int(month_now[:4]),int(month_now[4:]))[1]
    days = [("0%s" if day<10 else "%s") % day for day in range(1, num_days+1)]
    df_default = pd.DataFrame(data=np.array([days]).T, columns=['day'])

    df_report_expend = df_report[(df_report['tye_flow'] == 'expend')]
    df_report_income = df_report[(df_report['tye_flow'] == 'income')]
    expend_amount = pd.merge(df_default, df_report_expend, how='left', on='day').sort_values(by=['day']).fillna(0)['amount'].to_list()
    income_amount = pd.merge(df_default, df_report_income, how='left', on='day').sort_values(by=['day']).fillna(0)['amount'].to_list()

    report = {
        'days': days,
        'expend': expend_amount,
        'income': income_amount,
    }
    return {'report': report}


def utils_show_report(wx_data):
    acc_user = wx_data['token']
    year = wx_data['year']
    month = wx_data['month']

    if month.lower() == 'all':
        date = year
        date_length = 4
    else:
        date = "%s%s" % (year, month)
        date_length = 6

    report = []
    df_report = Transaction(acc_user).show_report(date, date_length)
    for tye_flow in ('expend', 'income', 'transfer'):
        df_content = df_report[df_report['tye_flow'] == tye_flow]
        report_content = []
        for index in range(len(df_content)):
            report_content.append(df_content.iloc[index].to_dict())
        report.append(report_content)

    return {'report': report}


def utils_export_trans(wx_data):
    acc_user = wx_data['token']
    df_trans = Transaction(acc_user).export_trans()
    
    filename = "%s.xlsx" % gen_short_uuid()
    path_server = get_export_path()
    file_server = os.path.join(path_server, filename)   # 文件存放路径
    df_trans.to_excel(file_server)

    url_file = "%s/dexport/?filename=%s" % (url_base, filename)  # 文件请求下载路径
    return {'url': url_file}


# modify拆解为delete+add
def utils_modify_trans(wx_data):
    acc_user = wx_data['token']
    id = wx_data['id']
    wx_data_delete = {'token': wx_data['token'], 'id': id}
    wx_data_add = copy.deepcopy(wx_data)
    sql_list, dfinfo_list =[], []

    # delete
    sql_delete_list, dfinfo_delete_list = utils_delete_trans(wx_data_delete, is_transaction=True)
    sql_list.extend(sql_delete_list)
    dfinfo_list.extend(dfinfo_delete_list)

    # add
    sql_add_list, dfinfo_add_list = utils_add_trans(wx_data_add, is_transaction=True)
    sql_list.extend(sql_add_list)
    dfinfo_list.extend(dfinfo_add_list)

    return {'result': DataBase().transaction(dfinfo_list, sql_list)}


# 删除交易记录后，对应的资金要回流
def utils_delete_trans(wx_data, is_transaction=False):
    acc_user = wx_data['token']
    id = wx_data['id']

    t = Transaction(acc_user)
    sql_delete_trans = t.delete_trans(id, is_transaction=True)
    df_trans = t.show_trans(id=id)

    if not df_trans.empty:
        df_trans = df_trans.iloc[:1]
        tye_flow = df_trans['tye_flow'][0]
        amount = df_trans['amt_trans'][0]
        acc_asset = df_trans['acc_asset'][0]
        tye_asset = df_trans['tye_asset'][0]
        acc_asset_related = df_trans['acc_asset_related'][0]
        tye_asset_related = df_trans['tye_asset_related'][0]
        cod_trans_type = df_trans['cod_trans_type'][0]

        sql_update_assets, sql_update_assets_related = Asset(acc_user).update_assets(tye_flow, amount, acc_asset, tye_asset, acc_asset_related, tye_asset_related, tye_update='delete_trans', is_transaction=True)
        sql_update_statistics = Statistic(acc_user).update_statistics(tye_flow, amount, cod_trans_type=cod_trans_type, tye_asset=tye_asset, tye_asset_related=tye_asset_related, tye_update='delete_trans', is_transaction=True)

    dfinfo_list = []
    sql_list = [sql_delete_trans, sql_update_assets, sql_update_statistics]
    if sql_update_assets_related:
        sql_list.append(sql_update_assets_related)

    if not is_transaction:
        return {'result': DataBase().transaction(dfinfo_list, sql_list)}
    else:
        return sql_list, dfinfo_list

