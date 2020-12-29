# -*- coding: utf-8 -*-
import os
import sys
import json
import pymysql
from sqlalchemy import create_engine
import pandas as pd

config_file = 'dbconfig.json'


class DataBase:
    def __init__(self):
        self.base_path = os.path.dirname(__file__)
        self.config = {}
        self.engine = None
        self.flag = False   # 执行结果成功与否的标志
        self.res = None     # 执行结果

        if not self.config:
            with open(os.path.join(self.base_path, config_file), 'r') as fp:
                self.config = json.load(fp)

        if not self.engine:
            self.engine = create_engine(
                f'mysql+pymysql://{self.config["user"]}:{self.config["password"]}@{self.config["host"]}:'
                f'{self.config["port"]}/{self.config["db"]}')

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
    print(db.read('show tables')[1])

