# -*- coding:utf-8 -*-
from flask import Blueprint, url_for, render_template, request,\
                  abort, flash, session, redirect
import json
import requests

mod = Blueprint('index', __name__, url_prefix='/')


@mod.route('/')
def index():
    return render_template('index.html')


@mod.route('/huaji')
def huaji():
    return render_template('huaji.html')


@mod.route('/decode_danmu')
def decode_danmu():
    danmu_url = 'http://cmts.iqiyi.com/bullet/77/00/874217700_300_3.z?business=danmu&is_iqiyi=true&is_video_page=true&tvid=874217700&albumid=205025001&categoryid=2'
    r = requests.get(danmu_url)
    return r.text