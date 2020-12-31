#!/usr/bin/env python
# -*- coding: utf-8 -*-
from flask import Blueprint
import json

mod = Blueprint('import', __name__, url_prefix='/import')


@mod.route('/test/')
def views_test():
    return json.dumps(True)
