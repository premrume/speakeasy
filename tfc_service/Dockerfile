FROM python:3.6.1

RUN \
  apt-get update \
  && apt-get install -y --no-install-recommends apt-utils

# Depends on volume (refer to ../docker-compose.yml) /models
LABEL \
      description="Tensorflow Client depends on models volume"

# Speakeasy User and Group:
RUN \
  groupadd -g 1000 flaskgroup \
  && useradd -m -g flaskgroup  -u 1000 -s /bin/bash flask \
  && mkdir -p /var/tfc_server \
  && chown -R flask:flaskgroup /var/tfc_server \
  && pip install --upgrade pip 

USER flask

# And then...
RUN \ 
  pip3 install --user nltk \
  && python3 -m nltk.downloader popular

# Takes a long time, separated from requirements.txt
WORKDIR /var/tfc_server
COPY . /var/tfc_server

ENV PATH "$PATH:/home/flask/.local/bin"
RUN pip3 install --user --no-cache-dir -r requirements.txt

ENTRYPOINT ["python"]
CMD ["app.py"]
