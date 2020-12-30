# -*- coding: utf-8 -*-
from database.models.users.user import User
from database.models.transactions.transaction import Transaction
from database.base.database_helper import DataBase
from database.init.initdb import init_db


class Test:
    def __init__(self):
        self.db = None
        self.acc_user = None

    def create_user(self, nam_user='韩大爷'):
        acc_user = User().create(nam_user=nam_user)
        if acc_user:
            self.acc_user

    def import_transtypes(self):
        pass

    def import_transactions(self):
        excel_transactions = 'transactions_upload.xlsx'
        dict_db2file_columns = {
            'dte_trans': '时间',
            'nam_asset': '账户',
            'txt_trans_type': '大类',
            'txt_trans_type_sub': '小类',
            'amt_trans': '金额',
            'nam_asset_related': '关联账户',
            'txt_remark': '备注'
        }
        r = Transaction(acc_user=self.acc_user).create_from_transactions(excel_transactions, dict_db2file_columns)
        print(r)

    def run(self):
        self.db = DataBase()
        init_db(self.db)


if __name__ == '__main__':
    t = Test()
    t.run()
