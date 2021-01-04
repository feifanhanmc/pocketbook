#!/usr/bin/env python
# -*- coding: utf-8 -*-
import json
import requests
from data.data_helper import load_config
from database.models.assets.asset import Asset

file_wxminiprj_token = 'wxminiprj_token.json'


def utils_show_assets(wx_data):
    acc_user = wx_data['token']
    df_assets = Asset(acc_user).show_assets()
    data = []
    return {'assets': data}



