#!/usr/bin/env python
# -*- coding: utf-8 -*-
from database.models.transtypes.transtype import Transtype


def utils_show_transtypes(wx_data):
    acc_user = wx_data['token']
    df_transtypes = Transtype(acc_user).show_transtypes()
    data = {}
    for tye_flow in ('expend', 'income', 'transfer'):
        df_temp = df_transtypes[df_transtypes['tye_flow'] == tye_flow]
        da = []
        for i in range(len(df_temp)):
            da.append(df_temp.iloc[i].to_dict())
        data[tye_flow] = da
    return {'transtypes': data}


def utils_add_transtypes():
    pass


def utils_update_transtypes():
    pass


def utils_delete_transtypes():
    pass



