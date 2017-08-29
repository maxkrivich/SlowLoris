# Quick tutorial how to build and run docker image
# $ sudo docker build -t pyslowloris .
# $ sudo docker run --rm -it pyslowloris [-h] [-u URL] [-p PORT] [-s SOCKET_COUNT]

FROM ubuntu:14.04

LABEL maintainer="Max Krivich"

RUN \
  apt-get update && \
  apt-get -y upgrade && \
  apt-get install -y python python-pip python-dev

ADD . /app

WORKDIR /app

RUN python setup.py install

ENTRYPOINT ["slowloris"]

CMD ["-h"]
