#!/usr/bin/env python
# -*- coding: utf-8 -*-
from tools.toolkit import gen_short_uuid, get_md5, load_next_id
from database.base.database_helper import DataBase
import pandas as pd


class User:
    def __init__(self, acc_user=None, pwd_user_md5=None, table='users',
                 columns=['id', 'acc_user', 'pwd_user_md5', 'nam_user', 'vlu_email', 'vlu_phone', 'vlu_openid']):
        self.table = table
        self.columns = columns
        self.acc_user = acc_user
        self.pwd_user_md5 = pwd_user_md5
        self.nam_user = ''
        self.vlu_email = ''
        self.vlu_phone = ''
        self.vlu_openid = ''

    def create(self, nam_user=None):
        self.acc_user = gen_short_uuid()
        if not self.nam_user:
            self.nam_user = gen_short_uuid()
        self.pwd_user_md5 = get_md5(self.acc_user)

        db = DataBase()
        next_id = load_next_id(self.table)
        df_user = pd.DataFrame(
            data=[[next_id, self.acc_user, self.pwd_user_md5, self.nam_user, self.vlu_email, self.vlu_phone, self.vlu_openid]],
            columns=self.columns)
        flag, result = db.write(df_user, self.table)
        if flag:
            return self.acc_user
        return flag

    def user_check(self, openid, nam_user='', db=None):
        if not db:
            db = DataBase()
        self.vlu_openid = openid
        sql_check = "select acc_user from %s where vlu_openid='%s' " % (self.table, self.vlu_openid)
        flag, result = db.read(sql_check)
        print(flag, result)
        if flag and not result.empty:
            self.acc_user = result['acc_user'][0]
        else:
            self.acc_user = self.create(nam_user=nam_user)
        return self.acc_user
    
    def save_userinfo(self, userinfo):
        # 若存在acc_user则update，反之创建
        pass


if __name__ == '__main__':
    u = User()
    print(u.create('韩大爷'))
