FROM python:3.8

WORKDIR /opt

COPY ./requirements.txt ./requirements.txt

RUN pip install -r requirements.txt -i https://mirrors.aliyun.com/pypi/simple

COPY . .
