#!/bin/bash
cd code
# Start Celery Workers
celery -A celery_worker worker -l info -c 10 -Q eagle &> /var/log/eagle/celery.log  &

# Start Celery Beat
celery -A celery_worker beat -l info -c 10 &> /var/log/eagle/celery_beat.log  &

# Start Flower
celery -A celery_worker flower --address=0.0.0.0 --port=5555 &> /var/log/eagle/celery_flower.log  &
