#-*- coding:utf-8 -*-
from wxpy import *
from webapp.mysql_helper import mysql_db
from webapp.config import mysql_config
import hashlib

def conver2md5(s):
    md5 = hashlib.md5()
    md5.update(s)
    return md5.hexdigest()

def init():
    pass

def signin(wx_account, wx_password_md5, table_name='wxbot'):
    db = mysql_db(mysql_config)
    check_sql = "select count(*) from %s where account='%s' and password='%s'; " % (table_name, wx_account, wx_password_md5)
    check_result = db.select(check_sql)
    if check_result:
        return True
    return False

def signup(wx_account, wx_password_md5, table_name='wxbot'):
    result_flag = False

    db = mysql_db(mysql_config)
    check_account_sql = "select count(*) from %s where account='%s'; " % (table_name, wx_account)
    check_account_result = db.select(check_account_sql, auto_close=False)
    if not check_account_result:
        data_headers = ['account', 'password']
        data = [[wx_account, wx_password_md5]]
        db.insert(table_name, data_headers, data, auto_close=False)
        result_flag = True
    db.close()

    return result_flag

def check_friends_sign(wx_account, wx_password_md5, table_name='wxbot'):
    res = {}

    db = mysql_db(mysql_config)
    check_sql = "select count(*) from %s where account='%s' and password='%s'; " % (table_name, wx_account, wx_password_md5)
    check_result = db.select(check_sql)
    if check_result:
        return True
    return False

