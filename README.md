# **Speakeasy**

## *What is Speakeasy*
> Investment/POC to Translate text files containing Korean Language to English.

> Walk (V1.0)
>> Focus on the data flow

![](slide1.jpg)

## PREREQs on VM (these steps are REQUIRED):
Install tools per your operating system instructions.  (Installation steps are outside the scope of Speakeasy.)

> docker, EG:
```
$ docker --version
Docker version 17.09.1-ce, build 19e2cf6
```
> docker-compose supporting version "3", EG:
```
$ docker-compose version
docker-py version: 3.5.0
CPython version: 3.6.6
OpenSSL version: OpenSSL 1.1.0f  25 May 2017
```

## Dev Steps

1. Clone
```
# Assumption is that you setup your token to clone from BAH...
cd
git clone https://github.boozallencsn.com/tampaml/speakeasy.git --branch V0.7
```

2. Configuration
> If  your .env does not have the right values ... THIS  WILL FAIL!!! Having the correct .env is REQUIRED.
```
# ./models/config.json needs YOUR access keys!
SPEAKEASY_SHARED=/var/speakeasy
SPEAKEASY_VERSION=1.07
SPEAKEASY_MINIO_URL=          GO ASK PEGGY
SPEAKEASY_MINIO_ACCESS_KEY=   GO ASK PEGGY
SPEAKEASY_MINIO_SECRET_KEY=   GO ASK PEGGY
```

3. Build
```
cd speakeasy
make
```

4. UI
* http://localhost:5000
