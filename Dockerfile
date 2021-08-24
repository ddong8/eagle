#docker image of web
# VERSION 1.0
# Author: donghaixing

FROM python:3.7

ENV PYTHONUNBUFFERED 1

RUN mkdir /var/log/eagle
RUN chmod -R 777 /var/log/eagle

ADD ./ /code

WORKDIR /code

RUN pip install -r /code/requirements.txt -i https://mirrors.aliyun.com/pypi/simple/ --trusted-host mirrors.aliyun.com
RUN python -m celery -A celery_worker worker -l info -c 10 -Q eagle
RUN python -m celery -A celery_worker beat -l info -c 10
RUN python -m celery -A celery_worker flower --address=0.0.0.0 --port=5555
CMD ["python", "/code/falcon_server.py"]
