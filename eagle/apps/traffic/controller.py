#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 5/20/2019 3:24 PM
# @File    : controller.py
# @Author  : donghaixing
# Do have a faith in what you're doing.
# Make your life a story worth telling.

from eagle.core.base import BaseView


class CityView(BaseView):
    table = 'city'


class LineView(BaseView):
    table = 'line'
