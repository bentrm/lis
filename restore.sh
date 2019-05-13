#!/bin/bash

set -o nounset
#set -o errexit

# Backup settings
BACKUP_DIR=$(realpath 'backups')

# Restore database
DUMP_FILE=$(ls -t $BACKUP_DIR/dump_* | head -1)
POSTGRES_USER='django'
POSTGRES_DB='django'
DOCKER_DB_SERVICE='lis_db'
DOCKER_DB_CONTAINER=$(docker ps --filter name=$DOCKER_DB_SERVICE --format "{{.ID}}")

echo 'Terminating all connections...'
docker exec -i -u postgres $DOCKER_DB_CONTAINER \
    psql -U $POSTGRES_USER -d postgres \
        -c "SELECT pg_terminate_backend(pid) FROM pg_stat_activity WHERE datname = '$POSTGRES_DB' AND pid <> pg_backend_pid();"

echo 'Dropping existing database...'
docker exec -i $DOCKER_DB_CONTAINER \
    dropdb --if-exists -U $POSTGRES_USER $POSTGRES_DB

echo "Restoring database from $DUMP_FILE..."
docker exec -i $DOCKER_DB_CONTAINER \
    pg_restore --create --no-owner -U $POSTGRES_USER -d postgres < $DUMP_FILE

# Restore media files
MEDIA_ARCHIVE=$(ls -t $BACKUP_DIR/media_* | head -1)
DOCKER_MEDIA_SERVICE='lis_media'
DOCKER_MEDIA_CONTAINER=$(docker ps --filter name=$DOCKER_MEDIA_SERVICE --format "{{.ID}}")

echo "Copying media archive $MEDIA_ARCHIVE to running container $DOCKER_MEDIA_CONTAINER..."
docker cp $MEDIA_ARCHIVE $DOCKER_MEDIA_CONTAINER:/backup.tgz

echo "Restoring media archive..."
docker exec -i $DOCKER_MEDIA_CONTAINER \
    tar -C /usr/share/nginx/html/media -xvf /backup.tgz

echo "Cleanup..."
docker exec -i $DOCKER_MEDIA_CONTAINER rm /backup.tgz
