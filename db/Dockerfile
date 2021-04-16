#docker image of postgres
# VERSION 1.0
# Author: donghaixing

#基础镜像
FROM postgres

#作者
MAINTAINER donghaixing <donghaixing2010@hotmail.com>

#导入数据库
RUN mkdir /db
WORKDIR /db
ADD ./ /db/
RUN chmod -R 777 /db
#RUN < /db/import/ihasy.sql
#RUN < /db/import/ihasy_data.sql

##设置容器启动时执行的命令
#CMD ["mysql", "< /db/import/ihasy.sql"]
EXPOSE 5432
