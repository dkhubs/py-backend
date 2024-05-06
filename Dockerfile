FROM python:3.9
MAINTAINER 'dkhubs@github.com'

COPY . /code

WORKDIR /code/app

RUN ln -sf /usr/share/zoneinfo/Asia/Shanghai /etc/localtime

RUN pip install --upgrade pip && pip install -r ../requirement.txt -i https://pypi.douban.com/simple

EXPOSE 80