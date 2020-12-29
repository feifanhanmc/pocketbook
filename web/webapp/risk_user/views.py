#-*- coding:utf-8 -*-
from flask import Blueprint, url_for, render_template, request,\
                  abort, flash, session, redirect
import json
from utils import utils_create_table, utils_show_urls, utils_show_risk_user


mod = Blueprint('risk_user', __name__, url_prefix='/risk_user')


@mod.route('/create_table/')
def create_table():
    sql = request.args.get('sql','')
    if sql:
        res = utils_create_table(sql)
        if res:
            return json.dumps(res)
    return json.dumps(False)

@mod.route('/show_urls/')
def show_urls():
    res = utils_show_urls()
    if res:
        return json.dumps(res)
    return json.dumps(False)

@mod.route('/show_risk_user/')
def show_risk_user():
    url = request.args.get('url','')
    if url:
        res = utils_show_risk_user(url)
        if res:
            return json.dumps(res)
    return json.dumps(False)

@mod.route('/upload_file/')
def upload_file():
    res = utils_upload_file()
    if res:
        return json.dumps(res)
    return json.dumps(False)
