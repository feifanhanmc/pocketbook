# -*- coding: utf-8 -*-
import os
from flask import Flask
from elasticsearch import Elasticsearch
from web.webapp.risk_user.views import mod as riskUserModule
from web.webapp.index.views import mod as indexModule

def create_app():
    app = Flask(__name__, template_folder='templates')
    app.register_blueprint(indexModule)
    app.register_blueprint(riskUserModule)
    app.config['DEBUG'] = True
    return app
