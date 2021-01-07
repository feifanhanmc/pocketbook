#!/usr/bin/env python
# -*- coding: utf-8 -*-
from database.models.transtypes.transtype import Transtype


def utils_show_transtypes(wx_data):
    acc_user = wx_data['token']
    acc_user_show = wx_data.get('acc_user', None)
    df_transtypes = Transtype(acc_user).show_transtypes(acc_user_show)
    data = {}
    for tye_flow, key in {'支出': 'expend', '收入': 'income', '其他': 'transfer'}.items():
        df_temp = df_transtypes[df_transtypes['tye_flow'] == tye_flow]
        da = []
        for i in range(len(df_temp)):
            da.append(df_temp.iloc[i].to_dict())
        data[key] = da
    return {'transtypes': data}


def utils_add_transtypes():
    pass


def utils_update_transtypes():
    pass


def utils_delete_transtypes():
    pass



