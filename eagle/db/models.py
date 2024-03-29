# -*- coding: utf-8 -*-

"""
本模块提供orm模型类

@Author  : donghaixing
@File    : handler.py
@Time    : 08/24/2022 11:14
"""


from sqlalchemy import DECIMAL, Column, Integer, String, Text
from sqlalchemy.ext.declarative import declarative_base

from .dictbase import DictBase

Base = declarative_base()
metadata = Base.metadata


class Stock(Base, DictBase):
    """stock table"""
    __tablename__ = 'stock'

    id = Column(String(64), primary_key=True)
    code = Column(Text, nullable=True)
    name = Column(Text, nullable=True)
    trade_date = Column(Text, nullable=True)
    change_rate = Column(DECIMAL(53, 6), nullable=True)
    close_price = Column(DECIMAL(53, 6), nullable=True)
    buy_amt = Column(DECIMAL(53, 6), nullable=True)
    net_buy_amt = Column(DECIMAL(53, 6), nullable=True)
    accum_amount = Column(Integer, nullable=True)
    market = Column(Text, nullable=True)
    explanation = Column(Text, nullable=True)
