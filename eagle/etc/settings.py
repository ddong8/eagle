#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 5/21/2019 12:05 PM
# @File    : settings.py
# @Author  : donghaixing
# Do have a faith in what you're doing.
# Make your life a story worth telling.


import os
import json
import logging
import sys

from celery.schedules import crontab

HOST = '0.0.0.0'
PORT = 9000

APP_NAME = 'eagle'

PUBLIC_ENDPOINT = 'http://eagle_web:9000'

APPS = [
    'eagle.apps.traffic',
]

CONN_STR = "postgresql+psycopg2://postgres:123456@global.ihasy.com/ork"

DB_CONFIG = {
    "connection": CONN_STR,
    "pool_size": 3,
    "pool_recycle": 3600,
    "pool_timeout": 5,
    "max_overflow": 5,
    "pool_pre_ping": True
}

LOGURU_CONFIG = {
    "handlers": [
        {
            "sink": sys.stdout,
            "level": logging.INFO,
            "format": "<green>{time:YYYY-MM-DD HH:mm:ss.SSS}</green> | {thread.name} | <level>{level}</level> | "
            "<cyan>{module}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>"
        },
        {
            "sink": "./logs/eagle_api.log",
            "level": logging.INFO,
            "rotation": "10 MB",
            "retention": "1 week",
            "encoding": 'utf-8',
            "format": "{time:YYYY-MM-DD HH:mm:ss.SSS} | {thread.name} | {level} | {module} : {function}:{line} -  {message}"
        },
        {
            "sink": "./logs/eagle_api_error.log",
            "serialize": True,
            "level": logging.ERROR,
            "retention": "1 week",
            "rotation": "10 MB",
            "encoding": 'utf-8',
            "format": "{time:YYYY-MM-DD HH:mm:ss.SSS} | {thread.name} | {level} | {module} : {function}:{line} -  {message}"
        },
    ],
}

CELERY = {
    "timezone": 'Asia/Shanghai',
    "enable_utc": False,
    "worker_concurrency": 8,
    "broker_url": "redis://:ddong.ihasy@eagle_redis/0",
    "result_backend": "redis://:ddong.ihasy@eagle_redis/0",
    "imports": [
        "eagle.workers.stock.tasks"
    ],
    "task_serializer": "json",
    "result_serializer": "json",
    "accept_content": ["json"],
    "worker_prefetch_multiplier": 1,
    "task_routes": {
        "eagle.workers.*": {"queue": "eagle",
                            "exchange": "eagle",
                            "routing_key": "eagle"}
    },
    "beat_schedule": {
        'add-every-30-seconds': {
            'task': 'eagle.workers.stock.tasks.monitor',
            'schedule': 30,
            'args': (16, 16),
        },
        "add-every-workday-afternoon": {
            "task": "eagle.workers.stock.tasks.add",
            "schedule": crontab(hour=18, minute=0, day_of_week='mon,tue,wed,thu,fri'),
            "args": ["id1", 3, 6]
        }
    }
}

CELERY_WORKER = {
    "callback": {
        "strict_client": True,
        "allow_hosts": ["eagle_redis", "eagle_web"]
    }
}

COOKIES = json.load(
    open(os.path.join(os.path.dirname(__file__), 'cookie.json')))
