#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 5/20/2019 3:24 PM
# @File    : controller.py
# @Author  : donghaixing
# Do have a faith in what you're doing.
# Make your life a story worth telling.

from eagle.core.base import CollectionView
from eagle.core.base import ItemView


class CityCollection(CollectionView):
    TABLE_NAME = "city"
    PK_KEY = 'uuid'


class CityItem(ItemView):
    TABLE_NAME = "city"
    PK_KEY = 'uuid'


class LineCollection(CollectionView):
    TABLE_NAME = "line"
    PK_KEY = 'uuid'


class LineItem(ItemView):
    TABLE_NAME = "line"
    PK_KEY = 'uuid'


class RegionCollection(CollectionView):
    TABLE_NAME = "region"
    PK_KEY = 'uuid'


class RegionItem(ItemView):
    TABLE_NAME = "region"
    PK_KEY = 'uuid'


class ProvinceCollection(CollectionView):
    TABLE_NAME = "province"
    PK_KEY = 'uuid'


class ProvinceItem(ItemView):
    TABLE_NAME = "province"
    PK_KEY = 'uuid'
