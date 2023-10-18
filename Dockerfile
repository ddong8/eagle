#docker image of web
# VERSION 1.0
# Author: donghaixing

FROM python:3.9

ENV PYTHONUNBUFFERED 1

RUN mkdir /var/log/eagle
RUN chmod -R 777 /var/log/eagle

ADD ./ /code

WORKDIR /code

RUN pip install -r /code/requirements.txt
CMD ["python", "/code/api_server.py"]
