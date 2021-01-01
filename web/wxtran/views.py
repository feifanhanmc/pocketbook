#!/usr/bin/env python
# -*- coding: utf-8 -*-
import json
from flask import Blueprint, url_for, render_template, request, abort, flash, session, redirect
from web.wxtran.utils import utils_tran_add

mod = Blueprint('wxtran', __name__, url_prefix='/wxtran')


@mod.route('/tran_add', methods=['POST'])
def views_tran_add():
    req_data = request.get_data()
    print('req_data', req_data)
    result = {}
    if req_data:
        data = json.loads(req_data.decode('utf-8'))
        result = utils_tran_add(data)
    return json.dumps(result)

