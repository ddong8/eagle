#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 5/21/2019 12:05 PM
# @File    : settings.py
# @Author  : donghaixing
# Do have a faith in what you're doing.
# Make your life a story worth telling.

HOST = '127.0.0.1'
PORT = 9000

APP_NAME = 'eagle'

PUBLIC_ENDPOINT = 'http://127.0.0.1:9000'

APPS = [
    'eagle.apps.traffic',
]

CELERY = {
    "timezone": 'Asia/Shanghai',
    "enable_utc": True,
    "worker_concurrency": 8,
    "broker_url": "redis://www.ihasy.com/0",
    "result_backend": "redis://www.ihasy.com/0",
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
    }
}

CELERY_WORKER = {
    "callback": {
        "strict_client": True,
        "allow_hosts": ["www.ihasy.com"]
    }
}
