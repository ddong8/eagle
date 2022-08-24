#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 5/20/2019 3:24 PM
# @File    : route.py
# @Author  : donghaixing
# Do have a faith in what you're doing.
# Make your life a story worth telling.


from ...db import models
from ...db.crud import ResourceBase


class Stock(ResourceBase):
    orm_meta = models.Stock
    _primary_keys = ('id',)
