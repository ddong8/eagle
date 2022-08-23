#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2022/08/22 15:25
# @File    : application.py
# @Author  : donghaixing
# Do have a faith in what you're doing.
# Make your life a story worth telling.


import uvicorn
from eagle.core.logger import init_logger
from eagle.etc import settings
from fastapi import FastAPI

app = FastAPI()


def initialize_logger():
    init_logger()


def initialize_database():
    from eagle.db import pool
    pool.defaultPool.reflesh(param=settings.DB_CONFIG)


def initialize_middleware():
    pass


def initialize_router():
    from eagle.apps import stock
    app.include_router(stock.router)


def initialize_applications():
    initialize_database()
    initialize_middleware()
    initialize_router()


def initialize_server():
    config = uvicorn.Config("eagle.server.application:app",
                            host=settings.HOST,
                            port=settings.PORT,
                            reload=True,
                            access_log=True)
    server = uvicorn.Server(config)
    initialize_logger()
    initialize_applications()
    return server


server = initialize_server()
