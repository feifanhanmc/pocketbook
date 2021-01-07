#!/usr/bin/env python
# -*- coding: utf-8 -*-
import json
from flask import Blueprint, url_for, render_template, request, abort, flash, session, redirect
from web.wxtranstypes.utils import utils_show_transtypes

mod = Blueprint('wxtranstypes', __name__, url_prefix='/wxtranstypes')


@mod.route('/show_transtypes', methods=['POST'])
def views_show_transtypes():
    req_data = request.get_data()
    result = {'data': {}, 'code': 500}
    if req_data:
        data = json.loads(req_data.decode('utf-8'))
        result['data'] = utils_show_transtypes(data)
        result['code'] = 200
    return json.dumps(result)


@mod.route('/add_transtypes', methods=['POST'])
def views_add_transtypes():
    pass


@mod.route('/update_transtypes', methods=['POST'])
def views_update_transtypes():
    pass


@mod.route('/delete_transtypes', methods=['POST'])
def views_delete_transtypes():
    pass
