#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 5/20/2019 3:25 PM
# @File    : application.py
# @Author  : donghaixing
# Do have a faith in what you're doing.
# Make your life a story worth telling.

import sys

import falcon
from eagle.etc import settings

api = falcon.App()


def initialize_applications(api):
    """初始化wsgi application"""
    for name in settings.APPS:
        if name:
            __import__(name)
            app = sys.modules[name]
            app.route.add_routes(api)

    return api


app = initialize_applications(api)
