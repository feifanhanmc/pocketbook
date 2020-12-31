# -*- coding:utf-8 -*-
import json, requests
from web.wxuser.WXBizDataCrypt import WXBizDataCrypt
from flask import Blueprint, url_for, render_template, request, abort, flash, session, redirect
from data.data_helper import load_config

file_wxminiprj_token = 'wxminiprj_token.config'
wx_login_api = 'https://api.weixin.qq.com/sns/jscode2session'


def utils_home():
    return True


def utils_login(wx_data):
    wxminiprj_token = load_config(file_wxminiprj_token)
    appID = wxminiprj_token['appID']
    appSecret = wxminiprj_token['appSecret']

    code = wx_data['platCode']  # 前端POST过来的微信临时登录凭证code
    encrypted_data = wx_data['platUserInfoMap']['encryptedData']
    iv = wx_data['platUserInfoMap']['iv']
    req_params = {
        'appid': appID,
        'secret': appSecret,
        'js_code': code,
        'grant_type': 'authorization_code'
    }


    response_data = requests.get(wx_login_api, params=req_params)  # 向API发起GET请求
    resData = response_data.json()
    openid = resData['openid']  # 得到用户关于当前小程序的OpenID
    session_key = resData['session_key']  # 得到用户关于当前小程序的会话密钥session_key

    pc = WXBizDataCrypt(appID, session_key)  # 对用户信息进行解密
    userinfo = pc.decrypt(encrypted_data, iv)  # 获得用户信息
    print(userinfo)
    '''
    下面部分是通过判断数据库中用户是否存在来确定添加或返回自定义登录态（若用户不存在则添加；若用户存在，返回用户信息）
    
    --------略略略略略略略略略-------------
    
    这部分我就省略啦，数据库中对用户进行操作
    '''

    return json.dumps({"code": 200, "msg": "登录成功", "userinfo": userinfo}, indent=4, sort_keys=True, default=str,
                      ensure_ascii=False)

