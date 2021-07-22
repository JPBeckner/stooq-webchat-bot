#!/bin/bash

export DISABLE_COLLECTSTATIC=1
export HOST=0.0.0.0
export PORT=8888

export DEBUG=false

python manage.py runserver $HOST:$PORT
