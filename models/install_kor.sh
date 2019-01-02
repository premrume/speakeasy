#!/bin/bash

install_kor() {
  # quick check for the folder
  if [ ! -d ${SPEAKEASY_HOME}/models/kor ]
  then
    cd ${SPEAKEASY_HOME}/models
    ./mc --config-dir . ls sofwerx/models/kor.tar.gz 
    ./mc --config-dir . cp sofwerx/models/kor.tar.gz .
    tar xf kor.tar.gz
    rm kor.tar.gz
    echo "   kor download complete"
    return 0 
  else
    echo "   skipping download, looks like you already have an kor folder"
    return 99 
  fi
}
