#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2022/08/22 10:24
# @File    : fastapi.py
# @Author  : donghaixing
# Do have a faith in what you're doing.
# Make your life a story worth telling.

import uvicorn
from typing import Union
from fastapi import FastAPI
from eagle.workers.stock import tasks

app = FastAPI()


@app.get("/")
async def read_root():
    return {"Hello": "World"}


@app.get("/items/{item_id}")
async def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}


@app.put("/stock/sync_data/{date_str}")
async def sync_stock_data(date_str: str):
    tasks.get_top_list(date_str)
    return {"date": date_str}


if __name__ == '__main__':
    uvicorn.run("api_server:app", host="0.0.0.0", port=9000)
