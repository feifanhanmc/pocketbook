# -*- coding: utf-8 -*-
import os
from database.base.database_helper import DataBase
from database.backup.backupdb import backup_db
from database.models.users.user import User
from database.models.transtypes.transtype import Transtype
from database.models.transactions.transaction import Transaction
from database.models.assets.asset import Asset
import pandas as pd

file_init_sql = 'initdb.sql'
base_path = os.path.dirname(__file__)


def init_data(db):
    for table in ['users', 'assets', 'transtypes', 'transactions']:
        filename = 'init_%s.csv' % table
        filename_full = os.path.join(base_path, filename)
        df_init = pd.read_csv(filename_full).fillna('')
        db.write(df_init, table)
    return True


def init_db(db):
    with open(os.path.join(base_path, file_init_sql), 'r') as fp:
        raw_sql = fp.read().strip()
    for sql in raw_sql.split('go'):
        sql = sql.strip()
        db.execute(sql)
    return True


def main(db=None):
    if not db:
        db = DataBase()
    if backup_db(db):
        if init_db(db):
            if init_data(db):
                return True
    return False


if __name__ == '__main__':
    main()

