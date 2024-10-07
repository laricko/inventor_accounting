from datetime import timedelta

import environ
import sentry_sdk
from sentry_sdk.integrations.django import DjangoIntegration

settings_dir = environ.Path(__file__) - 1  # Cut off current file name
root = environ.Path(__file__) - 3  # Directory where "src" sub-directory is located
env = environ.Env(
    DEBUG=(bool, False),
)

ENV_FILE = env("ENV_FILE", default=None) or ".env"

environ.Env.read_env(env_file=settings_dir(ENV_FILE))  # reading .env file

SITE_ROOT = root()

DEBUG = env("DEBUG")

CI = env("CI", cast=bool, default=False)

SECRET_KEY = env("SECRET_KEY")

TIME_ZONE = env("TIME_ZONE")

SENTRY_DSN = env("SENTRY_DSN", default=None)

if SENTRY_DSN is not None:
    sentry_sdk.init(
        dsn=SENTRY_DSN,
        integrations=[DjangoIntegration()],
        traces_sample_rate=1.0,
        send_default_pii=True,
    )

ALLOWED_HOSTS = [
    "localhost",
    "127.0.0.1",
]

CORS_ALLOW_CREDENTIALS = True
CORS_ORIGIN_REGEX_WHITELIST = [
    r".*localhost.*",
    r".*127.0.0.1.*",
]

STATIC_URL = env("STATIC_URL")
STATIC_ROOT = env("STATIC_ROOT")

DATABASES = {
    "default": env.db(),  # Raises ImproperlyConfigured exception if DATABASE_URL not in os.environ
}

CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.redis.RedisCache",
        "LOCATION": [
            "redis://0.0.0.0:6379/1"
        ],
    }
}

# Application definition

INSTALLED_APPS = [
    # Django
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    # 3-rd party
    "behaviors.apps.BehaviorsConfig",
    "corsheaders",
    "rest_framework",
    "rest_framework.authtoken",
    # Current project
    "app",
    "inventory",
    "marketplace",
    "warehouse",
    "regions",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "app.middleware.MarketplaceMiddleware",
]

ROOT_URLCONF = "app.urls"
WSGI_APPLICATION = "app.wsgi.application"

LANGUAGE_CODE = "ru"
USE_L10N = True
USE_i18N = True
USE_TZ = True
LOCALE_PATHS = ["_locale"]


TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

# Password validation

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "handlers": {
        "console": {
            "level": "DEBUG",  # Changed from default `INFO` level
            "class": "logging.StreamHandler",
        },
    },
}

STATICFILES_STORAGE = env(
    "STATICFILES_STORAGE",
    default="django.contrib.staticfiles.storage.StaticFilesStorage",
)
DEFAULT_FILE_STORAGE = env(
    "FILE_STORAGE", default="django.core.files.storage.FileSystemStorage"
)

if "swift" in DEFAULT_FILE_STORAGE:
    SWIFT_CONTAINER_NAME = env("SWIFT_CONTAINER_NAME")

if "swift" in STATICFILES_STORAGE:
    SWIFT_STATIC_CONTAINER_NAME = env("SWIFT_STATIC_CONTAINER_NAME")

if "swift" in STATICFILES_STORAGE or "swift" in DEFAULT_FILE_STORAGE:
    SWIFT_AUTH_URL = env("SWIFT_AUTH_URL")
    SWIFT_USERNAME = env("SWIFT_USERNAME")
    SWIFT_PASSWORD = env("SWIFT_PASSWORD")

REST_FRAMEWORK = {
    "DEFAULT_PERMISSION_CLASSES": [
        "rest_framework.permissions.IsAuthenticated",
    ],
    "DEFAULT_FILTER_BACKENDS": [
        "django_filters.rest_framework.DjangoFilterBackend",
    ],
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "rest_framework_simplejwt.authentication.JWTAuthentication",
        "rest_framework.authentication.TokenAuthentication",
        "rest_framework.authentication.SessionAuthentication",
    ],
    "DEFAULT_PAGINATION_CLASS": "app.pagination.AppPageNumberPagination",
    "PAGE_SIZE": 20,
}

SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(minutes=5),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=14),
    "AUTH_HEADER_TYPES": ("JWT",),
}

HEALTH_CHECKS_ERROR_CODE = 503
HEALTH_CHECKS = {
    "postgresql": "django_healthchecks.contrib.check_database",
    "cache": "django_healthchecks.contrib.check_cache_default",
}

CELERY_ALWAYS_EAGER = env("CELERY_ALWAYS_EAGER", cast=bool, default=DEBUG)
CELERY_TIMEZONE = env("TIME_ZONE")
BROKER_URL = env("CELERY_BACKEND")

# Place here any scheduled tasks
CELERYBEAT_SCHEDULE = {}

ITEMS_PER_OWNER_NUMBER = 10

PRODUCTS_AUTOSYNC_ENABLED = env("PRODUCTS_AUTOSYNC_ENABLED", cast=bool, default=True)
