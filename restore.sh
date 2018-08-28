#!/bin/bash

set -o nounset
set -o errexit

# Unset to activate local docker host
eval $(docker-machine env -u)

# Backup settings
BACKUP_DIR=$(realpath 'backups')
DUMP_FILE=$(ls -t $BACKUP_DIR/dump_* | head -1)
MEDIA_ARCHIVE=$(ls -t $BACKUP_DIR/media_* | head -1)

# Local docker settings
DOCKER_DB_VOLUME='lis_pgdata'
DOCKER_MEDIA_VOLUME='lis_media'
POSTGRES_IMAGE='mdillon/postgis:10-alpine'
POSTGRES_USER='django'
POSTGRES_DB='django'
DB_RESTORE_CONTAINER_NAME='backup-lis'
MEDIA_ROOT='files/media'

if [[ $(docker ps -a --filter volume=$DOCKER_DB_VOLUME --format "{{.ID}}") ]]; then
    echo "Volume $DOCKER_DB_VOLUME is in use."  1>&2
    exit 1
fi

# Restore database
docker run --rm -d --name $DB_RESTORE_CONTAINER_NAME \
    --volume "$DUMP_FILE:/dump.sql" \
    --volume "$DOCKER_DB_VOLUME:/var/lib/postgresql/data" \
    -e POSTGRES_USER=$POSTGRES_USER \
    -e PGDATA=/var/lib/postgresql/data/pgdata \
    $POSTGRES_IMAGE
sleep 3  # Wait for database
docker exec -it $DB_RESTORE_CONTAINER_NAME \
    psql -U $POSTGRES_USER -d postgres \
    -c "SELECT pg_terminate_backend(pid) FROM pg_stat_activity WHERE datname = '$POSTGRES_DB' AND pid <> pg_backend_pid();"
docker exec -it $DB_RESTORE_CONTAINER_NAME \
    psql -U $POSTGRES_USER -d postgres \
    -c "DROP DATABASE $POSTGRES_DB;"
docker exec -it $DB_RESTORE_CONTAINER_NAME \
    psql -U $POSTGRES_USER -d postgres \
    -c "CREATE DATABASE $POSTGRES_DB;"
docker exec -it $DB_RESTORE_CONTAINER_NAME \
    psql -U $POSTGRES_USER -d $POSTGRES_DB -f /dump.sql
docker stop $DB_RESTORE_CONTAINER_NAME

# Restore media files
tar -xvf $MEDIA_ARCHIVE -C $MEDIA_ROOT
