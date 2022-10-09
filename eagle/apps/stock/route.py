#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 5/20/2019 3:24 PM
# @File    : route.py
# @Author  : donghaixing
# Do have a faith in what you're doing.
# Make your life a story worth telling.


from datetime import date
from eagle.workers.stock import tasks
from fastapi import APIRouter

from .controller import lhb_data, realtime_data
from .resource import Stock

router = APIRouter(
    prefix="/stock",
)


@router.get("/get_realtime_data/{stock_code}")
async def get_realtime_data(stock_code: str):
    data = realtime_data(stock_code)
    return {"data": data}


@router.get("/get_lhb_data/{date_str}")
async def get_lhb_data(date_str: str):
    data = lhb_data(date_str)
    return {"data": data}


@router.get("/get_lhb_datas/")
async def get_lhb_datas(startDate: str = date.today().isoformat(), endDate: str = date.today().isoformat()):
    data = Stock().filter({"trade_date": startDate})
    return {"data": data}


@router.put("/sync_lhb_data/{date_str}")
async def sync_stock_data(date_str: str):
    tasks.get_top_list(date_str)
    return {"date": date_str}
