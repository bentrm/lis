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
SUFFIX=$(date '+%Y-%m-%d-%H-%M-%S')
BACKUP_DIR='backups'
DUMP_FILE="$BACKUP_DIR/dump_$SUFFIX.sql"
MEDIA_ARCHIVE="$BACKUP_DIR/media_$SUFFIX.tgz"

# Backup files
DOCKER_STATIC_CONTAINER=$(docker-compose ps -q static)

echo "Archiving media files to $MEDIA_ARCHIVE..."
docker exec -i $DOCKER_STATIC_CONTAINER \
    sh -c "cd /usr/share/nginx/html/media && tar --exclude ./images -cf - ." > $MEDIA_ARCHIVE

echo "Pruning renditions..."
DOCKER_CMS_CONTAINER=$(docker-compose ps -q cms)
docker exec -i $DOCKER_CMS_CONTAINER \
    python manage.py prunerenditions


echo "Dumping database to $DUMP_FILE"
POSTGRES_DB=$DB_NAME
POSTGRES_USER=$DB_USER
DOCKER_DB_CONTAINER=$(docker-compose ps -q db)
touch $DUMP_FILE
docker exec -i $DOCKER_DB_CONTAINER \
    pg_dump -Fc -U $POSTGRES_USER -d $POSTGRES_DB > "$DUMP_FILE"
