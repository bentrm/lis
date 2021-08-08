# Project structure

* `app` - Frontend Node/Webpack application based on Vue.js
* `backups` - default location for backup files
* `bin` - includes backup and restore scripts
* `cms` - the Django/Wagtail CMS backend
* `static` - http server component to serve static media files

# Run application as a Docker Compose Stack in production

Please be aware, in production proxy server negotiating SSL encryption is needed. 
An example configuration is included in the `docs` directory.

## Environment

The file `.env.example` includes example environmental variables. Copy the file as `.env` as it will
be considered by `docker-compose` during application startup.

# Init application

## 1. Prepare database:
`````
docker-compose -f docker-compose.yml -f docker-compose.dev.yml up db
`````

Wait until database is created and all extensions are installed. Last line should look like:

``````
db_1      | Loading PostGIS extensions into django
db_1      | CREATE EXTENSION

...

PostgreSQL init process complete; ready for start up.
db_1      |
db_1      | 2021-08-07 16:22:57.109 UTC [1] LOG:  starting PostgreSQL 13.3 (Debian 13.3-1.pgdg100+1) on x86_64-pc-linux-gnu, compiled by gcc (Debian 8.3.0-6) 8.3.0, 64-bit
db_1      | 2021-08-07 16:22:57.112 UTC [1] LOG:  listening on IPv4 address "0.0.0.0", port 5432
db_1      | 2021-08-07 16:22:57.112 UTC [1] LOG:  listening on IPv6 address "::", port 5432
db_1      | 2021-08-07 16:22:57.114 UTC [1] LOG:  listening on Unix socket "/var/run/postgresql/.s.PGSQL.5432"
db_1      | 2021-08-07 16:22:57.126 UTC [271] LOG:  database system was shut down at 2021-08-07 16:22:56 UTC
db_1      | 2021-08-07 16:22:57.139 UTC [1] LOG:  database system is ready to accept connections
``````

## 2. IMPORTANT QUICKFIX

Before continuing comment out the following line in cms/src/lis/urls.py 
ONLY during initial setup:

````` python
urlpatterns += i18n_patterns(
    path('api/', include('api.urls')) # <<< bug triggers database queries during migration
)
`````

Revert this change before running the application.

## 3. Run Migrations 

With the database still running, init database schema running Django migrations in a new terminal window:
`````
$ docker-compose -f docker-compose.yml -f docker-compose.dev.yml run cms python manage.py migrate
`````

4. Create superuser 

This user will be the initial superuser to log in to the CMS interface.

`````
$ docker-compose -f docker-compose.yml -f docker-compose.dev.yml run cms python manage.py createsuperuser
`````

5. Init homepage

Connect to the database via psql client:

`````
$ docker-compose -f docker-compose.yml -f docker-compose.dev.yml exec db psql -U django
`````

And run the following commands to update the default Wagtail homepage to be compatible with the LIS schema:
````sql
update wagtailcore_page 
set content_type_id = (
		select id from django_content_type 
		where  app_label = 'cms' and model = 'homepage'
	),
	slug = 'homepage'
where id = 2;

insert into cms_i18npage (page_ptr_id, title_de, title_cs, draft_title_de, draft_title_cs, editor, original_language, temporary_redirect)
values (2, 'Homepage',	'Homepage',	'Homepage',	'Homepage',	'root', 'de', '');

insert into cms__content_pages (i18npage_ptr_id, body, body_de, body_cs)
values (2, '[]', '[]', '[]');

insert into cms_homepage values (2);
`````

Also, there seems to be a bug in django-modelcluster when renaming models that are
linked via ParentalManyToMany fields. Update the reference column manually for now:

`````sql
alter table cms_memorial_site_tag_memorial_type
rename column locationtypetag_id to memorialtag_id;
`````

6. Finish up

Shut down all running stack components and revert the quickfix.
`````
$ docker-compose down
`````

# Running the application stack

Start application for development:
`````
$ docker-compose -f docker-compose.yml -f docker-compose.dev.yml up
`````

Start application for production (creates static build of app component):
`````
$ docker-compose up --build
`````

# Backup & restore

``````
# Backup from running containers
$ bin/backup.sh backups/ .env

# restore (timestamp of backup files in backups/ directory)
# !deletes existing data!
$ bin/restore.sh backups/ 2021-08-07-12-43-43 .env
``````

# Troubleshooting

Prune renditions
`````
$ docker-compose exec cms python manage.py prunerenditions
`````

Fix Wagtail page tree
`````
$ docker-compose exec cms python manage.py fixtree
`````

