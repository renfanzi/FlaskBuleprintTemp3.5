#!/usr/bin/env python
# -*- coding:utf-8 -*-

import configparser
import os
import datetime
import time
import pymysql



LogPath= os.path.join(os.path.dirname(__file__), "log", "flask.log")


class Config(object):
    """
    # Config().get_content("user_information")
    """
    def __init__(self, config_filename="my.cnf"):
        file_path = os.path.join(os.path.dirname(__file__), 'config', config_filename)
        print(file_path)
        self.cf = configparser.ConfigParser()
        self.cf.read(file_path)

    def get_sections(self):
        return self.cf.sections()

    def get_options(self, section):
        return self.cf.options(section)

    def get_content(self, section):
        result = {}
        for option in self.get_options(section):
            value = self.cf.get(section, option)
            result[option] = int(value) if value.isdigit() else value
        return result


def result(status, value):
    """
    staatus:
    2000, 什么都ok
    4000, 客户上传的文件格式不正确
    4001， 客户上传的文件列超过5400
    4002， 暂时梅想到
    5000， 服务器错误
    5001， 数据表已经存在
    5002,  sql语句错误
    """
    if status == 2000:
        message = u"True"
    elif status == 4000:
        message = u"客户上传的文件格式不正确"
    elif status == 4001:
        message = u"客户上传的文件列超过5400"
    elif status == 4002:
        message = u"暂时梅想到"
    elif status == 5000:
        message = u"服务器错误"
    elif status == 5001:
        message = u"数据表已经存在"
    elif status == 5002:
        message = u"sql语句错误"
    else:
        message = u"未知错误"
    return {
        "statuscode": status,
        "statusmessage": message,
        "value": value
    }


class base_pymysql(object):
    def __init__(self, host, port, user, password, db_name):
        self.db_host = host
        self.db_port = int(port)
        self.user = user
        self.password = str(password)
        self.db = db_name
        self.conn = None
        self.cursor = None

    def connect(self):
        self.conn = pymysql.connect(host=self.db_host, port=self.db_port, user=self.user,
                                    passwd=self.password, db=self.db, charset="utf8")
        self.cursor = self.conn.cursor(cursor=pymysql.cursors.DictCursor)


class MyPymysql(base_pymysql):
    """
    Basic Usage:
        ret = My_Pymysql('test1')
        res = ret.selectone_sql("select * from aaa")
        print(res)
        ret.close()
    Precautions:
        Config.__init__(self, config_filename="zk_css.cnf")
    """
    def __init__(self, conf_name):
        self.conf = Config().get_content(conf_name)
        super(MyPymysql, self).__init__(**self.conf)
        self.connect()

    def idu_sql(self, sql):
        # adu: insert, delete, update的简写
        # 考虑到多语句循环, try就不写在这里了
        self.cursor.execute(sql)
        self.conn.commit()

    def insert_sql(self, sql, value=None):
        # adu: insert, delete, update的简写
        self.cursor.execute(sql, value)
        self.conn.commit()

    def selectone_sql(self, sql):
        self.cursor.execute(sql)
        self.conn.commit()
        return self.cursor.fetchone()

    def selectall_sql(self, sql):
        self.cursor.execute(sql)
        self.conn.commit()
        return self.cursor.fetchall()

    def close(self):
        self.conn.close()
        self.conn = None
        self.cursor = None

if __name__ == '__main__':
    # ret = Config().get_content('mysql')
    # print(ret)
    print(LogPath)