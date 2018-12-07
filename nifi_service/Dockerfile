FROM apache/nifi:latest

# Depends on volume (refer to ../docker-compose.yml) /models
LABEL \
      version="0.1" \
      description="Simple NIFI flow"

COPY --chown=nifi:nifi flow.xml.gz /opt/nifi/nifi-current/conf/
COPY --chown=nifi:nifi ./nar/*  /opt/nifi/nifi-current/lib/
COPY --chown=nifi:nifi ./nifi-env.sh  /opt/nifi/nifi-current/bin/
COPY --chown=nifi:nifi ./bootstrap.conf  /opt/nifi/nifi-current/conf/
