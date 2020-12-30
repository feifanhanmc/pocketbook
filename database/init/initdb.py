# -*- coding: utf-8 -*-
import os
from database.base.database_helper import DataBase
from database.backup.backupdb import backup_db

file_init_sql = 'initdb.sql'
base_path = os.path.dirname(__file__)


def init_db(db=None):
    if not db:
        db = DataBase()
    if backup_db(db):
        with open(os.path.join(base_path, file_init_sql), 'r') as fp:
            raw_sql = fp.read().strip()
        for sql in raw_sql.split('go'):
            sql = sql.strip()
            db.execute(sql)
        return True
    return False


if __name__ == '__main__':
    init_db()

