#!/usr/bin/env python
# -*- coding: utf-8 -*-
from database.models.transactions.transaction import Transaction
from database.models.statistics.statistic import Statistic
from database.base.database_helper import DataBase


def utils_show_trans(wx_data):
    acc_user = wx_data['token']
    acc_asset = wx_data.get('acc_asset', None)
    df_trans = Transaction(acc_user).show_trans(acc_asset)
    data = []
    for index in range(len(df_trans)):
        data.append(df_trans.iloc[index].to_dict())
    return {'trans': data}


def utils_add_trans(wx_data):
    acc_user = wx_data['token']
    del wx_data['token']
    wx_data['acc_user'] = acc_user

    type_amount = wx_data['tye_flow']
    amount = wx_data['amt_trans']
    tye_asset = wx_data['tye_asset']
    tye_asset_related = wx_data.get('tye_asset_related', '')
    cod_trans_type = wx_data.get('cod_trans_type', '')

    df_trans, table_trans, index_trans, if_exists_trans = Transaction(acc_user).add_trans(wx_data, is_transaction=True)
    sql_update_statistics = Statistic(acc_user).update_statistics(type_amount, amount, cod_trans_type=cod_trans_type, tye_asset=tye_asset, tye_asset_related=tye_asset_related, is_transaction=True)

    conn = DataBase().gen_transaction_conn()
    tran = conn.begin()
    try:
        df_trans.to_sql(table_trans, con=conn, index=index_trans, if_exists=if_exists_trans)
        conn.execute(sql_update_statistics)
        tran.commit()
        return {'result': True}
    except Exception as e:
        print(str(e))
        tran.rollback()
        return {'result': False}


def utils_update_trans():
    pass


def utils_delete_trans():
    pass



