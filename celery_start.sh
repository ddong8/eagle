#!/bin/bash
cd /code
mkdir -p log
chmod -R 777 log
# Start Celery Workers
celery -A celery_worker worker -l info -c 10 -Q eagle &> ./log/celery.log  &

# Start Celery Beat
celery -A celery_worker beat -l info &> ./log/celery_beat.log  &

# Start Flower
celery -A celery_worker flower --address=0.0.0.0 --port=5555 &> ./log/celery_flower.log  &
