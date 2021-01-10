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
