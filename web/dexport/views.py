#!/usr/bin/env python
# -*- coding: utf-8 -*-
from flask import Blueprint, send_from_directory, request
from web.dexport.utils import utils_export
import json
import os


mod = Blueprint('dexport', __name__, url_prefix='/dexport')


@mod.route('/', methods=['GET'])
def views_export():
    filename = request.args.get("filename", "")
    if filename:
        dirname = utils_export()
        return send_from_directory(dirname, filename, as_attachment=True)

