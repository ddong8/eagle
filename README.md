# eagle
> 基于falcon的RESTful API框架.

## 功能说明
- 支持docker一键部署
- 快速RESTful CRUD API开发
- 异步任务集成[Celery]
- 定时任务集成[Celery]

## celery启动说明
```bash
celery -A celery_worker worker -l info -P eventlet -c 10 -Q eagle
```

## flower启动说明
```bash
celery -A celery_worker flower --port=5555
```