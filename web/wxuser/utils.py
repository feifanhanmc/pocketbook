#!/usr/bin/env python
# -*- coding: utf-8 -*-
import json
import requests
from web.wxuser.WXBizDataCrypt import WXBizDataCrypt
from data.data_helper import load_config
from database.models.users.user import User, dict_mapping
from database.models.transtypes.transtype import Transtype
from database.models.statistics.statistic import Statistic
from tools.toolkit import gen_short_uuid
from database.base.database_helper import DataBase


file_wxminiprj_token = 'wxminiprj_token.json'
wx_login_api = 'https://api.weixin.qq.com/sns/jscode2session'


def utils_home():
    return True


def utils_show_userinfo(wx_data):
    acc_user = wx_data['token']
    df_userinfo = User(acc_user).show_userinfo()

    userInfo = {}
    if not df_userinfo.empty:
        for key_web, key_db in dict_mapping.items():
            userInfo[key_web] = df_userinfo.iloc[0][key_db]
    return {'userInfo': userInfo}


'''
# 现在好像直接给了用户信息，不需要再进行解密获取
session_key = resData['session_key']  # 得到用户关于当前小程序的会话密钥session_key
pc = WXBizDataCrypt(appID, session_key)  # 对用户信息进行解密
userinfo = pc.decrypt(encrypted_data, iv)  # 获得用户信息
'''
def utils_save_userinfo(wx_data):
    acc_user = wx_data['token']
    userinfo = json.loads(wx_data.get('rawData', {}))

    u = User(acc_user)
    df_userinfo = u.show_userinfo()
    if not df_userinfo.empty:
        vlu_openid = df_userinfo.iloc[0]['vlu_openid']
        userinfo['vlu_openid'] = vlu_openid
    
        sql_delete_userinfo, df_userinfo, table, index, if_exists = User(acc_user).save_userinfo(userinfo, is_transaction=True)
        sql_list = [sql_delete_userinfo]
        dfinfo_list = [[df_userinfo, table, index, if_exists]]
        return {'result': DataBase().transaction(dfinfo_list, sql_list)}
    return {'result': False}


def utils_login_init(wx_data):
    resp = {}
    wxminiprj_token = load_config(file_wxminiprj_token)
    appID = wxminiprj_token['appID']
    appSecret = wxminiprj_token['appSecret']

    # 准备获取openid的请求数据，code为前端POST过来的微信临时登录凭证
    code = wx_data['code'] 
    req_params = {
        'appid': appID,
        'secret': appSecret,
        'js_code': code,
        'grant_type': 'authorization_code'
    }

    # 发起请求获取微信用户唯一标识openid
    response_data = requests.get(wx_login_api, params=req_params) 
    resData = response_data.json()
    openid = resData['openid']

    u = User()
    acc_user, flag_new = u.user_check(openid)
    if acc_user:
        # 对于新创建的用户，需要创建初始资产统计表
        if flag_new:
            s = Statistic(acc_user)
            statistic_flag, statistic_result = s.init_statistics()
            if statistic_flag:
                resp['init_statistics'] = True
            else:
                resp['init_statistics'] = False

    resp['token'] = acc_user
    return resp


