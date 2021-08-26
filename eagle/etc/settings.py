#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 5/21/2019 12:05 PM
# @File    : settings.py
# @Author  : donghaixing
# Do have a faith in what you're doing.
# Make your life a story worth telling.

from celery.schedules import crontab

HOST = '0.0.0.0'
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
    "broker_url": "redis://eagle_redis/0",
    "result_backend": "redis://eagle_redis/0",
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
        "add-every-workday-afternoon": {
            "task": "eagle.workers.stock.tasks.add",
            "schedule": crontab(hour=18, minute=0, day_of_week='mon,tue,wed,thu,fri'),
            "args": [3, 6]
        }
    }
}

CELERY_WORKER = {
    "callback": {
        "strict_client": True,
        "allow_hosts": ["eagle_redis"]
    }
}
