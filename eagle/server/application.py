#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2022/08/22 15:25
# @File    : application.py
# @Author  : donghaixing
# Do have a faith in what you're doing.
# Make your life a story worth telling.


from fastapi import FastAPI
from loguru import logger

app = FastAPI()


def initialize_logger():
    logger.add("eagle_api.log", rotation="500 MB", enqueue=True)
    logger.info("logger initialize done...")


def initialize_database():
    from eagle.db.pool import POOL


def initialize_middleware():
    pass


def initialize_router():
    from eagle.router import stock
    app.include_router(stock.router)


def initialize_applications():
    initialize_router()
    initialize_router()


def initialize_server():
    initialize_logger()
    initialize_database()
    initialize_applications()


initialize_server()
