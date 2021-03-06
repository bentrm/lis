#!/bin/bash

set -o nounset
set -o errexit

if [ $# -lt 3 ]; then
  echo 1>&2 "$0: not enough arguments"
  echo 1>&2 "usage: $0 path timestamp env"
  exit 2
elif [ $# -gt 3 ]; then
  echo 1>&2 "$0: too many arguments"
  echo 1>&2 "usage: $0 path timestamp env"
  exit 2
fi

# Backup settings, defaults to newest files
BACKUP_DIR="$1"
TIMESTAMP="$2"
ENV_FILE="$3"
DUMP_FILE="$BACKUP_DIR"dump_"$TIMESTAMP".sql
MEDIA_ARCHIVE="$BACKUP_DIR"media_"$TIMESTAMP".tgz

while IFS= read -r line
do
  IFS='=' read -r temp val <<< "$line"
  printf -v $temp "$val"
  export $temp
done < "$ENV_FILE"

# Restore database
POSTGRES_DB=$DB_NAME
POSTGRES_USER=$DB_USER
DOCKER_DB_CONTAINER=$(docker ps -q -f LABEL=com.docker.compose.project=lis -f LABEL=com.docker.compose.service=db)

echo 'Terminating all connections...'
docker exec -i -u postgres "$DOCKER_DB_CONTAINER" \
    psql -U "$POSTGRES_USER" -d postgres \
        -c "SELECT pg_terminate_backend(pid) FROM pg_stat_activity WHERE datname = '$POSTGRES_DB' AND pid <> pg_backend_pid();"

echo 'Dropping existing database...'
docker exec -i "$DOCKER_DB_CONTAINER" \
    dropdb --if-exists -U "$POSTGRES_USER" "$POSTGRES_DB"

echo "Restoring database from $DUMP_FILE..."
docker exec -i "$DOCKER_DB_CONTAINER" \
    pg_restore --create --no-owner -U "$POSTGRES_USER" -d postgres < "$DUMP_FILE"

# Restore media files
DOCKER_APP_CONTAINER=$(docker ps -q -f LABEL=com.docker.compose.project=lis -f LABEL=com.docker.compose.service=cms)

echo "Copying media archive $MEDIA_ARCHIVE to running container $DOCKER_APP_CONTAINER..."
docker cp "$MEDIA_ARCHIVE" "$DOCKER_APP_CONTAINER":/backup.tgz

echo "Restoring media archive..."
docker exec -i "$DOCKER_APP_CONTAINER" \
    tar -C /html/media -xvf /backup.tgz

echo "Cleanup..."
docker exec -i "$DOCKER_APP_CONTAINER" sh -c "rm /backup.tgz"

echo "Pruning renditions..."
docker exec -i "$DOCKER_APP_CONTAINER" \
    python manage.py prunerenditions
