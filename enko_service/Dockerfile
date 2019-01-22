FROM python:3.6.1

RUN \
  apt-get update \
  && apt-get install -y --no-install-recommends apt-utils

# Depends on volume (refer to ../docker-compose.yml) /models
LABEL \
      description="ENKO service depends on models volume"

# Speakeasy User and Group:
RUN \
  groupadd -g 1000 flaskgroup \
  && useradd -m -g flaskgroup  -u 1000 -s /bin/bash flask \
  && mkdir -p /var/enko_server \
  && chown -R flask:flaskgroup /var/enko_server \
  && pip install --upgrade pip 

USER flask

# Takes a long time, separated from requirements.txt
WORKDIR /var/enko_server
COPY . /var/enko_server

ENV PATH "$PATH:/home/flask/.local/bin"
RUN pip3 install --user --no-cache-dir -r requirements.txt

ENTRYPOINT ["python"]
CMD ["app.py"]
