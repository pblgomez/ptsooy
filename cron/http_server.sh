#!/bin/sh
set -e

export PIPENV_PIPFILE=/app/Pipfile
cd /
pipenv run /app/http_server.py