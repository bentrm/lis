#!/bin/bash

set -o nounset
set -o errexit

# Backup settings
SUFFIX=$(date '+%Y-%m-%d-%H-%M-%S')
BACKUP_DIR='backups'

# Backup files
DOCKER_MEDIA_SERVICE='lis_media'
DOCKER_MEDIA_CONTAINER=$(docker ps --filter name=$DOCKER_MEDIA_SERVICE --format "{{.ID}}")
MEDIA_ARCHIVE="$BACKUP_DIR/media_$SUFFIX.tgz"

echo "Archiving media files to $MEDIA_ARCHIVE..."
docker exec -i $DOCKER_MEDIA_CONTAINER \
    sh -c "cd /usr/share/nginx/html/media && tar --exclude ./images -cf - ." > $MEDIA_ARCHIVE

# Backup database
DUMP_FILE="$BACKUP_DIR/dump_$SUFFIX.sql"
POSTGRES_DB=$DB_NAME
POSTGRES_USER=$DB_USER

DOCKER_APP_SERVICE='lis_django'
DOCKER_APP_CONTAINER=$(docker ps --filter name=$DOCKER_APP_SERVICE --format "{{.ID}}")

echo "Pruning renditions..."
docker exec -i -u postgres $DOCKER_APP_CONTAINER \
    /venv/bin/python manage.py prunerenditions

DOCKER_DB_SERVICE='lis_db'
DOCKER_DB_CONTAINER=$(docker ps --filter name=$DOCKER_DB_SERVICE --format "{{.ID}}")

echo "Dumping database to $DUMP_FILE"
touch $DUMP_FILE
docker exec -i $DOCKER_DB_CONTAINER \
    pg_dump -Fc -U $POSTGRES_USER -d $POSTGRES_DB > "$DUMP_FILE"
