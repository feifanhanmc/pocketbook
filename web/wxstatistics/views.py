#!/usr/bin/env python
# -*- coding: utf-8 -*-
import json
from flask import Blueprint, url_for, render_template, request, abort, flash, session, redirect
from web.wxstatistics.utils import utils_show_statistics

mod = Blueprint('wxstatistics', __name__, url_prefix='/wxstatistics')


@mod.route('/show_statistics', methods=['POST'])
def views_show_statistics():
    req_data = request.get_data()
    result = {'data': {}, 'code': 500}
    if req_data:
        data = json.loads(req_data.decode('utf-8'))
        result['data'] = utils_show_statistics(data)
        result['code'] = 200
    return json.dumps(result)

