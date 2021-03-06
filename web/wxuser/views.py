#!/usr/bin/env python
# -*- coding: utf-8 -*-
import json
from flask import Blueprint, url_for, render_template, request, abort, flash, session, redirect
from web.wxuser.utils import utils_home, utils_login_init, utils_save_userinfo, utils_show_userinfo

mod = Blueprint('wxuser', __name__, url_prefix='/wxuser')


@mod.route('/')
def views_home():
    result = utils_home()
    return json.dumps(result)


@mod.route('/login_init', methods=['POST'])
def views_login_init():
    req_data = request.get_data()
    result = {'data': {}, 'code': 500}
    if req_data:
        data = json.loads(req_data.decode('utf-8'))
        result['data'] = utils_login_init(data)
        result['code'] = 200
    return json.dumps(result)


@mod.route('/show_userinfo', methods=['POST'])
def views_show_userinfo():
    req_data = request.get_data()
    result = {'data': {}, 'code': 500}
    if req_data:
        data = json.loads(req_data.decode('utf-8'))
        result['data'] = utils_show_userinfo(data)
        result['code'] = 200
    return json.dumps(result)


@mod.route('/save_userinfo', methods=['POST'])
def views_save_userinfo():
    req_data = request.get_data()
    result = {'data': {}, 'code': 500}
    if req_data:
        data = json.loads(req_data.decode('utf-8'))
        result['data'] = utils_save_userinfo(data)
        result['code'] = 200
    return json.dumps(result)