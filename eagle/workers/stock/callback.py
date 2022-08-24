# -*- coding: utf-8 -*-

from eagle.common import async_helper
# data是强制参数，task_id为url强制参数(如果url没有参数，则函数也无需task_id)


@async_helper.callback('/callback/add/{task_id}')
def callback_add(data, task_id, request=None, response=None):
    # 想要使用db功能，需要修改{$project_name}.server.celery_worker文件的默认项
    # 移除 # base.initialize_db()的注释符号
    # task_db_api().update(task_id, data)
    pass
