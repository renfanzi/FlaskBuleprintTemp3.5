#!/usr/bin/env python
# -*- coding:utf-8 -*-


from flask import Flask

from common.util.RegexConverter import RegexConverter


def create_app():
    app = Flask(__name__)
    app.url_map.converters['regex'] = RegexConverter  # 扩展调用方法
    from app.main import main as main_blueprint
    app.register_blueprint(main_blueprint, url_prefix='/main', static_folder='static',
                           template_folder='templates', )  # 意思是可以在建立一个static

    return app
