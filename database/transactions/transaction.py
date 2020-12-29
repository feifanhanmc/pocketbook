# -*- coding: utf-8 -*-
from tools.toolkit import gen_short_uuid, get_md5, load_next_id
from database.base.database_helper import DataBase
import pandas as pd


class Transaction:
    def __init__(self, acc_asset, table='transactions',
                 columns=['id', 'acc_asset', 'nam_asset', 'amt_trans', 'dte_trans', 'tme_trans', 'acc_asset_related',
                          'cod_trans_type', 'txt_trans_type', 'txt_trans_type_sub', 'txt_remark']):
        self.table = table
        self.acc_asset = acc_asset
        self.nam_asset = ''
        self.amt_trans = 0.0
        self.dte_trans = ''
        self.tme_trans = ''
        self.acc_asset_related = ''
        self.cod_trans_type = ''
        self.txt_trans_type = ''
        self.txt_trans_type_sub = ''
        self.txt_remark = ''

    @staticmethod
    def revert_dict(dic):
        res = {}
        for key, value in dic.items():
            res[value] = key
        return res
    
    def create_from_transactions(self, file_transactions):
        load
        next_id = load_next_id()



filename = '网易有钱记账数据.xlsx'

columns_convert_dict = {
    'dte_trans': '时间',
    'nam_acc': '账户',
    'tye_trans': '大类',
    'tye_trans_sub': '小类',
    'amt_trans': '金额',
    'txt_remark': '备注'
}





def date_format(date):
    return date.replace('-', '')[:8]


def process_column_dtype(table_structure):
    column_dtype = {}
    values_fillna = {}
    for Field, Type in table_structure.values[:, :2]:
        db_field = Field.lower()
        if db_field in columns_convert_dict.keys():
            file_field = columns_convert_dict[db_field]
            if Type.startswith('decimal'):
                column_dtype[file_field] = float
                values_fillna[file_field] = 0.0
            elif Type.startswith('integer'):
                column_dtype[file_field] = int
                values_fillna[file_field] = 0
            else:
                column_dtype[file_field] = str
                values_fillna[file_field] = ''
    return column_dtype, values_fillna


def extract_date_column():
    date_columns = []
    for key, value in columns_convert_dict.items():
        if key.startswith('dte'):
            date_columns.append(value)
    return date_columns


def auto_fill(df, auto_fill_columns):
    for column in auto_fill_columns:
        if column not in columns_convert_dict.keys():
            pass



def transactions_file2db(fn, table='transactions', auto_fill_columns=['acc_asset'], acc_user=None):
    db = DataBase()
    flag, df_table_structure = db.read('desc %s' % table)
    if flag:
        date_columns = extract_date_column()
        column_dtype, values_fillna = process_column_dtype(df_table_structure)
        df = pd.read_excel(fn, dtype=column_dtype)[column_dtype.keys()].fillna(value=values_fillna)
        for date_column in date_columns:
            df[date_column] = df[date_column].apply(date_format)
        df = df.rename(columns=revert_dict(columns_convert_dict))

        df['acc_asset'] = [gen_short_uuid()]*len(df)
        print(df)
        flag, result = db.write(df, table)
    print(flag, df_table_structure)


transactions_file2db(filename)
