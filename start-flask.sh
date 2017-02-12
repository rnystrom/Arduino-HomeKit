#!/bin/bash

# Activate the environments
. venv/bin/activate
. nenv/bin/activate

# Set flask app settings and run
export FLASK_DEBUG=0
export FLASK_APP=app.py
flask run --no-reload --host=0.0.0.0
