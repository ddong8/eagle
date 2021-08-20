#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/5/24 16:02
# @File    : simple_server.py
# @Author  : donghaixing
# Do have a faith in what you're doing.
# Make your life a story worth telling.

from wsgiref.simple_server import make_server

from eagle.etc import settings
from eagle.server.application import app


def run():
    host = settings.HOST
    port = settings.PORT
    httpd = make_server(host=host, port=port, app=app)
    print("Serving on %s:%d..." % (host, port))
    httpd.serve_forever()
