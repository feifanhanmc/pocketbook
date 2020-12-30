# -*- coding: utf-8 -*-
from uuid import uuid4
import hashlib
from database.base.database_helper import DataBase

uuid_chars = ("a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s",
              "t", "u", "v", "w", "x", "y", "z", "0", "1", "2", "3", "4", "5","6", "7", "8", "9", "A", "B",
              "C", "D", "E", "F", "G", "H", "I","J", "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T", "U",
              "V", "W", "X", "Y", "Z")


def gen_short_uuid():
    uuid = str(uuid4()).replace('-', '')
    short_uuid = ''
    for i in range(0, 8):
        sub = uuid[i * 4: i * 4 + 4]
        x = int(sub,16)
        short_uuid += uuid_chars[x % 0x3E]
    return short_uuid


def get_md5(content):
    md5hash = hashlib.md5(content.encode('utf8'))
    md5 = md5hash.hexdigest()
    return md5


def get_num_records(table, db=None, acc_user=None):
    if not db:
        db = DataBase()
    sql_condition = ""
    if acc_user:
        sql_condition = " where acc_user='%s'" % acc_user
    num_records = 0
    flag, result = (db.read("select count(*) as cnt from %s %s" % (table, sql_condition)))
    if flag and not result.empty:
        num_records = int(result['cnt'][0])
    return num_records


def load_next_id(table, db=None):
    if not db:
        db = DataBase()
    next_id = 1
    flag, result = (db.read('select id from %s order by id desc' % table))
    if flag and not result.empty:
        max_id = int(result['id'][0])
        next_id = max_id + 1
    return next_id


if __name__ == '__main__':
    print(gen_short_uuid())
    # print(get_md5('aa'))
    print(load_next_id('users'))
    print(get_num_records('transactions', acc_user='lxnkf54X'))
