#!/usr/bin/env python
# -*- coding: utf-8 -*-
from tools.toolkit import gen_short_uuid, get_md5, load_next_id
from database.base.database_helper import DataBase
import pandas as pd


class User:
    def __init__(self, acc_user=None, pwd_user_md5=None, table='users',
                 columns=['id', 'acc_user', 'pwd_user_md5', 'nam_user', 'vlu_email', 'vlu_phone']):
        self.table = table
        self.columns = columns
        self.acc_user = acc_user
        self.pwd_user_md5 = pwd_user_md5
        self.nam_user = ''
        self.vlu_email = ''
        self.vlu_phone = ''

    def create(self, nam_user=None):
        self.acc_user = gen_short_uuid()
        if not self.nam_user:
            self.nam_user = gen_short_uuid()
        self.pwd_user_md5 = get_md5(self.acc_user)

        db = DataBase()
        next_id = load_next_id(self.table)
        df_user = pd.DataFrame(
            data=[[next_id, self.acc_user, self.pwd_user_md5, self.nam_user, self.vlu_email, self.vlu_phone]],
            columns=self.columns)
        flag, result = db.write(df_user, self.table)
        if flag:
            return self.acc_user
        return flag



if __name__ == '__main__':
    u = User()
    print(u.create('韩大爷'))
