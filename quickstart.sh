#!/bin/bash

# Assumptions:  
#
# cd
# git clone https://github.boozallencsn.com/tampaml/speakeasy.git --branch V0.3
# cd speakeasy

# volume requirements:

###########################################3
# Define docker-compose variables
echo 'SPEAKEASY_SHARED=/var/speakeasy' >.env
echo 'SPEAKEASY_VERSION=0.4' >>.env

###########################################3
# Need root for the folder create
sudo install -o $USER -g $USER -d /var/speakeasy
###########################################3
# Create sub-folders
mkdir /var/speakeasy/mongodb
mkdir /var/speakeasy/output
mkdir /var/speakeasy/input
mkdir /var/speakeasy/input/ende
mkdir /var/speakeasy/input/kor
mkdir /var/speakeasy/models

# Install models
cp -r ~/speakeasy/models /var/speakeasy/
cd /var/speakeasy/models
./install_ende.sh

# Build and run ...
cd ~/speakeasy
docker-compose build
docker-compose up -d
docker-compose ps
