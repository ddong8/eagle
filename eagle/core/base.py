#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 5/22/2019 3:11 PM
# @File    : base.py
# @Author  : donghaixing
# Do have a faith in what you're doing.
# Make your life a story worth telling.

from sanic.response import json
from sanic.views import HTTPMethodView


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
        sql = "SELECT * FROM %s" % self.TABLE_NAME
        records = await request.app.db.fetch(sql)
        results = records_to_json(records)
        return json(results)

    async def post(self, request, *args, **kwargs):
        data = request.json
        if data:
            titles = ", ".join(tuple(data.keys()))
            values = str(tuple(data.values()))
            sql = "INSERT INTO %s (%s) VALUES %s" % (self.TABLE_NAME, titles, values)
            await request.app.db.execute(sql)
            return json(data)


class ItemView(HTTPMethodView):
    """
    ItemView for HTTP method 'GET','PATCH','PUT','DELETE'
    """
    PK_KEY = None
    TABLE_NAME = None

    async def get(self, request, *args, **kwargs):
        sql = "SELECT * FROM %s WHERE %s = '%s'" % (self.TABLE_NAME, self.PK_KEY, kwargs['rid'])
        records = await request.app.db.fetch(sql)
        results = records_to_json(records)
        return json(results)

    async def patch(self, request, *args, **kwargs):
        data = request.json
        if data:
            titles = ", ".join(tuple(data.keys()))
            values = str(tuple(data.values()))
            sql = "INSERT INTO %s (%s) VALUES %s" % (self.TABLE_NAME, titles, values)
            await request.app.db.execute(sql)
            return json(data)

    async def put(self, request, *args, **kwargs):
        data = request.json
        if data:
            update_item = ""
            for item in data:
                update_item = "%s = %s," % (item, data[item])
            update_item = update_item[:-1]
            sql = "UPDATE %s SET %s WHERE  %s = %s" % (self.TABLE_NAME, update_item, self.PK_KEY, kwargs['rid'])
            await request.app.db.execute(sql)
            return json(data)

    async def delete(self, request, *args, **kwargs):
        sql = "DELETE * FROM %s WHERE %s = '%s'" % (self.TABLE_NAME, self.PK_KEY, kwargs['rid'])
        records = await request.app.db.fetch(sql)
        results = records_to_json(records)
        return json(results)
