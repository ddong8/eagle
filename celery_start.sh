#!/bin/bash
python -m celery -A celery_worker worker -l info -c 10 -Q eagle
python -m celery -A celery_worker beat -l info -c 10
python -m celery -A celery_worker flower --address=0.0.0.0 --port=5555