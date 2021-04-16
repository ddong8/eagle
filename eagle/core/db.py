#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 5/20/2019 6:54 PM
# @File    : db.py
# @Author  : donghaixing
# Do have a faith in what you're doing.
# Make your life a story worth telling.


class DB:
    def __init__(self, db_pool):
        self.db_pool = db_pool

    async def fetch(self, sql, *args, **kwargs):
        async with self.db_pool.acquire() as connection:
            return await connection.fetch(sql, *args, **kwargs)

    async def execute(self, sql, *args, **kwargs):
        async with self.db_pool.acquire() as connection:
            return await connection.execute(sql, *args, **kwargs)
