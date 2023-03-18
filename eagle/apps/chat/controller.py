#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 5/20/2019 3:24 PM
# @File    : controller.py
# @Author  : donghaixing
# Do have a faith in what you're doing.
# Make your life a story worth telling.


import json
from uuid import uuid4

import requests


def realtime_data(stock_code):
    headers = {"Referer": "https://finance.sina.com.cn"}
    if stock_code.startswith('6'):
        stock_code = 'sh' + stock_code
    elif stock_code.startswith('0') or stock_code.startswith('3'):
        stock_code = 'sz' + stock_code
    url = f'http://hq.sinajs.cn/list={stock_code}'
    ret = requests.get(url, headers=headers)
    resp_data = ret.text
    start = resp_data.find('"') + 1
    end = resp_data.rfind('"') - 1
    data_list = []
    if end > start:
        data_str = resp_data[start:end]
        data_list = data_str.split(",")
    return data_list


def lhb_data(date_str):
    url = f'https://datacenter-web.eastmoney.com/api/data/v1/get?callback=jQuery112307541372703667037_1660893715485&sortColumns=NET_BUY_AMT&sortTypes=-1&pageSize=500&pageNumber=1&reportName=RPT_ORGANIZATION_TRADE_DETAILS&columns=ALL&source=WEB&client=WEB&filter=(TRADE_DATE%3E=%27{date_str}%27)'
    resp = requests.get(url)
    raw_data = resp.text
    raw_data = resp.text.split('(')[1].split(')')[0]
    json_data = json.loads(raw_data)
    stock_data_list = json_data['result']['data']
    data_list = []
    for stock in stock_data_list:
        data_list.append({
            'id': str(uuid4()),
            'code': stock['SECURITY_CODE'],
            'name': stock['SECURITY_NAME_ABBR'],
            'trade_date': stock['TRADE_DATE'].split(" ")[0],
            'change_rate': stock['CHANGE_RATE'],
            'close_price': stock['CLOSE_PRICE'],
            'buy_amt': stock['BUY_AMT'],
            'net_buy_amt': stock['NET_BUY_AMT'],
            'accum_amount': stock['ACCUM_AMOUNT'],
            'market': stock['MARKET'],
            'explanation': stock['EXPLANATION']
        })
    return data_list


