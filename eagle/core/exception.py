# -*- coding: utf-8 -*-

"""
本模块提供异常信息封装

@Author  : donghaixing
@File    : handler.py
@Time    : 08/24/2022 11:14
"""


from __future__ import absolute_import

import json


class Error(Exception):
    """异常基类"""
    code = 500

    def __init__(self, message=None, exception_data=None, **kwargs):
        if message is not None:
            self.message = message
        else:
            self._build_message(**kwargs)
        self._exception_data = exception_data or {}
        # code,title,description为保留字段
        self._exception_data.pop('code', None)
        self._exception_data.pop('title', None)
        self._exception_data.pop('description', None)
        super(Error, self).__init__(self.message, self._exception_data)

    def _build_message(self, **kwargs):
        self.message = self.message_format % kwargs

    def __str__(self):
        return self.message

    @property
    def message_format(self):
        return 'Unknown Error'

    @property
    def title(self):
        return None

    @property
    def exception_data(self):
        return self._exception_data

    def to_dict(self):
        data = {'code': self.code, 'title': self.title,
                'description': self.message}
        exception_data = self._exception_data.copy()
        if exception_data:
            data.update(exception_data)
        return data

    def to_json(self):
        data = self.to_dict()
        return json.dumps(data)


class CallBackError(Error):
    """接收并转换Restful错误异常"""

    def __init__(self, message, exception_data=None):
        self._message = message
        if isinstance(message, dict):
            self.message = message.get('description', 'Unknown')
            self.code = message.get('code', 500)
        self._exception_data = exception_data or {}
        # code,title,description为保留字段
        self._exception_data.pop('code', None)
        self._exception_data.pop('title', None)
        self._exception_data.pop('description', None)
        Exception.__init__(self, message)

    @property
    def title(self):
        if isinstance(self._message, dict):
            return self._message.get('title', 'Unknown')
        else:
            return self._message

    def __str__(self):
        if isinstance(self._message, dict):
            return self._message.get('description', 'Unknown')
        else:
            return self._message


class CriticalError(Error):
    """重大错误异常"""
    code = 500

    @property
    def title(self):
        return 'Server Error'

    @property
    def message_format(self):
        return 'detail: %(msg)s'


class DBError(Error):
    """DB错误异常"""
    code = 400

    @property
    def title(self):
        return 'DB Error'

    @property
    def message_format(self):
        return 'detail: %(msg)s'


class BodyParseError(Error):
    """解析错误异常"""
    code = 400

    @property
    def title(self):
        return 'HTTP Body Error'

    @property
    def message_format(self):
        return 'detail: body parse error: %(msg)s'


class ValidationError(Error):
    """验证错误异常"""
    code = 400

    @property
    def title(self):
        return 'Validation Error'

    @property
    def message_format(self):
        return 'detail: column %(attribute)s validate failed, because: %(msg)s'


class NotEnoughError(Error):
    """资源不足异常"""
    code = 400

    @property
    def title(self):
        return 'Resource NotEnough'

    @property
    def message_format(self):
        return 'detail: %(resource)s not enough'


class FieldRequired(ValidationError):
    """验证错误，字段缺失异常"""
    code = 400

    @property
    def title(self):
        return _('Field Missing')

    @property
    def message_format(self):
        return 'column: %(attribute)s must be specific'


class LoginError(Error):
    """认证错误异常"""
    code = 401

    @property
    def title(self):
        return 'Unauthorized'

    @property
    def message_format(self):
        return 'detail: ops, username or password error, login deny'


class AuthError(Error):
    """认证错误异常"""
    code = 401

    @property
    def title(self):
        return 'Unauthorized'

    @property
    def message_format(self):
        return 'detail: you are unauthenticated, login needed'


class ForbiddenError(Error):
    """认证错误异常"""
    code = 403

    @property
    def title(self):
        return 'Forbidden'

    @property
    def message_format(self):
        return 'detail: you are not allow to perfrom this action'


class NotFoundError(Error):
    """资源不存在异常"""
    code = 404

    @property
    def title(self):
        return 'Not Found'

    @property
    def message_format(self):
        return 'detail: the resource(%(resource)s) you request not found'


class MethodForbiddenError(Error):
    """HTTP方法不允许访问"""
    code = 405

    @property
    def title(self):
        return 'Method Not Allowed'

    @property
    def message_format(self):
        return 'detail: method you request is not allow to perfrom'


class ConflictError(Error):
    """约束冲突错误异常"""
    code = 409

    @property
    def title(self):
        return 'Conflict'

    @property
    def message_format(self):
        return 'detail: %(msg)s'
