#!/usr/bin/env python
# -*- coding:utf-8 -*-

from flask import Blueprint
from flask_restful import Api, Resource

# 这里是需要注意的地方之一
main = Blueprint('main', __name__, static_folder='static', template_folder='templates', )
main_api = Api(main)

from . import view
