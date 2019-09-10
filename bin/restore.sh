#!/bin/bash

set -o nounset
set -o errexit

while IFS= read -r line
do
  IFS='=' read -r temp val <<< "$line"
  printf -v $temp "$val"
  export $temp
done < "$1"

# Backup settings
BACKUP_DIR=$(realpath 'backups')

# Restore database
DUMP_FILE=$(ls -t $BACKUP_DIR/dump_* | head -1)
POSTGRES_DB=$DB_NAME
POSTGRES_USER=$DB_USER
DOCKER_DB_CONTAINER=$(docker-compose ps -q db)

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
DOCKER_APP_CONTAINER=$(docker-compose ps -q cms)

echo "Copying media archive $MEDIA_ARCHIVE to running container $DOCKER_APP_CONTAINER..."
docker cp $MEDIA_ARCHIVE $DOCKER_APP_CONTAINER:/backup.tgz

echo "Restoring media archive..."
docker exec -i $DOCKER_APP_CONTAINER \
    tar -C /html/media -xvf /backup.tgz

echo "Cleanup..."
docker exec -i $DOCKER_APP_CONTAINER sh -c "rm /backup.tgz"

echo "Pruning renditions..."
docker exec -i $DOCKER_APP_CONTAINER \
    python manage.py prunerenditions
