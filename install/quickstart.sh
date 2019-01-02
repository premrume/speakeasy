#!/bin/bash -ex
env | grep SPEAKEASY

###########################################
# Create sub-folders
mkdir -p /var/speakeasy/mongodb
mkdir -p /var/speakeasy/output
mkdir -p /var/speakeasy/input
mkdir -p /var/speakeasy/input/ende
mkdir -p /var/speakeasy/input/kor
mkdir -p /var/speakeasy/models

###########################################
# Install models
cp -r /models /var/speakeasy/
cd /var/speakeasy/models
./install_models.sh
