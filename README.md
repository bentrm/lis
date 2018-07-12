# Run application as Docker stack in production

In production a Nginx proxy server and a Let's Encrypt companien container is needed to negotiate SSL encryption.

See the `docker-stack.yml` file which env vars will be set.

## Environment

The following env vars are needed and need to be substituted with your production settings.

````bash
LIS_DB_NAME='@NAME'
LIS_DB_PASSWORD='@PASSWORD'
LIS_DB_PORT='@PORT'
LIS_DB_USER='@USER'
LIS_EMAIL_FROM='@EMAIL'
LIS_EMAIL_HOST_PASSWORD='@PASSWORD'
LIS_EMAIL_HOST_USER='@HOST_USER'
LIS_EMAIL_HOST='@HOST'
LIS_GOOGLE_MAP_API_KEY='@KEY'
LIS_LETSENCRYPT_EMAIL='@EMAIL'
LIS_MEDIA_PATH='@PATH'
LIS_SECRET_KEY='@KEY'
LIS_STATIC_PATH='@PATH'
LIS_VERSION='@VERSION'
LIS_VIRTUAL_HOST='@HOST'
LIS_VIRTUAL_PATH='@PATH'
````

## Command

The following command sources the environment vars from the file prod.env and inits the docker stack.

````bash
export $(cat prod.env | xargs) && docker stack deploy --prune -c docker-stack.yml lis
````
