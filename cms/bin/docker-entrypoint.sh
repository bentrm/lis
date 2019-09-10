#!/bin/bash
set -e

if [[ "$1" = 'gunicorn' ]]; then
    chown -R gunicorn "$MEDIA_ROOT"
    chmod 775 "$MEDIA_ROOT"

    # init Django app
    python manage.py migrate
    python manage.py collectstatic --no-input
    python manage.py update_index

    # run app as user gunicorn
    exec gosu gunicorn "$@"
fi

exec "$@"
