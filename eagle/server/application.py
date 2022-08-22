#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2022/08/22 15:25
# @File    : application.py
# @Author  : donghaixing
# Do have a faith in what you're doing.
# Make your life a story worth telling.


from fastapi import FastAPI

app = FastAPI()


def initialize_database():
    from eagle.db.pool import POOL


def initialize_middleware():
    pass


def initialize_router():
    from eagle.router import stock
    app.include_router(stock.router)


def initialize_applications():
    pass


def initialize_server():
    initialize_applications()
    initialize_router()


initialize_server()
