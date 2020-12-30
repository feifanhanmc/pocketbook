# -*- coding: utf-8 -*-
from database.base.database_helper import DataBase
from data.data_helper import get_data_path
from tools.toolkit import load_next_id
import time
import os


def mkdir():
    name_dir = 'backup_all_%s' % time.strftime("%Y%m%d_%H%M%S")
    path_data = get_data_path()
    path_full = os.path.join(path_data, name_dir)
    os.mkdir(path_full)
    return path_full


def backup_db(db=None, batch=50000):
    if not db:
        db = DataBase()
    path = mkdir()
    flag, result = db.read('show tables')
    if flag:
        df_tables = result
        for table in df_tables.values[:, 0]:
            num_line = load_next_id(table, db) - 1
            filename = os.path.join(path, '%s.csv' % table)
            for index in range(1 + int(num_line / batch)):
                offset = batch * index
                flag, result = db.read('select * from %s limit %s,%s' % (table, offset, batch))
                if flag:
                    result.to_csv(filename, index=False, mode='a', header=True if index == 0 else None)  # 追加写入
                else:
                    print(result)
    else:
        print(result)
    return flag


if __name__ == '__main__':
    backup_db()
