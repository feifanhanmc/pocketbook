# -*- coding: utf-8 -*-
import os
import sys
import json
import MySQLdb
sys.path.append(os.path.dirname(__file__))

print(os.path.dirname(__file__))
print(sys.path)

config_file = 'database.json'


class DataBase:
    def __init__(self):
        self.config = {}
        self.conn = None

    def load_config(self):
        print(os.getcwd())
        with open(config_file, 'r') as fp:
            self.config = json.load(fp)

    def connect(self):
        if not self.config:
            self.load_config()
        self.conn = MySQLdb.connect(
            host=self.config['host'],
            port=self.config['port'],
            user=self.config['user'],
            passwd=self.config['password'],
            db=self.config['db'],
            charset=self.config['charset'])

    def execute(self, sql):
        if not self.conn:
            self.connect()
        cursor = self.conn.cursor()
        cursor.execute(sql)
        result = cursor.fetchall()
        self.conn.commit()
        self.close()
        return [list(r) for r in result]

    def close(self):
        self.conn.close()

    def db2sql(self):
        pass

    def db2df(self):
        pass


if __name__ == '__main__':
    db = DataBase()
    print(db.execute('show tables'))

