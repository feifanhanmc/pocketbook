#!/usr/bin/env python
# -*- coding: utf-8 -*-
from tools.toolkit import gen_short_uuid, get_md5, load_next_id
from database.base.database_helper import DataBase
import pandas as pd


class User:
    def __init__(self, acc_user=None, pwd_user_md5=None, db=None, table='users',
                 columns=['id', 'acc_user', 'pwd_user_md5', 'nam_user', 'vlu_email', 'vlu_phone', 'vlu_openid',
                          'nam_nick', 'cod_gender', 'vlu_lang', 'vlu_city', 'vlu_prov', 'vlu_country', 'url_avatar']):
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

    def create(self):
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
        if nam_user:
            self.nam_user = nam_user
        self.vlu_openid = openid

        sql_check = "select acc_user from %s where vlu_openid='%s' " % (self.table, self.vlu_openid)
        flag, result = self.db.read(sql_check)

        if flag and not result.empty:
            self.acc_user = result['acc_user'][0]
            flag_new = False
        else:
            self.acc_user = self.create()
            flag_new = True
        return self.acc_user, flag_new
    
    def save_userinfo(self, userinfo):
        dict_mapping = {
            'nickName':     'nam_nick',
            'gender':       'cod_gender',
            'language':     'vlu_lang',
            'city':         'vlu_city',
            'province':     'vlu_prov',
            'country':      'vlu_country',
            'avatarUrl':    'url_avatar'}
        data, columns = [], []
        for key, column in dict_mapping.items():
            columns.append(column)
            data.append(userinfo.get(key, ''))
        df_userinfo = pd.DataFrame(data=data, columns=columns)
        flag, result = self.db.write(df_userinfo, self.table)
        if not flag:
            print(result)
        return flag, result

    def db_init(self):
        pass


if __name__ == '__main__':
    u = User()
    print(u.create('韩大爷'))
