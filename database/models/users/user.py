#!/usr/bin/env python
# -*- coding: utf-8 -*-
from tools.toolkit import gen_short_uuid, get_md5, load_next_id
from database.base.database_helper import DataBase
import pandas as pd


class User:
    def __init__(self, acc_user=None, pwd_user_md5=None, db=None, table='users',
                 columns=['id', 'acc_user', 'pwd_user_md5', 'nam_user', 'vlu_email', 'vlu_phone', 'vlu_openid',
                          'nam_nick', 'cod_gender', 'vlu_lang', 'vlu_city', 'vlu_prov', 'vlu_country', 'url_avatar' ]):
        self.db = db
        self.table = table
        self.columns = columns
        self.acc_user = acc_user
        self.pwd_user_md5 = pwd_user_md5
        self.nam_user = ''
        self.vlu_email = ''
        self.vlu_phone = ''
        self.vlu_openid = ''

        if not self.db:
            self.db = DataBase()

    def create(self, nam_user=None):
        if not self.acc_user:
            self.acc_user = gen_short_uuid()
        if not self.nam_user:
            self.nam_user = gen_short_uuid()
        self.pwd_user_md5 = get_md5(self.acc_user)

        df_user = pd.DataFrame(
            data=[[self.acc_user, self.pwd_user_md5, self.nam_user, self.vlu_email, self.vlu_phone, self.vlu_openid]],
            columns=self.columns[1:7])
        flag, result = self.db.write(df_user, self.table)
        if flag:
            return self.acc_user
        return flag

    def user_check(self, openid, nam_user=''):
        self.vlu_openid = openid
        sql_check = "select acc_user from %s where vlu_openid='%s' " % (self.table, self.vlu_openid)
        flag, result = self.db.read(sql_check)
        print(flag, result)
        if flag and not result.empty:
            self.acc_user = result['acc_user'][0]
        else:
            self.acc_user = self.create(nam_user=nam_user)
        return self.acc_user
    
    def save_userinfo(self, userinfo):
        # 若存在acc_user则update，反之创建
        pass

    def db_init(self):
        pass


if __name__ == '__main__':
    u = User()
    print(u.create('韩大爷'))
