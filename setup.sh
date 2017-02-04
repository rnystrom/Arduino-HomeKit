#!/bin/bash

# Install python dev environment to build c libs
echo "Install python-dev as sudo..."
sudo apt-get install python-dev

# Globally install python and node env to keep all changes local
echo "Install virtualenv and nodeenv as sudo..."
sudo pip install virtualenv nodeenv

echo "Installing python dependencies..."
virtualenv venv
. venv/bin/activate
pip install Flask Naked psutil paho-mqtt

echo "Installing node dependencies..."
nodeenv nenv
. nenv/bin/activate
cd hap && npm install
npm install sync-request

echo "Exiting environments..."
deactivate
cd ..
echo "done"