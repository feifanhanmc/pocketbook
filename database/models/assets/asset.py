#!/usr/bin/env python
# -*- coding: utf-8 -*-
from tools.toolkit import gen_short_uuid, get_md5, load_next_id
from database.base.database_helper import DataBase
import pandas as pd


class Asset:
    def __init__(self, acc_user, db=None, table='assets',
                 columns=['id', 'acc_user', 'acc_asset', 'nam_asset', 'rmk_asset', 'tye_asset', 'amt_asset',
                          'ico_asset', 'boo_active']):
        self.db = db
        self.table = table
        self.columns = columns
        self.acc_user = acc_user
        self.df_asset = pd.DataFrame()

        if not self.db:
            self.db = DataBase()

    def show_assets(self, flag_active=1):
        """
        :param db:
        :param flag_active: 1, 0, 'all'
        :return:
        """
        sql_active = " "
        if flag_active in (0, 1):
            sql_active = " and boo_active='%s'" % flag_active
        sql_show = "select * from assets where acc_user='%s' %s order by id" % (self.acc_user, sql_active)
        flag, result = self.db.read(sql_show)
        if flag:
            return result
        return None

    def add_assets(self, dict_asset):
        dict_asset['acc_asset'] = gen_short_uuid()
        data, columns = [], []
        for key, value in dict_asset.items():
            columns.append(key)
            data.append(value)
        data_asset = pd.DataFrame(data=[data], columns=columns)
        flag, result = self.db.write(data_asset, self.table)
        print(data_asset, flag, result)
        return flag

    def update_assets(self, dict_asset):
        sql_template = "update assets set % where acc_user='%s' and acc_asset='%s'"
        sql_list_update = []
        for key, value in dict_asset.items():
            if key in ['nam_asset', 'amt_asset']:
                sql_list_update.append(" %s='%s' " % (key, value))
        sql_str_update = ",".join(sql_list_update)
        sql_update = sql_template % (sql_str_update, self.acc_user, dict_asset['acc_asset'])
        self.db.execute(sql_update)
        return True

    def delete_assets(self, dict_asset):
        sql_delete = "update assets set boo_active=0 where acc_user='%s' and acc_asset='%s'" % \
                     (self.acc_user, dict_asset['acc_asset'])
        self.db.execute(sql_delete)
        return True

    # 适用于导入交易记录时自动创建交易类型
    def create_from_transactions(self, df_transactions):
        next_id = load_next_id()

        data_asset = []
        nam_asset_list = df_transactions['nam_asset'].unique()
        for i in range(len(nam_asset_list)):
            id = next_id + i
            nam_asset = nam_asset_list[i]
            acc_asset = gen_short_uuid()
            tye_asset = ''
            amt_asset = 0.0
            data_asset.append([id, self.acc_user, acc_asset, nam_asset, tye_asset, amt_asset])
        self.df_asset = pd.DataFrame(data=data_asset, columns=self.columns)
        flag, result = DataBase().write(self.df_asset, self.table)
        print(flag, result)

        return self.acc_user


if __name__ == '__main__':
    a = Asset()
    a.create_from_transactions(pd.DataFrame())
