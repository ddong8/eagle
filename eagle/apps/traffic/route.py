#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 5/20/2019 3:23 PM
# @File    : route.py
# @Author  : donghaixing
# Do have a faith in what you're doing.
# Make your life a story worth telling.

from sanic import response

from eagle.apps.traffic import controller


def add_routes(api):
    api.add_route(controller.CityView.as_view(), '/city')
    api.add_route(controller.LineView.as_view(), '/line')

    @api.route("/index")
    async def test(request):
        result = await request.app.db.fetch('select * from city')
        print(result)
        return response.json({"test": True})
