FROM ubuntu:xenial

RUN apt-get update
RUN apt-get install -y wget

ADD models/ /models/

VOLUME /var/speakeasy

ADD ./quickstart.sh .

CMD ./quickstart.sh
