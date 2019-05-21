#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 5/20/2019 5:13 PM
# @File    : base.py
# @Author  : donghaixing
# Do have a faith in what you're doing.
# Make your life a story worth telling.

from sanic.response import json
from sanic.response import text
from sanic.views import HTTPMethodView


class BaseView(HTTPMethodView):
    table = None

    async def get(self, request):
        records = await request.app.db.fetch("select * from %s" % self.table)
        data = []
        if records:
            for record in records:
                data.append(dict(record))
        results = {'count': len(data), 'data': data}
        return json(results)

    async def post(self, request):
        return text('I am post method')

    async def put(self, request):
        return text('I am put method')

    async def patch(self, request):
        return text('I am patch method')

    async def delete(self, request):
        return text('I am delete method')
