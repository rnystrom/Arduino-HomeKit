#!/bin/bash

echo "Install required build tools and services as sudo..."
sudo apt-get install python-dev

echo "Updating git submodules..."
git submodule update --init --recursive

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
cd ..

echo "Initializing the database"
export FLASK_APP=app.py
flask initdb

echo "Exiting environments..."
deactivate
echo "done"