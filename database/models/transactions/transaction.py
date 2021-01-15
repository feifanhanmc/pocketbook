#!/usr/bin/env python
# -*- coding: utf-8 -*-
from tools.toolkit import gen_short_uuid, get_md5, load_next_id
from database.base.database_helper import DataBase
import pandas as pd

dic_trans4assets_adjust = {
    'acc_user': '',
    'acc_asset': '',
    'nam_asset': '',
    'rmk_asset': '',
    'amt_trans': '',         
    'tye_asset': '',         
    'tye_flow': 'adjust',          
    'dte_trans': '',         
    'cod_trans_type': 'W51hSzBL',    
    'txt_trans_type': '资金调整',    
    'ico_trans': 'adjust'        
}


class Transaction:
    def __init__(self, acc_user, acc_asset='', db=None, table='transactions',
                 columns=['id', 'acc_user', 'acc_asset', 'nam_asset', 'rmk_asset', 'amt_trans', 'tye_asset', 'ico_asset', 'tye_flow', 
                          'dte_trans', 'tme_trans', 'acc_asset_related', 'nam_asset_related', 'rmk_asset_related',
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

    def show_trans(self, acc_asset=None, id=None):
        sql_asset, sql_id = " ", " "
        if acc_asset:
            sql_asset = " and (acc_asset='%s' or acc_asset_related='%s') " % (acc_asset, acc_asset)
        if id:
            sql_id = " and id=%s " % id
        sql_show = "select * from transactions where acc_user='%s' %s %s order by dte_trans desc, id desc" % \
                   (self.acc_user, sql_asset, sql_id)
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

    def show_flow(self, month_now):
        sql_show = """
            select 
                tye_flow,
                right(dte_trans,2) as day,
                sum(case when tye_flow='expend' then -1*amt_trans else amt_trans end) as amount
            from %s
            where acc_user='%s'
            and left(dte_trans,6)='%s'
            and tye_flow in ('income', 'expend')
            group by tye_flow, day
            order by tye_flow, day
            """ % (self.table, self.acc_user, month_now)
        flag, result = self.db.read(sql_show)
        if flag:
            return result
        return pd.DataFrame()

    def show_report(self, date, date_length):
        sql_show = """
            select 
                tye_flow,
                cod_trans_type,
                txt_trans_type,
                ico_trans,
                sum(case when tye_flow='expend' then -1*amt_trans else amt_trans end) as amount,
                count(*) as cnt
            from %s
            where acc_user='%s'
            and left(dte_trans,%s)='%s'
            and tye_flow in ('income', 'expend', 'transfer')
            group by tye_flow, cod_trans_type, txt_trans_type, ico_trans
            order by tye_flow, amount desc
            """ % (self.table, self.acc_user, date_length, date)
        flag, result = self.db.read(sql_show)
        if flag:
            return result
        return pd.DataFrame()

    def export_trans(self):   
        sql_export = """
            select 
                dte_trans as `日期`,
                case when amt_trans<0 then -1*amt_trans else amt_trans end as `金额`,
                case 
                    when tye_flow='income' then '流入' 
                    when tye_flow='expend' then '流出' 
                    else '转账' end as `资金流向`,
                txt_trans_type as `交易类型`,
                rmk_asset as `账户名称`,
                rmk_asset_related as `相关账户名称`,
                txt_remark as `备注`
            from %s
            where acc_user='%s'
        """ % (self.table, self.acc_user)
        flag, result = self.db.read(sql_export)
        if flag:
            return result
        return pd.DataFrame()


    # 由于删除交易记录会有资金回流，因此一般情况下禁止直接删除记录，而不做后续处理
    def delete_trans(self, id, is_transaction=True):
        sql_delete = "delete from %s where acc_user='%s' and id=%s " % (self.table, self.acc_user, id)
        if not is_transaction:
            flag, result = self.db.execute(sql_delete)
            if not flag:
                print(result)
            return flag
        else:
            return sql_delete


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

