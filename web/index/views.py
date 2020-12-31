#!/usr/bin/env python
# -*- coding: utf-8 -*-
from flask import Blueprint, url_for, render_template, request, abort, flash, session, redirect
import json
import requests

mod = Blueprint('index', __name__, url_prefix='/')


@mod.route('/')
def index():
    return render_template('index.html')


@mod.route('/huaji')
def huaji():
    return render_template('huaji.html')

