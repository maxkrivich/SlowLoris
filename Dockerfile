# I'm not sure what it is right

MAINTAINER Max Krivich (maxkrivich@gmail.com)

FROM ubuntu:14.04

RUN \
  apt-get update && \
  apt-get -y upgrade && \
  apt-get install -y python python-pip python-dev

#RUN pip install SlowLoris

ADD . /app

WORKDIR /app

RUN python setup.py install

#CMD with args from docker run