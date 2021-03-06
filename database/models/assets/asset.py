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

    def show_assets(self, acc_asset=None, flag_active=1, need_index=True):
        """
        :param db:
        :param flag_active: 1, 0, 'all'
        :return:
        """
        sql_active, sql_asset = " ", " "
        if flag_active in (0, 1):
            sql_active = " and boo_active='%s' " % flag_active
        if acc_asset:
            sql_asset = " and acc_asset='%s' " % acc_asset
        sql_show = "select * from assets where acc_user='%s' %s %s order by id" % (self.acc_user, sql_active, sql_asset)

        flag, result = self.db.read(sql_show)
        if flag:
            if need_index:
                result['index'] = range(len(result))
            return result
        return pd.DataFrame()

    def add_assets(self, dict_asset, is_transaction=False):
        if not dict_asset.has_key('acc_asset'):
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

    # 用于资产账户信息的更改
    def modify_assets(self, acc_asset, df_asset, is_transaction=False):
        # 由于中文编码有问题，所以update改为delete+insert
        sql_delete = "delete from %s where acc_user='%s' and acc_asset='%s'" % (self.table, self.acc_user, acc_asset)
        if not is_transaction:
            flag, result = self.db.execute(sql_delete)
            if not flag:
                print(result)
                return False
            else:
                flag, result = self.db.write(df_asset, self.table)
                if not flag:
                    print(result)
                    return False
            return True
        else:
            return sql_delete, self.table, False, 'append'

    # 用于交易等相关数据库事务的更新
    def update_assets(self, tye_flow, amount, acc_asset, tye_asset, acc_asset_related, tye_asset_related, tye_update='add', is_transaction=False):
        """
        :param tye_flow: ['income', 'expend', 'transfer', 'adjust']
        :param tye_update: ['add', 'delete_trans', 'delete_asset']
        """
        sql_update_assets, sql_update_assets_related = "", ""
        sql_template = "update %s set amt_asset=amt_asset %s %s where acc_user='%s' and acc_asset='%s' "
        if tye_update == 'add':
            if tye_flow == 'transfer':  # 账面金额一减一增
                sql_update_assets = sql_template % (self.table, '-', amount, self.acc_user, acc_asset)
                sql_update_assets_related = sql_template % (self.table, '+', amount, self.acc_user, acc_asset_related)
            elif tye_flow in ('income', 'expend'):
                sql_update_assets = sql_template % (self.table, '+', amount, self.acc_user, acc_asset)
            else:
                pass
        elif tye_update == 'delete_trans':  # 删除交易记录会引起资产账户变动
            if tye_flow == 'transfer':
                sql_update_assets = sql_template % (self.table, '+', amount, self.acc_user, acc_asset)
                sql_update_assets_related = sql_template % (self.table, '-', amount, self.acc_user, acc_asset_related)
            elif tye_flow in ('income', 'expend', 'adjust'):
                sql_update_assets = sql_template % (self.table, '-', amount, self.acc_user, acc_asset)
            else:
                pass
        elif tye_update == 'delete_asset':
            pass
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

    # 由于删除账户会有资产变动，因此一般情况下禁止直接删除账户，而不做后续处理
    def delete_assets(self, acc_asset, is_transaction=True):
        sql_delete = "delete from %s where acc_user='%s' and acc_asset='%s' " % (self.table, self.acc_user, acc_asset)
        if not is_transaction:
            flag, result = self.db.execute(sql_delete)
            if not flag:
                print(result)
            return flag
        else:
            return sql_delete

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
