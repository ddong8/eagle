# -*- coding: utf-8 -*-

"""
本模块统一数据库连接池对象

@Author  : donghaixing
@File    : crud.py
@Time    : 08/10/2021 11:24 AM
"""


import threading

import sqlalchemy
from sqlalchemy.orm import scoped_session, sessionmaker


def singleton(cls):
    """单例模式装饰器"""
    instances = {}
    lock = threading.Lock()

    def _singleton(*args, **kwargs):
        with lock:
            fullkey = str((cls.__module__, cls.__name__,
                          tuple(args), tuple(kwargs.items())))
            if fullkey not in instances:
                instances[fullkey] = cls(*args, **kwargs)
        return instances[fullkey]

    return _singleton


class DBPool(object):
    """数据库连接池，单例模式"""

    def __init__(self, param=None):
        """初始化连接池

        :param params: 连接信息列表
        {connection: xxx, [pool_size: xxx], [pool_recycle: xxx], [pool_timeout: xxx], [max_overflow: xxx]}
        :type params: list
        :param connecter: 连接器，可选pymysql,psycopg2
        :type connecter: str
        :raises: None
        """
        if param:
            self.reflesh(param=param)

    def get_session(self):
        """从连接池中获取一个会话对象

        :returns: 会话对象
        :rtype: scoped_session
        :raises: ValueError
        """
        if self._pool:
            session = scoped_session(self._pool)
            return session
        raise ValueError('failed to get session')

    def transaction(self):
        """从连接池中获取一个事务对象

        :returns: 会话对象
        :rtype: scoped_session
        :raises: ValueError
        """
        if self._pool:
            session = scoped_session(self._pool)
            session.begin()
            return session
        raise ValueError('failed to get session')

    def reflesh(self, param):
        """
        重建连接池

        :param params: 连接信息列表
        {connection: xxx, [pool_size: xxx], [pool_recycle: xxx], [pool_timeout: xxx], [max_overflow: xxx]}
        :type params: list
        :param connector: 连接器，可选pymysql,psycopg2
        :type connector: str
        :returns: 是否重建成功
        :rtype: bool
        """
        param.setdefault('echo', False)
        connection = param.pop('connection')
        self._pool = sessionmaker(bind=sqlalchemy.create_engine(
            connection, **param), autocommit=True)
        return True


@singleton
class DefaultDBPool(DBPool):
    '''
    默认db配置用的单例数据库连接池
    '''
    pass


defaultPool = DefaultDBPool()
