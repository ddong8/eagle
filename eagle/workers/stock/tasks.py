from eagle.common import celery
from eagle.common import async_helper
from eagle.workers.stock import callback


@celery.app.task
def add(task_id, x, y):
    # task_id, x, y均为函数自定义参数，本次我们需要做回调演示，因此我们需要task_id异步任务id，以及加法的x和y
    result = x + y
    # 这里还可以通知其他附加任务,当需要本次的一些计算结果来启动二次任务时使用
    # 接受参数：task调用函数路径 & 函数命名参数(dict)
    async_helper.send_task('eagle.workers.stock.tasks.other_task', kwargs={
                           'result': result, 'task_id': task_id})
    # send callback的参数必须与callback函数参数匹配(request，response除外)
    # url_base为callback注册的api地址，eg: http://127.0.0.1:9001
    # 仅接受data参数，若有多个参数，可打包为可json序列化的类型
    # task_id为url接受参数(所以函数也必须接受此参数)
    async_helper.send_callback("http://127.0.0.1:9000", callback.callback_add,
                               '',
                               task_id=task_id)
    # 此处是异步回调结果，不需要服务器等待或者轮询，worker会主动发送进度或者结果，可以不return
    # 如果想要使用return方式，则按照正常celery流程编写代码
    return result


@celery.app.task
def other_task(task_id, result):
    # task_id, result均为函数自定义参数，本次我们需要做通知演示，因此我们需要task_id原始异步任务id，以及加法的result
    pass
