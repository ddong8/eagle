# -*- coding: utf-8 -*-

"""
本模块提供DB的CRUD封装

@Author  : donghaixing
@File    : crud.py
@Time    : 08/10/2021 11:24 AM
"""


import copy
import datetime
from contextlib import contextmanager

import sqlalchemy.exc
from loguru import logger
from ..core import exception, utils
from ..core.i18n import _
from ..db import pool


class ResourceBase(object):
    """
    资源操作基类
    """
    orm_meta = None
    _primary_keys = 'id'
    _default_order = []

    def __init__(self, session=None, transaction=None):
        self._pool = None
        self._session = session
        self._transaction = transaction
        if session is None and transaction is None:
            self._pool = pool.defaultPool

    @property
    def default_order(self):
        """
        获取默认排序规则，只读
        :return: 默认排序规则
        :rtype: list
        """

        return copy.copy(self._default_order)

    @property
    def primary_keys(self):
        """
        获取默认主键列，只读
        :return: 默认主键列
        :rtype: list
        """
        return copy.copy(self._primary_keys)

    @contextmanager
    def get_session(self):
        """
        会话管理上下文， 如果资源初始化时指定使用外部会话，则返回的也是外部会话对象
        """
        session = None
        if self._session is None and self._transaction is None:
            try:
                old_session = self._session
                session = self._pool.get_session()
                self._session = session
                yield session
            finally:
                self._session = old_session
                if session:
                    session.remove()
        elif self._session:
            yield self._session
        else:
            yield self._transaction

    @contextmanager
    def transaction(self):
        """
        事务管理上下文，如果资源初始化时指定使用外部事物，则返回的也是外部事物对象，
        保证事物统一性
        eg.
        with self.transaction() as session:
            resource(transaction=session).add()
            resource(transaction=session).update()
            resource(transaction=session).delete()
        """
        session = None
        if self._transaction is None:
            try:
                old_transaction = self._transaction
                session = self._pool.transaction()
                # 设置默认的数据库会话，所有函数都使用此会话
                self._transaction = session
                yield session
                session.commit()
            except Exception as e:
                logger.error(e)
                if session:
                    session.rollback()
                raise e
            finally:
                # 恢复原先设置
                self._transaction = old_transaction
                if session:
                    session.remove()
        else:
            yield self._transaction

    def _apply_filters(self, query, orm_meta, orders=None, filters=None):
        """
        对query应用orders filter, 返回过滤后的query
        ：param query query对象
        : param orm_meta orm_meta对象
        : param filters: 简单的等于过滤条件, eg.{'column1': value, 'column2':value}，如果None，则默认使用default filter
        : param orders 排序['+field', '-field', 'field']，+表示递增，-表示递减，不设置默认递增
        """

        filters = filters or {}
        orders = orders or []
        for name, value in filters.items():
            column = getattr(orm_meta, name, None)
            if column is not None:
                if not isinstance(value, dict):
                    query = query.filter(column == value)

        orders = orders or []

        for field in orders:
            order = '+'
            if field.startswith('+'):
                order = '+'
                field = field[1:]
            elif field.startswith('-'):
                order = '-'
                field = field[1:]

            if '.' in field:
                fields = field.split('.')
                column = getattr(orm_meta, fields.pop(0), None)
                if column:
                    for field in fields:
                        column = column[field]
            else:
                column = getattr(orm_meta, field, None)

            if column:
                if order == '+':
                    query = query.order_by(column)
                else:
                    query = query.order_by(column.desc())
        return query

    def _get_query(self, session, orm_meta=None, orders=None, filters=None, tables=None, ignore_default=False):
        """获取一个query对象，这个对象已经应用了filter，可以确保查询的数据只包含我们感兴趣的数据，常用于过滤已被删除的数据
        :param session: session对象
        :type session: session
        :param orm_meta: ORM Model, 如果None, 则默认使用self.orm_meta
        :type orm_meta: ORM Model
        :param orders: 排序['+field', '-field', 'field']，+表示递增，-表示递减，不设置默认递增
        :type orders: list
        :param filters: 简单的等于过滤条件, eg.{'column1': value, 'column2':value}
        :type filters: dict
        :returns: query对象
        :rtype: query
        :raises: ValueError
        """
        orm_meta = orm_meta or self.orm_meta
        if not ignore_default:
            orders = self.default_order if orders is None else orders
        else:
            orders = orders or []
        orders = copy.copy(orders)
        tables = tables or []
        tables = copy.copy(tables)
        tables.insert(0, orm_meta)
        if orm_meta is None:
            raise exception.CriticalError(msg=utils.format_kwstring(
                _('%(name)s.orm_meta can not be None'), name=self.__class__.__name__))
        query = session.query(*tables)
        query = self._apply_filters(query, orm_meta, orders, filters)
        return query

    def list(self, orders=None, filters=None, offset=None, limit=None):
        """
        获取资源集合.
        :param orders 排序参数集
        :param filters: 过滤条件参数集
        :param offset 游标参数
        :param limit 取数数量限制
        :return results
        """
        offset = offset or 0
        with self.get_session() as session:
            query = self._get_query(session, orders=orders, filters=filters)
            if offset:
                query = query.offset(offset)
            if limit is not None:
                query = query.limit(limit)
            records = query
            results = [rec.to_dict() for rec in records]
        return results

    def count(self, offset=None, limit=None):
        """
        计算资源数量.
        :param offset 游标参数
        :param limit 取数数量限制
        :return query count 数量
        """
        offset = offset or 0
        with self.get_session() as session:
            query = self._get_query(session, orders=[])
            if offset:
                query = query.offset(offset)
            if limit is not None:
                query = query.limit(limit)
            return query.count()

    def _apply_primary_key_filter(self, query, rid):
        """
        应用主键过滤.
        :param query 查询对象
        :param rid 主键
        :return query
        """
        keys = self.primary_keys
        if utils.is_list_type(keys) and utils.is_list_type(rid):
            if len(rid) != len(keys):
                raise exception.CriticalError(msg=utils.format_kwstring(
                    _('primary key length not match! require: %(length_require)d, input: %(length_input)d'),
                    length_require=len(keys), length_input=len(rid)))
            for idx, val in enumerate(rid):
                query = query.filter(getattr(self.orm_meta, keys[idx]) == val)
        elif utils.is_string_type(keys) and utils.is_list_type(rid) and len(rid) == 1:
            query = query.filter(getattr(self.orm_meta, keys) == rid[0])
        elif utils.is_list_type(keys) and len(keys) == 1:
            query = query.filter(getattr(self.orm_meta, keys[0]) == rid)
        elif utils.is_string_type(keys) and not utils.is_list_type(rid):
            query = query.filter(getattr(self.orm_meta, keys) == rid)
        else:
            raise exception.CriticalError(msg=utils.format_kwstring(
                _('primary key not match! require: %(keys)s'), keys=keys))
        return query

    def get(self, rid):
        """
        根据资源id获取资源.
        :param rid:
        :return: result
        """
        result = None
        with self.get_session() as session:
            query = self._get_query(session)
            query = self._apply_primary_key_filter(query, rid)
            rec_tuples = query.one_or_none()
            if rec_tuples:
                result = rec_tuples.to_detail_dict()
            else:
                return None
                # raise exception.NotFoundError('%s not found!' % rid)
        return result

    def _before_create(self, resource):
        """
        创建资源前hook操作.
        :param resource 资源对象
        :return: None
        """
        pass

    def create(self, resource):
        """
        创建资源.
        :param resource 资源对象
        :return: None
        """
        with self.get_session() as session:
            self._before_create(resource)
            orm_fields = resource
            try:
                item = self.orm_meta(**orm_fields)
                session.add(item)
                session.flush()
                session.refresh(item)
                return item.to_dict()
            except sqlalchemy.exc.IntegrityError as e:
                print(e)
            except sqlalchemy.exc.SQLAlchemyError as e:
                logger.error(e)
                raise exception.DBError(msg=_('unknown db error'))

    def update(self, rid, resource):
        """
        更新指定资源.
        :param rid 待更新资源的rid
        :param resource 资源对象
        :return: None
        """
        with self.transaction() as session:
            try:
                query = self._get_query(session)
                query = self._apply_primary_key_filter(query, rid)
                record = query.one_or_none()
                orm_fields = resource
                if record is None:
                    return None, None
                    # raise exception.NotFoundError(rid=str(rid))
                else:
                    before_update = record.to_dict()
                    if orm_fields:
                        record.update(orm_fields)
                    session.flush()
                    session.refresh(record)
                    after_update = record.to_dict()
                return before_update, after_update
            except sqlalchemy.exc.IntegrityError as e:
                logger.error(e)
            except sqlalchemy.exc.SQLAlchemyError as e:
                logger.error(e)
                raise exception.DBError(msg=_('unknown db error'))

    def query_update(self, orders, filters, resource):
        """
        查询更新指定资源.
        :param rid 待更新资源的rid
        :param resource 资源对象
        :return: None
        """
        with self.get_session() as session:
            try:
                query = self._get_query(
                    session, orders=orders, filters=filters)
                record = query.first()
                if record:
                    record.update(resource)
                    session.flush()
                    session.refresh(record)
                    return record.to_dict()
                else:
                    return None
            except sqlalchemy.exc.IntegrityError as e:
                logger.error(e)
            except sqlalchemy.exc.SQLAlchemyError as e:
                logger.error(e)
                raise exception.DBError(msg=_('unknown db error'))

    def delete(self, rid):
        """
        删除指定资源.
        :param rid 待删除资源的rid
        :param resource 资源对象
        :return: None
        """
        with self.transaction() as session:
            try:
                query = self._get_query(session, orders=[])
                query = self._apply_primary_key_filter(query, rid)
                record = query.one_or_none()
                resource = None
                count = 0
                if record is not None:
                    resource = record.to_dict()
                if getattr(self.orm_meta, 'removed', None) is not None:
                    if record is not None:
                        count = query.update(
                            {'removed': datetime.datetime.now()})
                else:
                    count = query.delete(synchronize_session=False)
                session.flush()
                return count, [resource]
            except sqlalchemy.exc.IntegrityError as e:
                logger.error(e)
            except sqlalchemy.exc.SQLAlchemyError as e:
                logger.error(e)
                raise exception.DBError(msg=_('unknown db error'))
