#!/usr/bin/env python
# -*- coding:utf-8 -*-

from werkzeug.routing import BaseConverter  # 针对url正则

class RegexConverter(BaseConverter):
    """
    URL正则扩展类
    """

    def __init__(self, url_map, *items):
        super(RegexConverter, self).__init__(url_map)
        self.regex = items[0]