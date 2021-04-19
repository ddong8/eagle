#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 5/21/2019 12:05 PM
# @File    : settings.py
# @Author  : donghaixing
# Do have a faith in what you're doing.
# Make your life a story worth telling.

import multiprocessing

workers = multiprocessing.cpu_count() * 2 + 1

HOST = '0.0.0.0'
PORT = 9000

DEBUG = False
ACCESS_LOG = True

WORKERS = workers

DB_CFG = {
    "host": "193.123.248.180",
    "database": "ork",
    "user": "postgres",
    "password": "123456"
}

APPS = [
    'eagle.apps.traffic',
]
