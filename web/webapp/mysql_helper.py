#-*- coding: utf-8 -*-
import MySQLdb
from web.webapp.config import mysql_config
# from config import mysql_config

mysql_config_defalut = {
    'host': 'localhost',
    'port': 3306,
    'username': 'root',
    'password': 'root',
    'dbname': 'mysql'
}

class mysql_db():
    def __init__(self, mysql_config=mysql_config_defalut):
        self.conn = MySQLdb.connect(
                host=mysql_config['host'],
                port=mysql_config['port'],
                user=mysql_config['username'],
                passwd=mysql_config['password'],
                db=mysql_config['dbname'],
                charset='utf8')
        self.cursor = self.conn.cursor()

    def close(self):
        self.conn.close()

    def create_table(self, sql):
        self.cursor.execute(sql)
        self.close()

    def select(self, sql, auto_close=True):
        self.cursor.execute(sql)
        res = self.cursor.fetchall()
        if auto_close:
            self.close()
        return res

    def insert(self, table_name, data_headers, data, auto_close=True, debug_mode=True):
        '''
        :param data_headers(list of data_name(str)) 、 data(list of list)
        for example:
            data_headers = ['username', 'pwd']
            data = [['hmc', '123'],
                    ['admin', 'admin'],
                    ['root', 'root']] 
        '''
        flag = False
        debug_info = ''

        columc_num = len(data_headers)
        
        #拼接sqli语句
        sqli = 'INSERT INTO ' + table_name + '('
        datatype = '('
        for i in range(columc_num):
            if not i:
                sqli = sqli + data_headers[i]
                datatype += '%s'
            else:
                sqli = sqli + ', '  + data_headers[i]
                datatype += ', %s' 
        datatype += ')'
        sqli = sqli + ')' + ' VALUES ' + datatype
        
        #存储数据
        for d in data:
            t = []
            for i in range(columc_num):
                t.append(d[i])
            try:
                self.cursor.execute(sqli, tuple(t))
                self.conn.commit()
                flag = True
                debug_info += '存储成功，共存储 %s 条数据' % str(len(data))
            except Exception as e :
                debug_info += '存储失败，错误原因 : %s' % e
                self.conn.rollback()
                break 
        # 
        if debug_mode:
            print(debug_info)
        if auto_close:
            self.close()
        return flag
