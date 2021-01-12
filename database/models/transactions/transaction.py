#!/usr/bin/env python
# -*- coding: utf-8 -*-
from tools.toolkit import gen_short_uuid, get_md5, load_next_id
from database.base.database_helper import DataBase
import pandas as pd


class Transaction:
    def __init__(self, acc_user, acc_asset='', db=None, table='transactions',
                 columns=['id', 'acc_user', 'acc_asset', 'nam_asset', 'rmk_asset', 'amt_trans', 'tye_asset', 'tye_flow', 'dte_trans',
                          'tme_trans', 'acc_asset_related', 'nam_asset_related', 'rmk_asset_related',
                          'ico_asset_related', 'tye_asset_related','cod_trans_type', 'txt_trans_type', 'txt_trans_type_sub', 'txt_remark',
                          'ico_trans']):
        self.db = db
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

        if not db:
            self.db = DataBase()

    def show_trans(self, acc_asset=None):
        sql_asset = " "
        if acc_asset:
            sql_asset = " and (acc_asset='%s' or acc_asset_related='%s') " % (acc_asset, acc_asset)
        sql_show = "select * from transactions where acc_user='%s' %s order by dte_trans desc, id desc" % \
                   (self.acc_user, sql_asset)
        flag, result = self.db.read(sql_show)
        if flag:
            result['index'] = range(len(result))
            return result
        return pd.DataFrame()

    def add_trans(self, dict_tran, is_transaction=False):
        data, columns = [], []
        for key, value in dict_tran.items():
            columns.append(key)
            data.append(value)
        data_trans = pd.DataFrame(data=[data], columns=columns)
        if not is_transaction:
            flag, result = self.db.write(data_trans, self.table)
            if not flag:
                print(result)
            return flag
        else:
            return data_trans, self.table, False, 'append'

    def show_report(self):
        sql_show = """
            select 
                tye_flow,
                left(dte_trans,6) as month,
                right(dte_trans,2) as day,
                sum(case when tye_flow='expend' then -1*amt_trans else amt_trans end) as amt_day
            from %s
            where acc_user='%s'
            and tye_flow in ('income', 'expend')
            group by tye_flow, month, day
            order by tye_flow, month desc, day
            """ % (self.table, self.acc_user)
        flag, result = self.db.read(sql_show)
        if flag:
            result['index'] = range(len(result))
            return result
        return pd.DataFrame()

    def update_trans(self, dict_tran):
        # 逻辑比较复杂
        # 关联账户、交易类型、金额等变化后都会引起一系列账户的变化……最后再写
        # nam_asset_related
        # cod_trans_type
        # ico_trans
        """
        sql_template = "update transactions set % where acc_user='%s' and acc_asset='%s' and id='%s'"
        sql_list_update = []
        for key, value in dict_tran.items():
            # if key == ''
            if key in ['amt_trans', 'tye_flow', 'dte_trans', 'tme_trans', 'acc_asset_related', 'cod_trans_type',
                       'txt_remark']:
                sql_list_update.append(" %s='%s' " % (key, value))
        sql_str_update = ",".join(sql_list_update)
        sql_update = sql_template % (sql_str_update, self.acc_user, dict_tran['acc_asset'], dict_tran['id'])
        self.db.execute(sql_update)
        return True
        """
        pass

    def delete_trans(self, dict_tran):
        # 删除一笔交易后，资金要回笼
        # 如果涉及到的相关账户已经没了，要转到应收/应付账户还是该怎么做……
        # 最后在做
        """
        sql_delete = "update assets set boo_active=0 where acc_user='%s' and acc_asset='%s'" % \
                     (self.acc_user, dict_tran['acc_asset'])
        self.db.execute(sql_delete)
        return True
        """
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

    def create_from_transactions(self, file_transactions, dic_db2file_columns):
        flag, result = self.db.read('desc %s' % self.table)
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
            next_id = load_next_id(self.table, self.db)
            df_data['id'] = [next_id + i for i in range(len_df_data)]
            df_data['acc_user'] = [self.acc_user] * len_df_data
            for column in self.columns:
                if column not in df_data.columns:
                    df_data[column] = [self.vdefault_columns[column]] * len_df_data
            flag, result = self.db.write(df_data, self.table)
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

