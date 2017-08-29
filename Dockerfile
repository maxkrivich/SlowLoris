# docker build -t pyslowloris .

FROM ubuntu:14.04

LABEL maintainer="Max Krivich"

RUN \
  apt-get update && \
  apt-get -y upgrade && \
  apt-get install -y python python-pip python-dev

#RUN pip install SlowLoris

ADD . /app

WORKDIR /app

RUN python setup.py install

#EXPOSE 80

ENTRYPOINT ["slowloris"]

CMD ["-h"]