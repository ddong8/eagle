#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 5/22/2019 3:11 PM
# @File    : base.py
# @Author  : donghaixing
# Do have a faith in what you're doing.
# Make your life a story worth telling.

from sanic.response import json
from sanic.views import HTTPMethodView

from eagle.core import curd


def records_to_json(records):
    """
    convert asyncpg.record to json
    :param records: list
    :return: dict
    """
    data = []
    if records:
        for record in records:
            data.append(dict(record))
    results = {'count': len(data), 'data': data}
    return results


class CollectionView(HTTPMethodView):
    """
    BaseView for HTTP method 'GET','POST'
    """
    TABLE_NAME = None

    async def get(self, request, *args, **kwargs):
        sql = curd.get_s_sql(self.TABLE_NAME, keys=None, conditions=None)
        records = await request.app.db.fetch(sql)
        results = records_to_json(records)
        return json(results)

    async def post(self, request, *args, **kwargs):
        data = request.json
        sql = curd.get_c_sql(self.TABLE_NAME, data)
        await request.app.db.execute(sql)
        return json(data)


class ItemView(HTTPMethodView):
    """
    ItemView for HTTP method 'GET','PATCH','PUT','DELETE'
    """
    PK_KEY = None
    TABLE_NAME = None

    async def get(self, request, *args, **kwargs):
        sql = curd.get_s_sql(self.TABLE_NAME, keys=None, conditions={self.PK_KEY: kwargs['rid']})
        records = await request.app.db.fetch(sql)
        results = records_to_json(records)
        return json(results)

    async def patch(self, request, *args, **kwargs):
        data = request.json
        sql = curd.get_u_sql(self.TABLE_NAME, data, conditions={self.PK_KEY: kwargs['rid']})
        await request.app.db.execute(sql)
        return json(data)

    async def put(self, request, *args, **kwargs):
        data = request.json
        sql = curd.get_u_sql(self.TABLE_NAME, data, conditions={self.PK_KEY: kwargs['rid']})
        await request.app.db.execute(sql)
        return json(data)

    async def delete(self, request, *args, **kwargs):
        sql = curd.get_d_sql(self.TABLE_NAME, conditions={self.PK_KEY: kwargs['rid']})
        await request.app.db.execute(sql)
        return json({'count': 1, 'rid': kwargs['rid']})
