# -*- coding: utf-8 -*-
import os
from flask import Flask
from web.index.views import mod as indexModule
from web.wxuser.views import mod as wxUserModule
from web.dataexport.views import mod as exportModule
from web.dataimport.views import mod as importModule


def create_app():
    app = Flask(__name__, template_folder='templates')
    app.register_blueprint(indexModule)
    app.register_blueprint(wxUserModule)
    app.register_blueprint(exportModule)
    app.register_blueprint(importModule)
    return app
