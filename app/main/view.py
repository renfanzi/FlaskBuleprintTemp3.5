#!/usr/bin/env python
# -*- coding:utf-8 -*-
from flask import Flask, render_template, request, redirect, url_for, make_response
from . import main
from . import main_api
from flask_restful import Resource
import pandas as pd
import logging
from logging.handlers import RotatingFileHandler
from sqlalchemy import create_engine
from flask import request, g, jsonify
from common.base import Config
import os
from common.base import LogPath
from scipy import stats



@main.route('/usr/<regex("[a-z]{3}"):user_id>')
# 正则扩展方法展示
def user_id(user_id):
    # return user_id
    return redirect(url_for('main.hello_world'))  # 看这里跳转的时候是方法名需要注意了


@main_api.resource('/userapi/')
class user(Resource):
    @staticmethod
    def get():
        user_id = request.args.get("user_id")
        return user_id


def setup_db():
    pass


def do_chisquare2way(v1, v2):

    # x2 = stats.chisquare(v1, f_exp=v2)


    # return {'p': x2['p'], 'df': x2['df'], 'chisq': x2['chisq'], 'N': x2['N']}
    return {}


@main.route('/v1/chisquare2way/<string:v1>:<string:v2>:<string:table>:<string:where>', methods=['GET'])
def chisquare_get(v1, v2, table, where):
    if request.method == 'GET':
        ret = Config().get_content('mysql')
        SQLALCHEMY_DATABASE_URI = "mysql+pymysql://{}:{}@{}:{}/{}?charset=utf8".format(ret['user'],
                                                                                       ret['password'],
                                                                                       ret['host'],
                                                                                       ret['port'],
                                                                                       ret['db_name'])
        Sqlal = create_engine(SQLALCHEMY_DATABASE_URI,
                              pool_size=20,
                              pool_recycle=3600,
                              max_overflow=10,
                              encoding='utf-8',
                              )
        sql = "select {}, {} from {} where {};".format(v1, v2, table, where)
        df = pd.read_sql(sql, Sqlal)
        df_dropna = df.dropna()

        ret = do_chisquare2way(df_dropna[v1], df_dropna[v2])
        return jsonify(ret)


if __name__ == '__main__':
    ret = os.path.join(os.path.dirname(os.path.dirname(__file__)))
    print(ret)
