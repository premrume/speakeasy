#!/bin/bash

echo "...Get the ende model from amazon and rename it"

# quick check for the folder
if [ ! -d /var/speakeasy/models/ende ]
then
  cd /var/speakeasy/models
  wget https://s3.amazonaws.com/opennmt-models/averaged-ende-export500k.tar.gz
  tar xf averaged-ende-export500k.tar.gz
  mv averaged-ende-export500k ende
  rm averaged-ende-export500k.tar.gz
else
  echo "   skipping download, looks like you already have an ende folder"
fi
