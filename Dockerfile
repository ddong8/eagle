#docker image of web
# VERSION 1.0
# Author: donghaixing

FROM python:3.7

ENV PYTHONUNBUFFERED 1

RUN mkdir /var/log/eagle
RUN chmod -R 777 /var/log/eagle

WORKDIR /code/server

ADD ./eagle/server /code/server

RUN pip install -r requirements.txt -i https://mirrors.aliyun.com/pypi/simple/ --trusted-host mirrors.aliyun.com
CMD ["python", "simple_server.py"]
