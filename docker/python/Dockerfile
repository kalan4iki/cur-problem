FROM python:latest
MAINTAINER Vadim Kalnini 'kalan4ikiii@gmail.com'

RUN apt update -y && apt install python3 python3-pip build-essential libssl-dev libffi-dev python3-dev -y

COPY ./mcur /srv/www/mcur
WORKDIR /srv/www/mcur

RUN pip install -r Requirements.txt