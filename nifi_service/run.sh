#!/bin/bash -e
gunzip /opt/nifi/nifi-current/conf/flow.xml.gz
sed -i -e "s%mongodb://speakeasy:Speakeasy123@mongo:27017%${MONGO_CONNECT}%" /opt/nifi/nifi-current/conf/flow.xml
gzip /opt/nifi/nifi-current/conf/flow.xml
. ../scripts/start.sh
