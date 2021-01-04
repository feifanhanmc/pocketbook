#!/usr/bin/env python
# -*- coding: utf-8 -*-
import json
from flask import Blueprint, url_for, render_template, request, abort, flash, session, redirect
from web.wxassets.utils import utils_show_assets

mod = Blueprint('wxassets', __name__, url_prefix='/wxassets')


@mod.route('/show_assets', methods=['POST'])
def views_show_assets():
    req_data = request.get_data()
    print('req_data', req_data)
    result = {'data': {}, 'code': 500}
    if req_data:
        data = json.loads(req_data.decode('utf-8'))
        result['data']= utils_login_init(data)
        result['code'] = 200
    print(result)
    return json.dumps(result)

