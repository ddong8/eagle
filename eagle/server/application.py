#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 5/20/2019 3:25 PM
# @File    : application.py
# @Author  : donghaixing
# Do have a faith in what you're doing.
# Make your life a story worth telling.

import sys

import asyncpg
from sanic import Sanic

from eagle.core.db import DB

app = Sanic('eagle')
app.config.update_config('./eagle/etc/settings.py')


@app.main_process_start
async def initialize_app(application, loop):
    """
    register route.
    :param application: Sanic object
    :param loop: Sanic async event loop
    :return: None
    """
    for name in application.config.APPS:
        if name:
            __import__(name)
            module = sys.modules[name]
            module.route.add_routes(application)


@app.before_server_start
async def initialize_db(application, loop):
    """
    initialize database.
    :param application: Sanic object
    :param loop: Sanic async event loop
    :return: None
    """
    application.ctx.db_pool = await asyncpg.create_pool(
        **application.config.DB_CFG,
        max_inactive_connection_lifetime=60,
        min_size=10,
        max_size=10,
        loop=loop,
    )
    application.ctx.db = DB(application.ctx.db_pool)
