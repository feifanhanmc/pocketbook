#!/usr/bin/env python
# -*- coding: utf-8 -*-
from database.base.database_helper import DataBase
from data_helper import get_backup_path
from tools.toolkit import get_num_records
import time
import os


def mkdir(acc_user):
    name_dir = 'backup_%s_%s' % (acc_user, time.strftime("%Y%m%d_%H%M%S"))
    path_data = get_backup_path()
    path_full = os.path.join(path_data, name_dir)
    os.mkdir(path_full)
    return path_full


def export_data(acc_user, db=None, batch=50000, tables=['assets', 'transactions', 'transtypes']):
    if not db:
        db = DataBase()
    path = mkdir(acc_user)
    flag = False
    for table in tables:
        num_line = get_num_records(table, db, acc_user)
        filename = os.path.join(path, '%s.csv' % table)
        for index in range(1 + int(num_line / batch)):
            offset = batch * index
            flag, result = db.read("select * from %s where acc_user='%s' limit %s,%s"
                                   % (table, acc_user, offset, batch))
            if flag:
                result.to_csv(filename, index=False, mode='a', header=True if index == 0 else None)  # 追加写入
            else:
                print(result)
    return flag


if __name__ == '__main__':
    export_data('lxnkf54X')
