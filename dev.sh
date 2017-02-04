#!/bin/bash

# Activate the environments
. venv/bin/activate
. nenv/bin/activate

# Set flask app settings
export FLASK_DEBUG=1
export FLASK_APP=app.py