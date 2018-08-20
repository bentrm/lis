#!/bin/sh
set -e

if [ "$1" = 'gunicorn' ]; then

    # init Django app
    /venv/bin/python manage.py migrate
    /venv/bin/python manage.py collectstatic --no-input

    # init Cron scripts purging sessions
    crond -bS

    # run app as user gunicorn
    su-exec gunicorn /venv/bin/gunicorn -c python:config.gunicorn lis.wsgi:application
fi

exec "$@"
