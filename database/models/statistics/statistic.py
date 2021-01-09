#!/usr/bin/env python
# -*- coding: utf-8 -*-
from tools.toolkit import gen_short_uuid, get_md5, load_next_id
from database.base.database_helper import DataBase
import pandas as pd
import time


class Statistic:
    def __init__(self, acc_user, dte_month=None, db=None, table='statistics',
                 columns=['id', 'acc_user', 'dte_month', 'amt_income_month', 'amt_expend_month', 'amt_budget',
                          'amt_budget_surplus', 'amt_debt_total', 'amt_asset_total', 'amt_asset_net']):
        self.db = db
        self.table = table
        self.columns = columns
        self.acc_user = acc_user
        self.dte_month = dte_month

        if not self.db:
            self.db = DataBase()

    def init_statistics(self):
        if not self.dte_month:
            self.dte_month = time.strftime("%Y%m", time.localtime())
        df_statistics = pd.DataFrame(
            columns=['acc_user', 'dte_month'],
            data=[[self.acc_user, self.dte_month]])
        flag, result = self.db.write(df_statistics, self.table)
        return flag, result

    def show_statistics(self):
        dte_month_now = time.strftime("%Y%m", time.localtime())
        sql_show = """
            select 
                dte_month,
                case when dte_month='%s' then amt_income_month else 0 end as amt_income_month,
                case when dte_month='%s' then amt_expend_month else 0 end as amt_expend_month,
                case when dte_month='%s' then amt_budget_surplus else 0 end as amt_budget_surplus,
                amt_budget,
                amt_debt_total, 
                amt_asset_total, 
                amt_asset_net
            from %s 
            where acc_user='%s' 
            """ % (dte_month_now, dte_month_now, dte_month_now, self.table, self.acc_user)
        flag, statistics = self.db.read(sql_show)
        if flag:
            if dte_month_now == statistics['dte_month'].values[0]:
                sql_update = "update %s set dte_month='%s', amt_income_month=0, amt_expend_month=0, " \
                             "amt_budget_surplus=amt_budget where acc_user='%s'" % \
                             (self.table, dte_month_now, self.acc_user)
                self.db.execute(sql_update)
                return statistics
        return flag

    def update_statistics_transaction(self, type_amount, amount):
        """
        :param type_amount: ['income', 'expend', 'budget', 'asset', 'debt']
        :param amount: positive float
        :return: 适用于数据库事务的sql语句
        """
        if type_amount == 'income':
            sql_set = """ 
                amt_income_month = amt_income_month + %s,
                amt_asset_total = amt_asset_total + %s,
                amt_asset_net = amt_asset_net + %s
                """ % tuple([amount]*3)
        elif type_amount == 'expend':
            sql_set = """ 
                amt_expend_month = amt_expend_month + %s,
                amt_budget_surplus = amt_budget - amt_expend_month - %s,
                amt_asset_total = amt_asset_total - %s,
                amt_asset_net = amt_asset_net - %s
                """ % tuple([amount]*4)
        elif type_amount == 'budget':
            sql_set = """ 
                amt_budget = %s,
                amt_budget_surplus = %s - amt_expend_month
                """ % tuple([amount]*2)
        elif type_amount == 'asset':
            sql_set = """ 
                amt_asset_total = amt_asset_total + %s,
                amt_asset_net = amt_asset_net + %s
                """ % tuple([amount] * 2)
        elif type_amount == 'debt':
            sql_set = """ 
                    amt_asset_total = amt_asset_total - %s,
                    amt_debt_total = amt_debt_total + %s
                    """ % tuple([amount] * 2)
        else:
            pass
        sql_update = "update % set %s where acc_user ='%s'" % (self.table, sql_set, self.acc_user)
        return sql_update


if __name__ == '__main__':
    pass
