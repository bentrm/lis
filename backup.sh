#!/bin/bash

set -o nounset
set -o errexit

# Docker Host settings
DOCKER_MEDIA_VOLUME='lis_media'

DOCKER_DB_SERVICE='lis_db'
POSTGRES_DB='django'

# Backup settings
SUFFIX=$(date '+%Y-%m-%d-%H-%M-%S')
BACKUP_DIR='backups'
MEDIA_ARCHIVE="$BACKUP_DIR/media_$SUFFIX.tgz"
DUMP_FILE="$BACKUP_DIR/dump_$SUFFIX.sql"

# Local Docker settings
MEDIA_ROOT='files/media'

# Backup files
docker run --rm --volume "$DOCKER_MEDIA_VOLUME:/backup" busybox sh -c 'tar c -vOz -f - -C /backup --exclude ./images ./' > "$MEDIA_ARCHIVE"

# Backup and restore database locally
echo "Dumping database to $DUMP_FILE"
touch $DUMP_FILE
docker exec -it -u postgres \
    $(docker ps --filter name=$DOCKER_DB_SERVICE --format "{{.ID}}") \
    pg_dump --clean --if-exists -d $POSTGRES_DB > "$DUMP_FILE"
