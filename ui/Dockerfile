FROM python:3.7-slim

# OS
RUN \
 apt-get update \
 && apt-get install -y --no-install-recommends apt-utils

# Depends on volume (refer to ../docker-compose.yml) /models
LABEL \
 description="UI UI"

#  As ROOT
RUN \
 groupadd flaskgroup \
 && useradd -m -g flaskgroup -s /bin/bash flask \ 
 && mkdir -p /var/ui \
 && chown -R flask:flaskgroup /var/ui \
 && pip install --upgrade pip 

# Install the app as user 
# see .dockerignore
USER flask
WORKDIR /var/ui
COPY . /var/ui

ENV PATH "$PATH:/home/flask/.local/bin"

RUN \ 
  pip install --user --no-cache-dir -r requirements.txt \
  && flask db init \
  && flask db migrate -m "init" \
  && flask db upgrade

#ENTRYPOINT ["python"]
CMD ["python","-u","app.py"]
