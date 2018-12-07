FROM tensorflow/serving

# Info
LABEL \
      version="0.1" \
      description="Tensorflow Serving depends on models volume and models.conf"

# Depends on volume (refer to ../docker-compose.yml) /models

# Speakeasy User and Group:
RUN \
  groupadd -g 1000 magpie && \
  useradd -m -g magpie  -u 1000 -s /bin/bash magpie

USER magpie

# Force the entry point with the config file on the mounted drive, does not work as  of 11.0
#ENV MODEL_CONFIG_FILE=/models/models.conf
ENTRYPOINT [ "/usr/bin/tensorflow_model_server",  "--model_config_file=/models/models.conf"]
