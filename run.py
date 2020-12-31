#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
from flask import Flask, Blueprint, url_for, render_template, request, abort, flash, session, redirect
from web.index.views import mod as indexModule
from web.wxuser.views import mod as wxUserModule
from web.dataexport.views import mod as exportModule
from web.dataimport.views import mod as importModule


def create_app(static_folder='web/static', template_folder='web/templates'):
    app = Flask(__name__, static_folder=static_folder, template_folder=template_folder)
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
