# -*- coding:utf-8 -*-
import json
from flask import Blueprint, url_for, render_template, request, abort, flash, session, redirect
from web.wxuser.utils import utils_home, utils_login

mod = Blueprint('wxuser', __name__, url_prefix='/wxuser')


@mod.route('/')
def views_home():
    result = utils_home()
    return json.dumps(result)


@mod.route('/login', methods=['GET', 'POST'])
def views_login():
    req_data = request.get_data()
    if req_data:
        data = json.loads(req_data.decode('utf-8'))
        result = utils_login(data)
        if result:
            return result
            # return json.dumps(result)
    return json.dumps(False)

