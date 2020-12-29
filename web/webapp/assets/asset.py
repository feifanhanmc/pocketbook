# -*- coding: utf-8 -*-
from tools.toolkit import gen_short_uuid, get_md5, load_next_id
from database.conn.database import DataBase


class Asset:
    def __init__(self, acc_user):
        self.acc_user = acc_user
        self.acc_asset_list = []
        self.nam_asset_list = []
        self.amt_asset_list = []

    def create_from_trans(self, nam_user=None, table='users'):
        self.acc_user = gen_short_uuid()
        if not self.nam_user:
            self.nam_user = gen_short_uuid()
        self.pwd_user_md5 = get_md5(self.acc_user)

        db = DataBase()
        next_id = load_next_id(table)
        db.execute("insert into %s values ('%s', '%s', '%s', '%s', '%s', '%s')" %
                   (table, next_id, self.acc_user, self.pwd_user_md5, self.nam_user, self.vlu_email, self.vlu_phone))

        return self.acc_user


if __name__ == '__main__':
    u = User()
    u.create('韩大爷')
