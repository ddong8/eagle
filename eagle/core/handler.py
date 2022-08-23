#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 08/23/2022 14:13
# @File    : handler.py
# @Author  : donghaixing
# Do have a faith in what you're doing.
# Make your life a story worth telling.


import copy
import json

from ..core.base import BaseHandler
from ..core.utils import ComplexEncoder


class CollectionHandler(BaseHandler):
    """集合控制器"""
    allow_methods = ("GET", "POST")

    def get(self, *args, **kwargs):
        """
        GET方法获取集合资源
        :param args tuple参数
        :param kwargs dict参数
        :returns: None
        """
        self._validate_method(self.request, self.allow_methods)
        criteria = self._build_criteria(self.request)
        refs = self.list(copy.deepcopy(criteria), **kwargs)
        count = self.count(criteria, results=refs, **kwargs)
        if count:
            resp_json = json.loads(json.dumps(
                {'code': 0, 'msg': 'ok', 'data': {'count': count, 'data': refs}}, cls=ComplexEncoder))
            self.request.json = resp_json
            self.write(self.request.json)
        else:
            resp_json = json.loads(json.dumps(
                {'code': -1, 'msg': 'error'}, cls=ComplexEncoder))
            self.write(resp_json)

    def post(self, *args, **kwargs):
        """
        POST方法创建资源
        :param args tuple参数
        :param kwargs dict参数
        :returns: None
        """
        self._validate_method(self.request, self.allow_methods)
        self._validate_data(self.request, self.request.body)
        response = self.create(self.request.json)
        if response:
            self.set_status(status_code=201)
            resp_json = json.loads(json.dumps(
                {'code': 0, 'msg': 'ok', 'data': response}, cls=ComplexEncoder))
            self.write(resp_json)
        else:
            resp_json = json.loads(json.dumps(
                {'code': -1, 'msg': 'error'}, cls=ComplexEncoder))
            self.write(resp_json)

    def count(self, criteria, results=None, **kwargs):
        """
        根据过滤条件，统计资源
        :param req: 请求对象
        :type req: Request
        :param criteria: {'filters': filters, 'offset': offset, 'limit': limit}
        :type criteria: dict
        :param results: criteria过滤出来的结果集
        :type results: list
        :returns: 符合条件的资源数量
        :rtype: int
        """
        criteria = copy.deepcopy(criteria)
        # remove offset,limit
        criteria.pop('offset')
        criteria.pop('limit')
        criteria.pop('orders')
        return self.make_resource().count(**criteria)

    def list(self, criteria, **kwargs):
        """
        根据过滤条件，获取资源
        :param req: 请求对象
        :type req: Request
        :param criteria: {'filters': filters, 'offset': offset, 'limit': limit}
        :type criteria: dict
        :returns: 符合条件的资源
        :rtype: list
        """
        return self.make_resource().list(**criteria)

    def create(self, data, **kwargs):
        """
        创建资源
        :param req: 请求对象
        :type req: Request
        :param data: 资源的内容
        :type data: dict
        :returns: 创建后的资源信息
        :rtype: dict
        """
        return self.make_resource().create(data)


class ItemHandler(BaseHandler):
    """单项资源控制器"""
    allow_methods = ('GET', 'PATCH', 'DELETE')

    def get(self, *args, **kwargs):
        """
        获取资源详情
        :param req: 请求对象
        :type req: Request
        :returns: 资源详情信息
        :rtype: dict
        """
        self._validate_method(self.request, self.allow_methods)
        ref = self.make_resource().get(self.path_args, **kwargs)
        if ref:
            resp_json = json.loads(json.dumps(
                {'code': 0, 'msg': 'ok', 'data': ref}, cls=ComplexEncoder))
            self.write(resp_json)
        else:
            resp_json = json.loads(json.dumps(
                {'code': -1, 'msg': 'error'}, cls=ComplexEncoder))
            self.write(resp_json)

    def patch(self, *args, **kwargs):
        """
        处理PATCH请求
        :param req: 请求对象
        :type req: Request
        :param resp: 相应对象
        :type resp: Response
        """
        self._validate_method(self.request, self.allow_methods)
        self._validate_data(self.request, self.request.body)
        ref_before, ref_after = self.update(self.path_args, self.request.json)
        if ref_after:
            resp_json = json.loads(json.dumps(
                {'code': 0, 'msg': 'ok', 'data': ref_after}, cls=ComplexEncoder))
            self.write(resp_json)
        else:
            resp_json = json.loads(json.dumps(
                {'code': -1, 'msg': 'error'}, cls=ComplexEncoder))
            self.write(resp_json)

    def update(self, path_args, data, **kwargs):
        """
        更新资源
        :param path_args: 路径参数
        :type path_args: string
        :param data: 资源的内容
        :type data: dict
        :returns: 更新后的资源信息
        :rtype: dict
        """
        rid = path_args[0]
        return self.make_resource().update(rid, data)

    def delete(self, *args, **kwargs):
        """
        删除资源
        :param req: 请求对象
        :type req: Request
        :returns: 删除的资源数量
        :rtype: int
        """
        self._validate_method(self.request, self.allow_methods)
        ref, details = self.make_resource().delete(self.path_args, **kwargs)
        if ref:
            resp_json = json.loads(json.dumps(
                {'code': 0, 'msg': 'ok', 'data': {'count': ref, 'detail': details}}, cls=ComplexEncoder))
            self.write(resp_json)
        else:
            resp_json = json.loads(json.dumps(
                {'code': -1, 'msg': 'error'}, cls=ComplexEncoder))
            self.write(resp_json)