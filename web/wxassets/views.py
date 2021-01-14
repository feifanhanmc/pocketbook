#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
import json
from flask import Blueprint, url_for, render_template, request, abort, flash, session, redirect
from web.wxassets.utils import utils_show_assets, utils_add_assets, utils_modify_assets, utils_delete_assets

mod = Blueprint('wxassets', __name__, url_prefix='/wxassets')


@mod.route('/show_assets', methods=['POST'])
def views_show_assets():
    req_data = request.get_data()
    result = {'data': {}, 'code': 500}
    if req_data:
        data = json.loads(req_data.decode('utf-8'))
        result['data'] = utils_show_assets(data)
        result['code'] = 200
    return json.dumps(result)


@mod.route('/show_default_assets', methods=['POST'])
def views_show_default_assets():
    req_data = request.get_data()
    result = {'data': {}, 'code': 500}
    if req_data:
        data = json.loads(req_data.decode('utf-8'))
        result['data']= utils_show_assets(data, flag_default=True)
        result['code'] = 200
    return json.dumps(result)


@mod.route('/add_assets', methods=['POST'])
def view_add_assets():
    req_data = request.get_data()
    result = {'data': {}, 'code': 500}
    if req_data:
        data = json.loads(req_data.decode('utf-8'))
        result['data'] = utils_add_assets(data)
        result['code'] = 200
    return json.dumps(result)


@mod.route('/modify_assets', methods=['POST'])
def view_modify_assets():
    req_data = request.get_data()
    result = {'data': {}, 'code': 500}
    if req_data:
        data = json.loads(req_data.decode('utf-8'))
        result['data'] = utils_modify_assets(data)
        result['code'] = 200
    return json.dumps(result)


@mod.route('/delete_assets', methods=['POST'])
def view_delete_assets():
    req_data = request.get_data()
    result = {'data': {}, 'code': 500}
    if req_data:
        data = json.loads(req_data.decode('utf-8'))
        result['data'] = utils_delete_assets(data)
        result['code'] = 200
    return json.dumps(result)

