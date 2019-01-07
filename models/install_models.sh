#!/bin/bash -e

echo "...Get the ende model from mc and rename it"
echo "...mc depends on ./config.json which has passwords ... "

SPEAKEASY_HOME=/var/speakeasy

# Either put this here or i Docker ....
if [ ! -f mc ]; then
  wget https://dl.minio.io/client/mc/release/linux-amd64/mc
fi
if [ ! -x mc ] ; then
  chmod +x mc
fi
./mc version
./mc --help

. ./install_ende.sh
. ./install_kor.sh

install_ende
if [ ${?} -ne 0 ] 
then
  echo "FAILURE on ende install"
  exit 99
fi

install_kor
if [ ${?} -ne 0 ] 
then
  echo "FAILURE on kor install"
  exit 99
fi
