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

    # 为避免使用contab等定时工具，需要在执行statistics相关的操作之前，检查是否是新月，来决定是否清空月统计数据
    def reset_statistics(self):
        dte_month_now = time.strftime("%Y%m", time.localtime())
        sql_update = """
            update %s 
            set  
                dte_month = case when dte_month='%s' then dte_month else '%s' end,
                amt_income_month = case when dte_month='%s' then amt_income_month else 0 end,
                amt_expend_month = case when dte_month='%s' then amt_expend_month else 0 end
            where acc_user='%s' 
            """ % (self.table, dte_month_now, dte_month_now, dte_month_now, dte_month_now, self.acc_user)
        flag, result = self.db.execute(sql_update)
        if not flag:
            print(result)
        return flag

    def show_statistics(self):
        self.reset_statistics()

        sql_show = " select * from %s where acc_user='%s' " % (self.table, self.acc_user)
        flag, result = self.db.read(sql_show)
        if not flag:
            print(result)
            return pd.DataFrame()
        else:
            return result

    def update_statistics(self, tye_amount, amount, cod_trans_type='', tye_asset='', tye_asset_related='', tye_update='add', is_transaction=False):
        """
        :param tye_update: ['add', 'delete_trans', 'delete_asset']
        :param tye_amount: ['income', 'expend', 'transfer', 'budget', 'asset', 'debt']
        :param amount: 根据type_amount，取对应的值或者相反数
        :param cod_trans_type: 交易类型代码
        :param tye_asset: 资产账户类型
        :param tye_asset_related: 相关联的资产账户类型
        :param is_transaction: 为False则直接执行；为True则返回sql语句，待后续按照数据库事务规范执行
        :return: 返回执行结果或返回适用于数据库事务的sql
        """
        self.reset_statistics()

        sql_set = " amt_asset_total = amt_asset_total "
        if tye_update == 'add':
            if tye_amount == 'income':     # 流入
                if tye_asset == 'asset':
                    if cod_trans_type in ('yqkDZNq7', 'xSTyQpeH'):  # 退款、报销，不计入收入，但支出、预算剩余应减少
                        sql_set = " amt_asset_total = amt_asset_total + %s, amt_asset_net = amt_asset_net + %s, amt_expend_month = amt_expend_month + %s, amt_budget_surplus = amt_budget + amt_expend_month " % tuple([amount]*3)
                    else:
                        sql_set = " amt_income_month = amt_income_month + %s, amt_asset_total = amt_asset_total + %s, amt_asset_net = amt_asset_net + %s " % tuple([amount]*3)
                elif tye_asset == 'debt':
                    if cod_trans_type in ('yqkDZNq7', 'xSTyQpeH'):  # 退款、报销，不计入收入，但支出、预算剩余应减少
                        sql_set = " amt_debt_total = amt_debt_total + %s, amt_asset_net = amt_asset_net + %s, amt_expend_month = amt_expend_month + %s, amt_budget_surplus = amt_budget + amt_expend_month " % tuple([amount]*3)
                    else:
                        sql_set = " amt_income_month = amt_income_month + %s, amt_debt_total = amt_debt_total + %s, amt_asset_net = amt_asset_net + %s " % tuple([amount]*3)
            elif tye_amount == 'expend':   # 流出
                if tye_asset == 'asset':
                    sql_set = " amt_expend_month = amt_expend_month + %s, amt_budget_surplus = amt_budget + amt_expend_month, amt_asset_total = amt_asset_total + %s, amt_asset_net = amt_asset_net + %s " % tuple([amount]*3)
                elif tye_asset == 'debt':
                    sql_set = " amt_expend_month = amt_expend_month + %s, amt_budget_surplus = amt_budget + amt_expend_month, amt_debt_total = amt_debt_total + %s, amt_asset_net = amt_asset_net + %s " % tuple([amount]*3)
                else:
                    pass
            elif tye_amount == 'transfer': # 转账
                if tye_asset == 'asset' and tye_asset_related == 'debt':    # 资产负债都减少，但数值一减一增
                    sql_set = " amt_asset_total = amt_asset_total - %s, amt_debt_total = amt_debt_total + %s " % tuple([amount]*2)
                elif tye_asset == 'debt' and tye_asset_related == 'asset':  # 资产负债都增加，但数值一增一减
                    sql_set = " amt_asset_total = amt_asset_total + %s, amt_debt_total = amt_debt_total - %s " % tuple([amount]*2)
                else:   # 不需要任何变动
                    pass
            elif tye_amount == 'budget':
                sql_set = " amt_budget = %s, amt_budget_surplus = %s + amt_expend_month " % tuple([amount]*2)
            elif tye_amount == 'asset':
                sql_set = " amt_asset_total = amt_asset_total + %s, amt_asset_net = amt_asset_net + %s " % tuple([amount] * 2)
            elif tye_amount == 'debt':
                sql_set = " amt_debt_total = amt_debt_total + %s, amt_asset_net = amt_asset_net + %s " % tuple([amount] * 2)
            else:
                pass
        elif tye_update == 'delete_trans':  # 删除交易记录会引起资产账户变动
            if tye_amount == 'income':     # 原交易记录为流入
                if cod_trans_type in ('yqkDZNq7', 'xSTyQpeH'):  # 退款、报销
                    sql_set = " amt_asset_total = amt_asset_total - %s, amt_asset_net = amt_asset_net - %s, amt_expend_month = amt_expend_month - %s, amt_budget_surplus = amt_budget + amt_expend_month " % tuple([amount]*3)
                else:
                    sql_set = " amt_income_month = amt_income_month - %s, amt_asset_total = amt_asset_total - %s, amt_asset_net = amt_asset_net - %s " % tuple([amount]*3)
            elif tye_amount == 'expend':   # 原交易记录为流出
                if tye_asset == 'asset':
                    sql_set = " amt_expend_month = amt_expend_month - %s, amt_budget_surplus = amt_budget + amt_expend_month, amt_asset_total = amt_asset_total - %s, amt_asset_net = amt_asset_net - %s " % tuple([amount]*3)
                elif tye_asset == 'debt':
                    sql_set = " amt_expend_month = amt_expend_month - %s, amt_budget_surplus = amt_budget + amt_expend_month, amt_debt_total = amt_debt_total - %s, amt_asset_net = amt_asset_net - %s " % tuple([amount]*3)
                else:
                    pass
            elif tye_amount == 'transfer': # 原交易记录为转账
                if tye_asset == 'asset' and tye_asset_related == 'debt':    
                    sql_set = " amt_asset_total = amt_asset_total + %s, amt_debt_total = amt_debt_total - %s " % tuple([amount]*2)
                elif tye_asset == 'debt' and tye_asset_related == 'asset': 
                    sql_set = " amt_asset_total = amt_asset_total - %s, amt_debt_total = amt_debt_total + %s " % tuple([amount]*2)
                else:   # 不需要任何变动
                    pass  
        elif tye_update == 'delete_asset':
            if tye_asset == 'asset':    
                sql_set = " amt_asset_total = amt_asset_total - %s, amt_asset_net = amt_asset_net - %s " % tuple([amount]*2)
            elif tye_asset == 'debt':
                sql_set = " amt_debt_total = amt_debt_total - %s, amt_asset_net = amt_asset_net - %s " % tuple([amount] * 2)
            else:
                pass
        else:
            pass

        sql_update = "update %s set %s where acc_user ='%s'" % (self.table, sql_set, self.acc_user)
        print('sql_update_statistics', sql_update)

        if not is_transaction:
            flag, result = self.db.execute(sql_update)
            if not flag:
                print(result)
            return flag
        else:
            return sql_update


if __name__ == '__main__':
    pass
