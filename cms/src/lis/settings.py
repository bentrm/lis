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

from config.helpers import env

CMS_VERSION = env("CMS_VERSION", default="latest")


# Build paths inside the project like this: os.path.join(SRC_DIR, ...)
APP_DIR = os.path.dirname(os.path.abspath(__file__))
SRC_DIR = os.path.dirname(APP_DIR)
PROJECT_DIR = os.path.dirname(SRC_DIR)


ADMINS = [x.split("=") for x in env("LIS_ADMINS", "").split(";")]
MANAGERS = [x.split("=") for x in env("LIS_MANAGERS", "").split(";")]

DEFAULT_FROM_EMAIL = env("DEFAULT_FROM_EMAIL", "postmaster@localhost")
SERVER_EMAIL = env("DEFAULT_FROM_EMAIL", "postmaster@localhost")
EMAIL_BACKEND = env("EMAIL_BACKEND", "django.core.mail.backends.console.EmailBackend")
EMAIL_HOST = env("EMAIL_HOST")
EMAIL_PORT = int(env("EMAIL_PORT", 587))
EMAIL_HOST_USER = env("EMAIL_HOST_USER")
EMAIL_HOST_PASSWORD = env("EMAIL_HOST_PASSWORD")
EMAIL_USE_TLS = env("EMAIL_USE_TLS", True, parse_to_bool=True)
EMAIL_USE_SSL = env("EMAIL_USE_SSL", True, parse_to_bool=True)

EMAIL_SUBJECT_PREFIX = "[LIS] "

# SECURITY WARNING: don't run with debug turned on in production!
ALLOWED_HOSTS = env("VIRTUAL_HOST", "localhost").split(",")
DEBUG = env("DEBUG", False, parse_to_bool=True)
INTERNAL_IPS = ["127.0.0.1", "localhost"]

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = env("SECRET_KEY", required=True)

if env("USE_SSL", True, parse_to_bool=True):
    SECURE_CONTENT_TYPE_NOSNIFF = True
    SECURE_BROWSER_XSS_FILTER = True
    SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
    SECURE_SSL_REDIRECT = True
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True
    X_FRAME_OPTIONS = "DENY"

# Application definition

INSTALLED_APPS = [
    "api",
    "cms",
    "dal",
    "dal_select2",
    "wagtail.api.v2",
    "wagtail.contrib.modeladmin",
    "wagtail.contrib.forms",
    "wagtail.contrib.redirects",
    "wagtail.contrib.postgres_search",
    "wagtail.contrib.routable_page",
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
    "rest_framework",
    "rest_framework_gis",
    "corsheaders",
    "django_filters",
    "debug_toolbar",
    "django.contrib.gis",
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
]

MIDDLEWARE = [
    "corsheaders.middleware.CorsMiddleware",
    "debug_toolbar.middleware.DebugToolbarMiddleware",
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
        "DIRS": [os.path.join(SRC_DIR, "templates")],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                "cms.context_processors.app_status",
            ]
        },
    }
]

WSGI_APPLICATION = "lis.wsgi.application"


# Database
# https://docs.djangoproject.com/en/1.11/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": env("DB_ENGINE", "django.db.backends.postgresql"),
        "NAME": env("DB_NAME", required=True),
        "USER": env("DB_USER", required=True),
        "PASSWORD": env("DB_PASSWORD", required=True),
        "HOST": env("DB_HOST", required=True),
        "PORT": env("DB_PORT", "5432"),
        "CONN_MAX_AGE": 360,
    }
}

# Caching
CACHE_MIDDLEWARE_ALIAS = "default"
CACHE_MIDDLEWARE_SECONDS = 60
CACHE_MIDDLEWARE_KEY_PREFIX = ""
if DEBUG:
    CACHES = {
        "default": {
            "BACKEND": "django.core.cache.backends.dummy.DummyCache",
        }
    }
else:
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
        "verbose": {"format": "%(levelname)s %(asctime)s %(module)s %(message)s"}
    },
    "handlers": {
        "console": {
            "level": "INFO",
            "class": "logging.StreamHandler",
            "formatter": "verbose",
        }
    },
    "loggers": {"django": {"handlers": ["console"], "propagate": True}},
}


# Internationalization
# https://docs.djangoproject.com/en/1.11/topics/i18n/

LANGUAGE_CODE = "de-de"
LANGUAGES = [("en", "English"), ("de", "Deutsch"), ("cs", "český")]

TIME_ZONE = "Europe/Berlin"

USE_I18N = True

USE_L10N = True

USE_TZ = True

LOCALE_PATHS = [os.path.join(SRC_DIR, "locale")]

STATICFILES_DIRS = [
    os.path.join(SRC_DIR, "static"),
    "/assets"
]

STATIC_ROOT = "/html/static"
STATIC_URL = env("STATIC_URL", "/static/")

MEDIA_ROOT = "/html/media"
MEDIA_URL = env("MEDIA_URL", "/media/")

# Wagtail settings
WAGTAIL_ENABLE_UPDATE_CHECK = False
WAGTAIL_SITE_NAME = "LIS"
WAGTAILIMAGES_IMAGE_MODEL = "cms.ImageMedia"
WAGTAILDOCS_DOCUMENT_MODEL = "cms.DocumentMedia"
WAGTAIL_USAGE_COUNT_ENABLED = False
WAGTAILADMIN_PERMITTED_LANGUAGES = LANGUAGES
WAGTAIL_FRONTEND_LOGIN_URL = "/accounts/login/"
WAGTAIL_GRAVATAR_PROVIDER_URL = None
WAGTAILSEARCH_BACKENDS = {
    "default": {
        "BACKEND": "wagtail.contrib.postgres_search.backend",
        'SEARCH_CONFIG': 'english',
    },
    "german": {
        "BACKEND": "wagtail.contrib.postgres_search.backend",
        'SEARCH_CONFIG': 'german',
    }
}
WAGTAILAPI_LIMIT_MAX = None

# Map widgets
MAP_WIDGETS = {
    "GooglePointFieldWidget": (
        ("zoom", 15),
        ("mapCenterLocationName", "Dresden"),
        ("markerFitZoom", 12),
    ),
    "GOOGLE_MAP_API_KEY": env("GOOGLE_MAP_API_KEY", required=True),
}

# Base URL to use when referring to full URLs within the Wagtail admin backend -
# e.g. in notification emails. Don't include "/admin" or a trailing slash
BASE_URL = env("LIS_BASE_URL", "http://localhost:8000")

# API settings
REST_FRAMEWORK = {
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.LimitOffsetPagination',
    'PAGE_SIZE': 100
}

# Application Settings
LIS_SIGNUP_KEYWORD = env("LIS_SIGNUP_KEYWORD", required=True)

# CORS configuration
CORS_ORIGIN_REGEX_WHITELIST = [
    r"^http://localhost(:[0-9]{2,6})?",
    r"^http://141.56.[0-9]{1,3}\.[0-9]{1,3}(:[0-9]{2,6})?$"
]
CORS_URLS_REGEX = r'^/api/.*$'
CORS_ALLOW_METHODS = [
    'GET',
    'OPTIONS',
    'POST',
]
