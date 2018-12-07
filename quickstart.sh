#!/bin/bash -ex
dir=$(cd -P -- "$(dirname -- "$0")" && pwd -P)
env | grep SPEAKEASY

# Assumptions:  
#
# cd
# git clone https://github.boozallencsn.com/tampaml/speakeasy.git --branch V0.3
# cd speakeasy

# volume requirements:

###########################################3
# Define docker-compose variables
#echo 'SPEAKEASY_SHARED=/var/speakeasy' >.env
#echo 'SPEAKEASY_VERSION=0.4' >>.env

###########################################3
# Need root for the folder create
#sudo install -o $USER -g $USER -d /var/speakeasy
###########################################3
# Create sub-folders
mkdir -p /var/speakeasy/mongodb
mkdir -p /var/speakeasy/output
mkdir -p /var/speakeasy/input
mkdir -p /var/speakeasy/input/ende
mkdir -p /var/speakeasy/input/kor
mkdir -p /var/speakeasy/models

# Install models
cp -r $dir/models /var/speakeasy/
cd /var/speakeasy/models
./install_ende.sh

# Build and run ...
#cd $dir
#docker-compose build
#docker-compose up -d
#docker-compose ps
