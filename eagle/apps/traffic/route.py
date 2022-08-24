#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 5/20/2019 3:23 PM
# @File    : route.py
# @Author  : donghaixing
# Do have a faith in what you're doing.
# Make your life a story worth telling.


from eagle.common import async_helper
from eagle.workers.stock import callback


def add_routes(api):
    """
    Add route
    :param api: Sanic object
    :return: None
    """
    async_helper.add_callback_route(api, callback.callback_add)
