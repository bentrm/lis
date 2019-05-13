#!/bin/sh
set -e

if [[ "$1" = 'gunicorn' ]]; then

    chown -R gunicorn "$MEDIA_ROOT"
    chmod 775 "$MEDIA_ROOT"

    # init Django app
    /venv/bin/python manage.py migrate
    /venv/bin/python manage.py collectstatic --no-input
    /venv/bin/python manage.py prunerenditions

    # init Cron scripts purging sessions
    crond -bS

    # run app as user gunicorn
    su-exec gunicorn /venv/bin/gunicorn -c python:config.gunicorn lis.wsgi:application
fi

exec "$@"
