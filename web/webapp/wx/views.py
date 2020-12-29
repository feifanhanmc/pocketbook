#-*- coding:utf-8 -*-
from flask import Blueprint, url_for, render_template, request,\
                  abort, flash, session, redirect
import json
import requests
from utils import   init as utils_init,\
                    signin as utils_signin,\
                    signup as utils_signup,\
                    check_friends_sign as utils_check_friends_sign

mod = Blueprint('wx', __name__, url_prefix='/wx')


@mod.route('/init')
def index():

    return render_template('index.html')


@mod.route('/signin')
def signin():
    wx_account = request.args.get('account', '')
    wx_password_md5 = request.args.get('password', '')
    if wx_account and wx_password_md5:
        res = utils_signin(wx_account, wx_password_md5)
        if res:
            return json.dumps(res)
    return json.dumps({})

@mod.route('/siginup')
def signup():
    wx_account = request.args.get('account', '')
    wx_password_md5 = request.args.get('password', '')
    if wx_account and wx_password_md5:
        res = utils_signup(wx_account, wx_password_md5)
        if res:
            return json.dumps(res)
    return json.dumps({})

@mod.route('/check_friends_sign')
def check_friends_sign():
    wx_account = request.args.get('account', '')
    wx_password_md5 = request.args.get('password', '')
    if wx_account and wx_password_md5:
        res = utils_check_friends_sign(wx_account, wx_password_md5)
        if res:
            return json.dumps(res)
    return json.dumps({})
