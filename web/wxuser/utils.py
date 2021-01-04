#!/usr/bin/env python
# -*- coding: utf-8 -*-
import json
import requests
from web.wxuser.WXBizDataCrypt import WXBizDataCrypt
from data.data_helper import load_config
from database.models.users.user import User

file_wxminiprj_token = 'wxminiprj_token.json'
wx_login_api = 'https://api.weixin.qq.com/sns/jscode2session'


def utils_home():
    return True


def utils_login_init(wx_data):
    wxminiprj_token = load_config(file_wxminiprj_token)
    appID = wxminiprj_token['appID']
    appSecret = wxminiprj_token['appSecret']

    acc_user = wx_data.get('acc_user', '')
    userinfo = json.loads(wx_data.get('rawData', {}))
    nam_user = userinfo.get('nickName', '')
    
    # 准备获取openid的请求数据
    code = wx_data['code']  # 前端POST过来的微信临时登录凭证code
    encrypted_data = wx_data['encryptedData']
    iv = wx_data['iv']
    req_params = {
        'appid': appID,
        'secret': appSecret,
        'js_code': code,
        'grant_type': 'authorization_code'
    }

    # 发起请求获取微信用户唯一标识openid
    response_data = requests.get(wx_login_api, params=req_params)  # 向API发起GET请求
    resData = response_data.json()
    openid = resData['openid']  # 得到用户关于当前小程序的OpenID

    '''
    # 现在好像直接给了用户信息，不需要再进行解密获取
    session_key = resData['session_key']  # 得到用户关于当前小程序的会话密钥session_key
    pc = WXBizDataCrypt(appID, session_key)  # 对用户信息进行解密
    userinfo = pc.decrypt(encrypted_data, iv)  # 获得用户信息
    '''
    
    u = User()
    acc_user = u.user_check(openid, nam_user=nam_user)
    u.save_userinfo(userinfo)
    return {"token":acc_user}


