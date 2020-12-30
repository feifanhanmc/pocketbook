# -*- coding:utf-8 -*-
from flask import Blueprint
import json

mod = Blueprint('export', __name__, url_prefix='/export')


@mod.route('/test/')
def views_test():
    return json.dumps(True)
