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
    return json(results)


class CollectionView(HTTPMethodView):
    """
    BaseView for HTTP method 'GET','POST'
    """
    table_name = None

    async def get(self, request, *args, **kwargs):
        sql = curd.get_r_sql(self.table_name, conditions=request.raw_args)
        records = await request.app.db.fetch(sql)
        return records_to_json(records)

    async def post(self, request, *args, **kwargs):
        data = request.json
        sql = curd.get_c_sql(self.table_name, data)
        await request.app.db.execute(sql)
        return json(data)


class ItemView(HTTPMethodView):
    """
    ItemView for HTTP method 'GET','PATCH','PUT','DELETE'
    """
    primary_key = None
    table_name = None

    async def get(self, request, *args, **kwargs):
        sql = curd.get_r_sql(self.table_name, conditions={self.primary_key: kwargs['rid']})
        records = await request.app.db.fetch(sql)
        return records_to_json(records)

    async def patch(self, request, *args, **kwargs):
        data = request.json
        sql = curd.get_u_sql(self.table_name, data, conditions={self.primary_key: kwargs['rid']})
        await request.app.db.execute(sql)
        return json(data)

    async def put(self, request, *args, **kwargs):
        data = request.json
        sql = curd.get_u_sql(self.table_name, data, conditions={self.primary_key: kwargs['rid']})
        await request.app.db.execute(sql)
        return json(data)

    async def delete(self, request, *args, **kwargs):
        sql = curd.get_d_sql(self.table_name, conditions={self.primary_key: kwargs['rid']})
        await request.app.db.execute(sql)
        return json({'count': 1, 'rid': kwargs['rid']})
