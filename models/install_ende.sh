#!/bin/bash -e

install_ende() {
  # quick check for the folder
  if [ ! -d ${SPEAKEASY_HOME}/models/ende ]
  then
    cd ${SPEAKEASY_HOME}/models
    # origin
    # wget -q https://s3.amazonaws.com/opennmt-models/averaged-ende-export500k.tar.gz
    # this requires mc to be installed and the config
    ./mc --config-dir . ls sofwerx/models/averaged-ende-export500k.tar.gz 
    ./mc --config-dir . cp sofwerx/models/averaged-ende-export500k.tar.gz .
    tar xf averaged-ende-export500k.tar.gz
    mv averaged-ende-export500k ende
    rm averaged-ende-export500k.tar.gz
    echo "   ende download complete"
    return 0 
  else
    echo "   skipping download, looks like you already have an ende folder"
    return 0
  fi
}
