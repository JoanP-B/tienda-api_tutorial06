#!/bin/sh
set -e

export DJANGO_SETTINGS_MODULE="${DJANGO_SETTINGS_MODULE:-config.settings}"

python manage.py migrate --noinput
exec "$@"
