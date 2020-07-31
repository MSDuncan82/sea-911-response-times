#!/bin/bash

## Install aws
curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "/root/awscliv2.zip"
unzip /root/awscliv2.zip
./aws/install --bin-dir /usr/local/bin --install-dir /usr/aws-cli
rm -rf /root/awscliv2.zip

## Set up credentials
python .devcontainer/aws_setup.py