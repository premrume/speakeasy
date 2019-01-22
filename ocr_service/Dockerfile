FROM python:3.7-slim

ENV PYTHONUNBUFFERED=1
ENV LC_ALL=C.UTF-8
ENV LANG=C.UTF-8

RUN apt-get update \
    && apt install -y tesseract-ocr \
    && apt install libtesseract-dev \
    && apt-get install tesseract-ocr-kor \
    && apt-get install libsm6 libxrender1 libfontconfig1 \
    && rm -rf /var/lib/apt/lists/* \
    && pip install --upgrade pip

# Depends on ...
LABEL \
      description="Very limited OCR"

# Speakeasy User and Group:
RUN \
  groupadd -g 1000 flaskgroup && \
  useradd -m -g flaskgroup  -u 1000 -s /bin/bash flask

USER flask

WORKDIR /var/ocr
COPY . /var/ocr
ENV PATH "$PATH:/home/flask/.local/bin"
RUN pip install --user -r requirements.txt

ENTRYPOINT ["python"]
CMD ["app.py"]
