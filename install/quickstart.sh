#!/bin/bash -e

###########################################
# Create sub-folders
mkdir -p /var/speakeasy/mongodb
mkdir -p /var/speakeasy/output
mkdir -p /var/speakeasy/input
mkdir -p /var/speakeasy/input/ende
mkdir -p /var/speakeasy/input/kor
mkdir -p /var/speakeasy/input/enko
mkdir -p /var/speakeasy/models

###########################################
# Install models
cp -r /models /var/speakeasy/
cd /var/speakeasy/models

if [ -n "${SPEAKEASY_MINIO_URL}" ]; then
  cat <<EOF > config.json
{
	"version": "9",
	"hosts": {
		"sofwerx": {
			"url": "${SPEAKEASY_MINIO_URL}",
			"accessKey": "${SPEAKEASY_MINIO_ACCESS_KEY}",
			"secretKey": "${SPEAKEASY_MINIO_SECRET_KEY}",
			"api": "S3v2",
			"lookup": "auto"
		}
	}
}
EOF
fi

./install_models.sh
