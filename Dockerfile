FROM ubuntu:xenial

RUN apt-get update
RUN apt-get install -y wget

VOLUME /var/speakeasy

ADD ./models/ ./models/
ADD ./install/ .

CMD ./quickstart.sh
