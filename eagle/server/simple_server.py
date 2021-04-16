#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/5/24 16:02
# @File    : simple_server.py
# @Author  : donghaixing
# Do have a faith in what you're doing.
# Make your life a story worth telling.

from eagle.server.application import app


def run():
    config = app.config
    app.run(host=config.HOST, port=config.PORT,
            debug=config.DEBUG, access_log=config.ACCESS_LOG, workers=config.WORKERS)
