#!/usr/bin/env python
# -*- coding: utf-8 -*-
from tools.toolkit import gen_short_uuid, get_md5, load_next_id
from database.base.database_helper import DataBase
import pandas as pd


class Transaction:
    def __init__(self, acc_user, acc_asset='', table='transactions',
                 columns=['id', 'acc_user', 'acc_asset', 'nam_asset', 'amt_trans', 'tye_flow', 'dte_trans',
                          'tme_trans', 'acc_asset_related', 'nam_asset_related', 'cod_trans_type', 'txt_trans_type',
                          'txt_trans_type_sub', 'txt_remark']):
        self.table = table
        self.columns = columns
        self.dtype_columns = {}
        self.vdefault_columns = {}
        self.acc_user = acc_user
        self.acc_asset = acc_asset
        self.nam_asset = ''
        self.amt_trans = 0.0
        self.tye_flow = ''
        self.dte_trans = ''
        self.tme_trans = ''
        self.acc_asset_related = ''
        self.nam_asset_related = ''
        self.cod_trans_type = ''
        self.txt_trans_type = ''
        self.txt_trans_type_sub = ''
        self.txt_remark = ''

    def insert(self, tran_data, db=None):
        if not db:
            self.db = DataBase()
        id = load_next_id(self.table, self.db)
        self.acc_asset = tran_data['acc_asset']
        self.amt_trans = tran_data['amt_trans']
        data = [[id, self.acc_user, self.acc_asset, self.nam_asset, self.amt_trans, self.tye_flow, self.dte_trans,
                self.tme_trans, self.acc_asset_related, self.nam_asset_related, self.cod_trans_type, self.txt_trans_type,
                self.txt_trans_type_sub, self.txt_remark]]
        df_tran = pd.DataFrame(data=data, columns=self.columns)
        flag, result = self.db.write(df_tran, self.table)
        if not flag:
            print(result)
        return flag

    def update(self):
        pass

    def delete(self):
        pass

    @staticmethod
    def revert_dict(dic):
        res = {}
        for key, value in dic.items():
            res[value] = key
        return res

    @staticmethod
    def date_format(date, target_format='yyyymmdd'):
        def date_fill(date_part):
            if len(date_part) == 1:
                date_part = '0%s' % date_part
            return date_part[:2]

        for seg in ['-', '/']:
            if seg in date:
                y, m, d = date.split(' ')[0].split(seg)[:3]
                m = date_fill(m)
                d = date_fill(d)
                date = '%s%s%s' % (y, m, d)
                break
        return date[:8]

    @staticmethod
    def extract_date_column(dic_db2file_columns):
        date_columns = []
        for key, value in dic_db2file_columns.items():
            if key.startswith('dte'):
                date_columns.append(value)
        return date_columns

    def process_column_dtype(self, table_structure, dic_db2file_columns):
        if not self.dtype_columns:
            for Field, Type in table_structure.values[:, :2]:
                column = Field.lower()
                if Type.startswith('decimal'):
                    self.dtype_columns[column] = float
                    self.vdefault_columns[column] = 0.0
                elif Type.startswith('integer'):
                    self.dtype_columns[column] = int
                    self.vdefault_columns[column] = 0
                else:
                    self.dtype_columns[column] = str
                    self.vdefault_columns[column] = ''

        dtype_file_columns = {}
        vdefault_file_columns = {}
        for column, file_column in dic_db2file_columns.items():
            dtype_file_columns[file_column] = self.dtype_columns[column]
            vdefault_file_columns[file_column] = self.vdefault_columns[column]

        return dtype_file_columns, vdefault_file_columns

    def create_from_transactions(self, file_transactions, dic_db2file_columns, db=None):
        if not db:
            db = DataBase()
        flag, result = db.read('desc %s' % self.table)
        if flag:
            df_table_structure = result
            date_columns = self.extract_date_column(dic_db2file_columns)
            dtype_file_columns, vdefault_file_columns = self.process_column_dtype(df_table_structure,
                                                                                  dic_db2file_columns)
            df_data = pd.read_excel(file_transactions, dtype=dtype_file_columns)[dtype_file_columns.keys()].\
                fillna(value=vdefault_file_columns)
            for date_column in date_columns:
                df_data[date_column] = df_data[date_column].apply(self.date_format)
            df_data = df_data.rename(columns=self.revert_dict(dic_db2file_columns))
            # auto fill
            len_df_data = len(df_data)
            next_id = load_next_id(self.table, db)
            df_data['id'] = [next_id + i for i in range(len_df_data)]
            df_data['acc_user'] = [self.acc_user] * len_df_data
            for column in self.columns:
                if column not in df_data.columns:
                    df_data[column] = [self.vdefault_columns[column]] * len_df_data
            flag, result = db.write(df_data, self.table)
            if not flag:
                print(result)
            return flag
        return flag


if __name__ == '__main__':
    excel_transactions = 'transactions_upload.xlsx'
    dict_db2file_columns = {
        'dte_trans': '时间',
        'nam_asset': '账户',
        'txt_trans_type': '大类',
        'txt_trans_type_sub': '小类',
        'amt_trans': '金额',
        'nam_asset_related': '关联账户',
        'txt_remark': '备注',
        'tye_flow': '流向'
    }
    r = Transaction(acc_user='lxnkf54X').create_from_transactions(excel_transactions, dict_db2file_columns)
    print(r)

