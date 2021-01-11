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
            result['index'] = range(len(result))
            return result
        return None

    def add_assets(self, dict_asset, is_transaction=False):
        dict_asset['acc_asset'] = gen_short_uuid()
        data, columns = [], []
        for key, value in dict_asset.items():
            columns.append(key)
            data.append(value)
        data_asset = pd.DataFrame(data=[data], columns=columns)
        if not is_transaction:
            flag, result = self.db.write(data_asset, self.table)
            return flag
        else:
            return data_asset, self.table, False, 'append'

    def modify_assets_info(self, dict_asset):
        sql_template = "update assets set % where acc_user='%s' and acc_asset='%s'"
        sql_list_modify= []
        for key, value in dict_asset.items():
            if key in ['nam_asset', 'amt_asset']:
                sql_list_modify.append(" %s='%s' " % (key, value))
        sql_str_modify = ",".join(sql_list_modify)
        sql_modify = sql_template % (sql_str_modify, self.acc_user, dict_asset['acc_asset'])
        flag, result = self.db.execute(sql_modify)
        if not flag:
            print(result)
        return flag

    def update_assets(self, tye_flow, amount, acc_asset, tye_asset, acc_asset_related, tye_asset_related, is_transaction=False):
        sql_update_assets, sql_update_assets_related = "", ""
        sql_template = "update %s set amt_asset=amt_asset %s %s where acc_user='%s' and acc_asset='%s' "
        if tye_flow == 'transfer':  # 账面金额一减一增
            sql_update_assets = sql_template % (self.table, '-', amount, self.acc_user, acc_asset)
            sql_update_assets_related = sql_template % (self.table, '+', amount, self.acc_user, acc_asset_related)
        elif tye_flow in ('income', 'expend'):
            sql_update_assets = sql_template % (self.table, '+', amount, self.acc_user, acc_asset)
        else:
            pass
        
        print('sql_update_assets', sql_update_assets)
        print('sql_update_assets_related', sql_update_assets_related)

        if not is_transaction:
            if sql_update_assets:
                flag, result = self.db.execute(sql_update_assets)
                if not flag:
                    print(result)
                    return False
                else:
                    if sql_update_assets_related:
                        flag, result = self.db.execute(sql_update_assets_related)
                        if not flag:
                            print(result)
                            return False
            return True
        else:
            return sql_update_assets, sql_update_assets_related

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
