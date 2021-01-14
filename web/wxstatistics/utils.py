#!/usr/bin/env python
# -*- coding: utf-8 -*-
from database.models.statistics.statistic import Statistic


def utils_show_statistics(wx_data):
    acc_user = wx_data['token']
    df_statistics = Statistic(acc_user).show_statistics()
    data = {}
    if not df_statistics.empty:
        data = df_statistics.iloc[0].to_dict()
    return {'statistics': data}

def utils_set_budget(wx_data):
    acc_user = wx_data['token']
    amt_budget = float(wx_data['amt_budget'])
    result = Statistic(acc_user).update_statistics(tye_amount='budget', amount=amt_budget)
    return {'result': result}
