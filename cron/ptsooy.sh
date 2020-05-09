#!/bin/sh
set -e

export PIPENV_PIPFILE=/app/Pipfile
cd /
pipenv run /app/ptsooy.py -i /app/subscription_manager.opml
