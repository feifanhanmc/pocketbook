# -*- coding:utf-8 -*-
from flask import Blueprint
import json

mod = Blueprint('login', __name__, url_prefix='/login')


@mod.route('/test/')
def views_test():
    return json.dumps(True)
