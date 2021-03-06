#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 5/23/2019 10:01 AM
# @File    : curd.py
# @Author  : donghaixing
# Do have a faith in what you're doing.
# Make your life a story worth telling.


def safe_cast_2_str(val, default=''):
    """
    :param val: any->need to convert value
    :param default: ''
    :return: string
    """
    try:
        return str(val)
    except (ValueError, TypeError):
        return default


def dict_2_str(fields):
    """
    convert dict to string format: key = 'value',key = 'value'
    :param fields:dict->fields dict
    :return: string
    """
    tmp_list = []
    for k, v in fields.items():
        tmp = "{}='{}'".format(str(k), safe_cast_2_str(v))
        tmp_list.append(' {} '.format(tmp))
    return ','.join(tmp_list)


def dict_2_str_and(fields):
    """
    convert dict to string format: key = 'value' and key = 'value'
    :param fields:dict->fields dict
    :return: string
    """
    tmp_list = []
    for k, v in fields.items():
        tmp = "{}='{}'".format(str(k), safe_cast_2_str(v))
        tmp_list.append(' {} '.format(tmp))
    return ' AND '.join(tmp_list)


def tuple_2_str(fields):
    """
    convert tuple to string format: key1,key2,key3
    :param fields:dict->fields dict.
    :return: string
    """
    tmp1 = [str(i) for i in fields.keys()]
    tmp2 = ["'{}'".format(safe_cast_2_str(i)) for i in fields.values()]
    return ','.join(tmp1), ','.join(tmp2)


def get_r_sql(table, conditions):
    """
    generate select sql statement.
    :param table:string->query table name
    :param conditions:dict->query conditions
    :return:string
    """
    sql = 'SELECT * FROM {}'.format(table)
    if conditions:
        sql += ' WHERE {}'.format(dict_2_str_and(conditions))
    return sql


def get_u_sql(table, fields, conditions):
    """
    generate update sql statement.
    :param table:string->query table name
    :param fields:dict->query fields
    :param conditions:dict->query conditions
    :return: string
    """
    sql = 'UPDATE {} SET '.format(table)
    sql += dict_2_str(fields)
    if conditions:
        sql += ' WHERE {}'.format(dict_2_str_and(conditions))
    return sql


def get_c_sql(table, fields):
    """
    generate insert sql statement.
    :param table:string->query table name
    :param fields:dict->query fields.
    :return:string
    """
    keys, values = tuple_2_str(fields)
    sql = 'INSERT INTO {} ({}) VALUES ({})'.format(table, keys, values)
    return sql


def get_d_sql(table, conditions):
    """
    generate delete sql statement.
    :param table:string->query table name
    :param conditions:dict->query conditions.
    :return:string-->sql
    """
    sql = 'DELETE FROM {}'.format(table)
    if conditions:
        sql += ' WHERE {}'.format(dict_2_str_and(conditions))
    return sql
