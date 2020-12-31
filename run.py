#!/usr/bin/env python
# -*- coding: utf-8 -*-
from flask import Flask, Blueprint, url_for, render_template, request, abort, flash, session, redirect
from index.views import mod as indexModule
from web.wxuser.views import mod as wxUserModule
from dataexport.views import mod as exportModule
from dataimport.views import mod as importModule


def create_app():
    app = Flask(__name__, template_folder='templates')
    app.register_blueprint(indexModule)
    app.register_blueprint(wxUserModule)
    app.register_blueprint(exportModule)
    app.register_blueprint(importModule)
    return app


app = create_app()


@app.route('/')
def home():
    return redirect('/')


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=9991, debug=True)
