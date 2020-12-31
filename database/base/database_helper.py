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

    def execute(self, sql):
        with self.engine.connect() as conn:
            conn.execute(sql)

    def read(self, sql):
        try:
            df = pd.read_sql(sql, self.engine)
            self.res = df
            self.flag = True
        except Exception as e:
            self.res = str(e)
            self.flag = False
        return self.flag, self.res

    def write(self, df, table, index=False, if_exists='append'):
        try:
            df.to_sql(table, con=self.engine, index=index, if_exists=if_exists)
            self.flag = True
        except Exception as e:
            self.res = str(e)
            self.flag = False
        return self.flag, self.res


if __name__ == '__main__':
    db = DataBase()
    # db.execute('show tables')
    # print(db.read('show tables')[1])
    print(db.read('desc assets')[1]['Default'].tolist())

