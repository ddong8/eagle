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
CMD ["python", "/code/start_up.py"]
