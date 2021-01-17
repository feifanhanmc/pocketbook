#!/usr/bin/env python
# -*- coding: utf-8 -*-
from tools.toolkit import gen_short_uuid, get_md5, load_next_id
from database.base.database_helper import DataBase
import pandas as pd


dict_mapping = {
    'nickName':     'nam_user',
    'gender':       'cod_gender',
    'language':     'vlu_lang',
    'city':         'vlu_city',
    'province':     'vlu_prov',
    'country':      'vlu_country',
    'avatarUrl':    'url_avatar'}


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

    def show_userinfo(self):
        sql_show = "select * from %s where acc_user='%s' " % (self.table, self.acc_user)
        flag, result = self.db.read(sql_show)
        if not flag:
            print(result)
            return pd.DataFrame()
        else:
            return result

    def save_userinfo(self, userinfo, is_transaction=False):
        if not self.acc_user:
            self.acc_user = gen_short_uuid()
        self.pwd_user_md5 = get_md5(self.acc_user)
        
        sql_delete = "delete from %s where acc_user='%s' " % (self.table, self.acc_user)

        columns = ['acc_user', 'pwd_user_md5', 'vlu_openid']
        data = [self.acc_user, self.pwd_user_md5, userinfo['vlu_openid']]
        for key, column in dict_mapping.items():
            columns.append(column)
            data.append(userinfo.get(key, ''))
        df_userinfo = pd.DataFrame(data=[data], columns=columns)

        if not is_transaction:
            flag, result = self.db.execute(sql_delete)
            if not flag:
                print(result)
                return False
            else:
                flag, result = self.db.write(df_userinfo, self.table)
                if not flag:
                    print(result)
                return False
            return True
        else:
            return sql_delete, df_userinfo, self.table, False, 'append'

    def create(self):
        if not self.acc_user:
            self.acc_user = gen_short_uuid()
        self.pwd_user_md5 = get_md5(self.acc_user)
        
        columns = ['acc_user', 'pwd_user_md5', 'vlu_openid']
        data = [self.acc_user, self.pwd_user_md5, self.vlu_openid]
        df_user = pd.DataFrame(data=[data], columns=columns)
        flag, result = self.db.write(df_user, self.table)

        if flag:
            return self.acc_user
        else:
            print(result)
            return False

    def user_check(self, openid):
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


if __name__ == '__main__':
    u = User()
    print(u.create('韩大爷'))
