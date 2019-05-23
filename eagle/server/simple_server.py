#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 5/20/2019 2:34 PM
# @File    : simple_server.py
# @Author  : donghaixing
# Do have a faith in what you're doing.
# Make your life a story worth telling.

from eagle.server.application import app

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8000, debug=True, access_log=True)
