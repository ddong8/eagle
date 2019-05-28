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
    table_name = "city"
    primary_key = 'uuid'


class CityItem(ItemView):
    table_name = "city"
    primary_key = 'uuid'


class LineCollection(CollectionView):
    table_name = "line"
    primary_key = 'uuid'


class LineItem(ItemView):
    table_name = "line"
    primary_key = 'uuid'


class RegionCollection(CollectionView):
    table_name = "region"
    primary_key = 'uuid'


class RegionItem(ItemView):
    table_name = "region"
    primary_key = 'uuid'


class ProvinceCollection(CollectionView):
    table_name = "province"
    primary_key = 'uuid'


class ProvinceItem(ItemView):
    table_name = "province"
    primary_key = 'uuid'
