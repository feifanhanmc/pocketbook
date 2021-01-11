#!/usr/bin/env python
# -*- coding: utf-8 -*-
from tools.toolkit import gen_short_uuid, get_md5, load_next_id
from database.base.database_helper import DataBase
import pandas as pd
import os
import json

file_default_transtype = 'default_transtypes.csv'


class Transtype:
    def __init__(self, acc_user, db=None, table='transtypes',
                 columns=['id', 'acc_user', 'cod_trans_type', 'txt_trans_type', 'txt_trans_type_sub', 'tye_flow',
                          'boo_active','ico_trans']):
        self.db = db
        self.table = table
        self.columns = columns
        self.acc_user = acc_user
        self.cod_trans_type = ''
        self.txt_trans_type = ''
        self.txt_trans_type_sub = ''
        self.tye_flow = ''
        self.df_transtype = pd.DataFrame()
        self.df_transtype_default = None
        self.base_path = os.path.dirname(__file__)

        if not self.db:
            self.db = DataBase()

    # 包括用户自定义交易类别和默认类别
    def show_transtypes(self, acc_user_default='dbuser',need_index=True):
        sql_show = "select * from transtypes where acc_user in ('%s', '%s') order by id asc" % (self.acc_user, acc_user_default)
        flag, result = self.db.read(sql_show)
        if flag:
            if need_index:
                result['index'] = range(len(result))
            return result
        return None

    def init_transtypes(self, df_transtypes):
        flag, result = self.db.write(df_transtypes, self.table)
        return flag, result

    def add_transtypes(self):
        pass

    def create_from_default(self):
        if not self.df_transtype_default:
            next_id = load_next_id(self.table)
            df_transtype_default = pd.read_csv(os.path.join(self.base_path, file_default_transtype))
            len_transtype_default = len(df_transtype_default)
            df_transtype_default['txt_trans_type_sub'] = ['']*len_transtype_default
            df_transtype_default['acc_user'] = [self.acc_user]*len_transtype_default
            df_transtype_default['id'] = [next_id + i for i in range(len_transtype_default)]

            flag, result = DataBase().write(df_transtype_default, self.table)
            if flag:
                self.df_transtype_default = df_transtype_default
                self.df_transtype = df_transtype_default
            return flag

    def create_from_transactions(self, df_transactions):
        self.df_transtype = self.df_transtype_default + ''


if __name__ == '__main__':
    t = Transtype('bzZgLatE')
    print(t.create_from_default())
