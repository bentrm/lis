"""
Django settings for lis project.

Generated by "django-admin startproject" using Django 1.11.9.

For more information on this file, see
https://docs.djangoproject.com/en/1.11/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.11/ref/settings/
"""

from __future__ import absolute_import, unicode_literals

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os


def env(NAME, default=""):
    """Return env variable or default."""
    return os.environ.get(NAME, default)


CMS_VERSION = env("CMS_VERSION", default="latest")


# Build paths inside the project like this: os.path.join(SRC_DIR, ...)
PROJECT_DIR = os.path.dirname(os.path.abspath(__file__))
SRC_DIR = os.path.dirname(PROJECT_DIR)
BASE_DIR = os.path.dirname(SRC_DIR)


ADMINS = [
    ("***Name***", "***Email***"),
]
MANAGERS = [
    ("***Name***", "***Email***"),
]
DEFAULT_FROM_EMAIL = env("DEFAULT_FROM_EMAIL", "postmaster@localhost")
SERVER_EMAIL = env("DEFAULT_FROM_EMAIL", "postmaster@localhost")
EMAIL_BACKEND = env("EMAIL_BACKEND", "django.core.mail.backends.console.EmailBackend")
EMAIL_HOST = env("EMAIL_HOST")
EMAIL_PORT = int(env("EMAIL_PORT", 587))
EMAIL_HOST_USER = env("EMAIL_HOST_USER")
EMAIL_HOST_PASSWORD = env("EMAIL_HOST_PASSWORD")
EMAIL_USE_TLS = env("EMAIL_USE_TLS", True) in ("True", "true", "t", "1", True)
EMAIL_USE_SSL = env("EMAIL_USE_SSL", True) in ("True", "true", "t", "1", True)

EMAIL_SUBJECT_PREFIX = "[LIS] "

# SECURITY WARNING: don't run with debug turned on in production!
ALLOWED_HOSTS = env("VIRTUAL_HOST", "localhost").split(",")
DEBUG = env("DEBUG", False) in ("True", "true", "t", "1", True)

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = env("SECRET_KEY", "***SECRET***")

if not DEBUG:
    SECURE_CONTENT_TYPE_NOSNIFF = True
    SECURE_BROWSER_XSS_FILTER = True
    SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
    SECURE_SSL_REDIRECT = True
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True
    X_FRAME_OPTIONS = "DENY"

# Application definition

INSTALLED_APPS = [
    "cms",
    "search",
    "wagtail.contrib.forms",
    "wagtail.contrib.redirects",
    "wagtail.embeds",
    "wagtail.sites",
    "wagtail.users",
    "wagtail.snippets",
    "wagtail.documents",
    "wagtail.images",
    "wagtail.search",
    "wagtail.admin",
    "wagtail.core",
    "modelcluster",
    "taggit",
    "mapwidgets",
    "django.contrib.gis",
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
]

MIDDLEWARE = [
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.locale.LocaleMiddleware",
    "django.middleware.cache.UpdateCacheMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.cache.FetchFromCacheMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "django.middleware.security.SecurityMiddleware",
    "wagtail.core.middleware.SiteMiddleware",
    "wagtail.contrib.redirects.middleware.RedirectMiddleware",
]

ROOT_URLCONF = "lis.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [
            os.path.join(SRC_DIR, "templates"),
        ],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                "cms.context_processors.app_versions",
            ],
        },
    },
]

WSGI_APPLICATION = "lis.wsgi.application"


# Database
# https://docs.djangoproject.com/en/1.11/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": env("DB_ENGINE", "django.db.backends.postgresql"),
        "NAME": env("DB_NAME"),
        "USER": env("DB_USER"),
        "PASSWORD": env("DB_PASSWORD"),
        "HOST": env("DB_HOST"),
        "PORT": env("DB_PORT", "5432"),
        "CONN_MAX_AGE": 360,
    },
}

# Caching
CACHE_MIDDLEWARE_ALIAS = "default"
CACHE_MIDDLEWARE_SECONDS = 60
CACHE_MIDDLEWARE_KEY_PREFIX = ""
CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.memcached.MemcachedCache",
        "LOCATION": "cache:11211",
        "TIMEOUT": 60,
    }
}

# Logging
LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "verbose": {
            "format": "%(levelname)s %(asctime)s %(module)s %(message)s"
        }
    },
    "handlers": {
        "console": {
            "level": "INFO",
            "class": "logging.StreamHandler",
            "formatter": "verbose",
        },
    },
    "loggers": {
        "django": {
            "handlers": ["console"],
            "propagate": True,
        },
    },
}


# Internationalization
# https://docs.djangoproject.com/en/1.11/topics/i18n/

LANGUAGE_CODE = "de-de"

TIME_ZONE = "Europe/Berlin"

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.0/howto/static-files/
STATICFILES_DIRS = [
    os.path.join(SRC_DIR, "static"),
]
STATIC_ROOT = env("STATIC_ROOT", os.path.join(BASE_DIR, "static"))
STATIC_URL = env("STATIC_URL", "/static/")

MEDIA_ROOT = env("MEDIA_ROOT", os.path.join(BASE_DIR, "media"))
MEDIA_URL = env("MEDIA_URL", "/media/")

# Wagtail settings
WAGTAIL_SITE_NAME = "lis"
WAGTAILIMAGES_IMAGE_MODEL = "cms.ImageMedia"
WAGTAILDOCS_DOCUMENT_MODEL = "cms.DocumentMedia"
WAGTAIL_USAGE_COUNT_ENABLED = True
LANGUAGES = WAGTAILADMIN_PERMITTED_LANGUAGES = [
    ("en", "English"),
    ("de", "Deutsch"),
    ("cs", "český"),
]
WAGTAILSEARCH_BACKENDS = {
    "default": {
        "BACKEND": "wagtail.search.backends.elasticsearch6",
        "URLS": ["http://elasticsearch:9200"],
    }
}

# Geotools
GDAL_LIBRARY_PATH = env("GDAL_LIBRARY_PATH")
GEOS_LIBRARY_PATH = env("GEOS_LIBRARY_PATH")
SPATIALITE_LIBRARY_PATH = env("SPATIALITE_LIBRARY_PATH")

# Map widgets
MAP_WIDGETS = {
    "GooglePointFieldWidget": (
        ("zoom", 15),
        ("mapCenterLocationName", "Dresden"),
        ("markerFitZoom", 12),
    ),
    "GOOGLE_MAP_API_KEY": env("GOOGLE_MAP_API_KEY")
}

# Base URL to use when referring to full URLs within the Wagtail admin backend -
# e.g. in notification emails. Don"t include "/admin" or a trailing slash
BASE_URL = "https://lis-map.eu"
