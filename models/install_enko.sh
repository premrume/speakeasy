#!/bin/bash -e

install_enko() {
  # quick check for the folder
  if [ ! -d ${SPEAKEASY_HOME}/models/enko ]
  then
    cd ${SPEAKEASY_HOME}/models
    # origin
    ./mc --config-dir . ls sofwerx/models/enko.tar.gz 
    ./mc --config-dir . cp sofwerx/models/enko.tar.gz .
    tar xf enko.tar.gz
    rm enko.tar.gz
    echo "   enko download complete"
    return 0 
  else
    echo "   skipping download, looks like you already have an enko folder"
    return 0
  fi
}
