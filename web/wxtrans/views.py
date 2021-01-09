#!/usr/bin/env python
# -*- coding: utf-8 -*-
import json
from flask import Blueprint, url_for, render_template, request, abort, flash, session, redirect
from web.wxtrans.utils import utils_show_trans, utils_add_trans, utils_update_trans, utils_delete_trans

mod = Blueprint('wxtrans', __name__, url_prefix='/wxtrans')


@mod.route('/show_trans', methods=['POST'])
def views_show_trans():
    req_data = request.get_data()
    result = {'data': {}, 'code': 500}
    if req_data:
        data = json.loads(req_data.decode('utf-8'))
        result['data'] = utils_show_trans(data)
        result['code'] = 200
    return json.dumps(result)


@mod.route('/add_trans', methods=['POST'])
def views_add_trans():
    req_data = request.get_data()
    result = {'data': {}, 'code': 500}
    if req_data:
        data = json.loads(req_data.decode('utf-8'))
        result['data'] = utils_add_trans(data)
        result['code'] = 200
    return json.dumps(result)


@mod.route('/update_trans', methods=['POST'])
def views_update_trans():
    pass


@mod.route('/delete_trans', methods=['POST'])
def views_delete_trans():
    pass