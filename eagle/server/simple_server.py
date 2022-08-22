#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2022/08/22 14:02
# @File    : simple_server.py
# @Author  : donghaixing
# Do have a faith in what you're doing.
# Make your life a story worth telling.


import uvicorn
from eagle.etc import settings


def run():
    host = settings.HOST
    port = settings.PORT
    uvicorn.run("eagle.server.application:app",
                host=host, port=port, reload=True)
