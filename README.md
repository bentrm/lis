# Run application as Docker stack in production

In production a Nginx proxy server and a Let's Encrypt companien container is needed to negotiate SSL encryption.

See the `docker-stack.yml` file which env vars will be set.

## Environment

The following env vars are needed and need to be substituted with your production settings.

````bash
export LIS_DB_NAME='@NAME'
export LIS_DB_PASSWORD='@PASSWORD'
export LIS_DB_PORT='@PORT'
export LIS_DB_USER='@USER'
export LIS_EMAIL_FROM='@EMAIL'
export LIS_EMAIL_HOST_PASSWORD='@PASSWORD'
export LIS_EMAIL_HOST_USER='@HOST_USER'
export LIS_EMAIL_HOST='@HOST'
export LIS_GOOGLE_MAP_API_KEY='@KEY'
export LIS_LETSENCRYPT_EMAIL='@EMAIL'
export LIS_MEDIA_PATH='@PATH'
export LIS_SECRET_KEY='@KEY'
export LIS_STATIC_PATH='@PATH'
export LIS_VERSION='@VERSION'
export LIS_VIRTUAL_HOST='@HOST'
export LIS_VIRTUAL_PATH='@PATH'
export LIS_ADMINS="@Name=@Email;@Name=@Email"
export LIS_MANAGERS="@Name=@Email;@Name=@Email"
````

## Command

The following command sources the environment vars from the file prod.env and inits the docker stack.

````bash
source prod.env && docker stack deploy --prune -c docker-stack.yml lis
````
