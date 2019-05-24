#!/bin/bash

set -o nounset
set -o errexit

# Backup settings
SUFFIX=$(date '+%Y-%m-%d-%H-%M-%S')
BACKUP_DIR='backups'

# Backup files
DOCKER_MEDIA_SERVICE='lis_media'
MEDIA_ARCHIVE="$BACKUP_DIR/media_$SUFFIX.tgz"

echo "Archiving media files to $MEDIA_ARCHIVE..."
docker exec -i \
    $(docker ps --filter name=$DOCKER_MEDIA_SERVICE --format "{{.ID}}") \
    sh -c "cd /usr/share/nginx/html/media && tar --exclude ./images -cf - ." > $MEDIA_ARCHIVE

# Backup and restore database locally
DUMP_FILE="$BACKUP_DIR/dump_$SUFFIX.sql"
POSTGRES_DB='django'
POSTGRES_USER='django'
DOCKER_DB_SERVICE='lis_db'
DOCKER_DB_CONTAINER=$(docker ps --filter name=$DOCKER_DB_SERVICE --format "{{.ID}}")

DOCKER_DJANGO_SERVICE='lis_django'
DOCKER_DB_CONTAINER=$(docker ps --filter name=$DOCKER_DJANGO_SERVICE --format "{{.ID}}")

echo "Pruning renditions..."
docker exec -i -u postgres $DOCKER_DB_CONTAINER \
    /venv/bin/python manage.py prunerenditions

echo "Dumping database to $DUMP_FILE"
touch $DUMP_FILE
docker exec -i -u postgres $DOCKER_DB_CONTAINER \
    pg_dump -Fc -U $POSTGRES_USER -d $POSTGRES_DB > "$DUMP_FILE"
