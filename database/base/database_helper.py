#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
from sqlalchemy import create_engine
import pandas as pd
from data.data_helper import load_config

file_config = 'dbconfig.json'


class DataBase:
    def __init__(self):
        self.base_path = os.path.dirname(__file__)
        self.config = {}
        self.engine = None
        self.flag = False   # 执行结果成功与否的标志
        self.res = None     # 执行结果

        if not self.config:
            self.config = load_config(file_config)

        if not self.engine:
            self.engine = create_engine('mysql+pymysql://%s:%s@%s:%s/%s' %
                                        (self.config["user"], self.config["password"], self.config["host"],
                                         self.config["port"], self.config["db"]))

    def gen_transaction_conn(self):
        """
        desc: 按照数据库事务规范执行，任何一条语句失败则rollback
        usage:
            tran = conn.begin()
            try:
                conn.execute(sql_1)
                conn.execute(sql_2)
                tran.commit()
            except:
                tran.rollback()
            或
            tran = conn.begin()
            try:
                df1.to_sql()
                df2.to_sql()
                tran.commit()
            except:
                tran.rollback()
        :return:
        """
        return self.engine.connect()

    def execute(self, sql):
        try:
            with self.engine.connect() as conn:
                conn.execute(sql)
            flag = True
            result = {}
        except Exception as e:
            result = str(e)
            flag = False
        return flag, result

    def read(self, sql):
        try:
            df = pd.read_sql(sql, self.engine)
            result = df
            flag = True
        except Exception as e:
            result = str(e)
            flag = False
        return flag, result

    def write(self, df, table, index=False, if_exists='append'):
        try:
            df.to_sql(table, con=self.engine, index=index, if_exists=if_exists)
            result = {}
            flag = True
        except Exception as e:
            result = str(e)
            flag = False
        return flag, result


if __name__ == '__main__':
    db = DataBase()
    # db.execute('show tables')
    # print(db.read('show tables')[1])
    # print(db.read('desc assets')[1]['Default'].tolist())
    conn = db.connection()
    trans = conn.begin()
    try:
        pd.DataFrame(data=[['c', 'c']], columns=['acc_user', 'pwd_user_md5']).to_sql('users', con=conn, index=False, if_exists='append')
        pd.DataFrame(data=[['dddddddddddddd', 'd']], columns=['acc_user', 'pwd_user_md5']).to_sql('users', con=conn, index=False, if_exists='append')
        trans.commit()
    except Exception as e:
        print(str(e))
        trans.rollback()


