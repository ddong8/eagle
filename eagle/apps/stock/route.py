#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 5/20/2019 3:24 PM
# @File    : route.py
# @Author  : donghaixing
# Do have a faith in what you're doing.
# Make your life a story worth telling.


from eagle.workers.stock import tasks
from fastapi import APIRouter

from .resource import Stock

router = APIRouter(
    prefix="/stock",
)


@router.get("/get_lhb_data/{date_str}")
async def get_stock_data(date_str: str):
    stock_data = Stock().list(filters={'trade_date': date_str})
    return {"data": stock_data}


@router.put("/sync_lhb_data/{date_str}")
async def sync_stock_data(date_str: str):
    tasks.get_top_list(date_str)
    return {"date": date_str}
