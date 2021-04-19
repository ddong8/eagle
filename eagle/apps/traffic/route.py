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
    """
    Add route
    :param api: Sanic object
    :return: None
    """
    api.add_route(controller.CityCollection.as_view(), '/cities')
    api.add_route(controller.CityItem.as_view(), '/city/<rid>')
    api.add_route(controller.LineCollection.as_view(), '/lines')
    api.add_route(controller.LineItem.as_view(), '/line/<rid>')
    api.add_route(controller.RegionCollection.as_view(), '/regions')
    api.add_route(controller.RegionItem.as_view(), '/region/<rid>')
    api.add_route(controller.ProvinceCollection.as_view(), '/provinces')
    api.add_route(controller.ProvinceItem.as_view(), '/province/<rid>')
    api.add_route(controller.StockCollection.as_view(), '/stocks')
    api.add_route(controller.StockItem.as_view(), '/stock/<rid>')

    @api.route("/")
    async def index(request):
        """
        index url
        :param request: Sanic request.
        :return: html
        """
        return response.html(body="welcome come to api service!", status=200)
