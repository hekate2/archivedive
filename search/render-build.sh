#!/usr/bin/env bash

# Install Java
apt-get update
apt-get install -y default-jre

# Install Python dependencies
pip install -r server-requirements.txt
