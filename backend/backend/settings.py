"""
Django settings for backend project.

Generated by 'django-admin startproject' using Django 2.2.6.

For more information on this file, see
https://docs.djangoproject.com/en/2.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.2/ref/settings/
"""

import os
import sys

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


BUSY_UNIT_TESTING = "test" in sys.argv
RUNNING_IN_GAE = bool(os.getenv("GAE_APPLICATION", False))
# BASE_URL = os.getenv("BASE_URL")


err = "Cant run unit tests on GAE cloud"
if BUSY_UNIT_TESTING:
    assert not RUNNING_IN_GAE, err

# if RUNNING_IN_GAE:
#     GAE_SERVICE = os.environ["GAE_SERVICE"]
#     assert not BUSY_UNIT_TESTING, err

#     BASE_URL = {
#         "management-info-sys": "https://management-info-sys-dot-people-portal-staging.appspot.com",
#         "management-info-sys-devtest": "https://management-info-sys-devtest-dot-people-portal-staging.appspot.com",
#     }[GAE_SERVICE]

# else:
BASE_URL = "http://localhost:8000"


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = "*^rt0_72g4%&k(!4+l-hf80$llcs=ry&6&2lck$3z1^cph&+s+"

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True


# CORS

# see here for opitons: https://pypi.org/project/django-cors-headers/

CORS_ORIGIN_ALLOW_ALL = True
# CORS_URLS_REGEX = r"^/api/.*$"  # we should only allow cors on certain url patterns. Feel free to change this if you have APIs elsewhere

try:
    PROD_MODE = int(os.getenv("PROD_MODE", 0))
except ValueError:
    PROD_MODE = 0

if PROD_MODE:
    SECRET_KEY = os.environ["PROD_SECRET_KEY"]
    assert len(SECRET_KEY) >= 50
    DEBUG = False
    # ALLOWED_HOSTS = [
    #     "tilde-dot-umuzi-prod.nw.r.appspot.com",  # prod
    #     "tilde.umuzi.org",
    # ]
    # X_FRAME_OPTIONS = "DENY"
    # CSRF_COOKIE_SECURE = True
    # SESSION_COOKIE_SECURE = True
    # SECURE_SSL_REDIRECT = True
    # SECURE_BROWSER_XSS_FILTER = True
    # SECURE_CONTENT_TYPE_NOSNIFF = True
    # SECURE_HSTS_SECONDS = 30  # TODO 518400
    # SECURE_HSTS_INCLUDE_SUBDOMAINS = True
    # SECURE_HSTS_PRELOAD = True
    # BASE_URL = "tilde-dot-umuzi-prod.nw.r.appspot.com"
else:
    # SECURITY WARNING: keep the secret key used in production secret!
    SECRET_KEY = "n9y0e&ol12u-917hxu=fjs)z_4##+u#q#8%n_%@(81e^s1+gjz"
    # SECURITY WARNING: don't run with debug turned on in production!
    DEBUG = True

    # ALLOWED_HOSTS = [
    #     "127.0.0.1",  # Localhost
    #     # "management-info-sys-devtest-dot-people-portal-staging.appspot.com",  # dev-test environment
    #     # "management-info-sys-dot-people-portal-staging.appspot.com",  # staging environment
    #     "localhost",
    # ]

# PROD_MODE = 0
# DEBUG = True

ALLOWED_HOSTS = ["*"]

# Application definition

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "corsheaders",
    "django.contrib.sites",
    "rest_framework",
    "rest_framework.authtoken",
    "dj_rest_auth",
    "adminsortable2",
    "taggit",
    "django_extensions",
    "django_filters",
    "django_countries",
    "guardian",
    "core.apps.CoreConfig",
    "curriculum_tracking.apps.CurriculumTrackingConfig",
    "git_real.apps.GitRealConfig",
    "social_auth.apps.SocialAuthConfig",
    "dev_helpers.apps.DevHelpersConfig",
    "config.apps.ConfigConfig",
    "activity_log.apps.ActivityLogConfig",
]

SITE_ID = 1  # from allauth docs


MIDDLEWARE = [
    "health_check_middleware.HealthCheckMiddleware",
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "logging_middleware.RequestUserLogMiddleware",
]

ROOT_URLCONF = "backend.urls"

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
                # `allauth` needs this from django
                "django.template.context_processors.request",
            ]
        },
    }
]

WSGI_APPLICATION = "backend.wsgi.application"


# Database
# https://docs.djangoproject.com/en/2.2/ref/settings/#databases


# [START db_setup]
if RUNNING_IN_GAE:
    # Running on production App Engine, so connect to Google Cloud SQL using
    # the unix socket at /cloudsql/<your-cloudsql-connection string>

    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.postgresql_psycopg2",
            "HOST": f'/cloudsql/{os.environ["SQL_CONNECTION_NAME"]}',
            "USER": os.environ["TILDE_SQL_USER"],
            "PASSWORD": os.environ["TILDE_SQL_PASS"],
            "NAME": os.environ["TILDE_SQL_DB"],
        }
    }

else:
    # Running locally so connect to either a local MySQL instance or connect to Cloud SQL via the proxy.
    # look inside the databases directory to see how to launch the database/proxy
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.postgresql_psycopg2",
            "HOST": os.getenv("TILDE_SQL_HOST", "127.0.0.1"),
            "PORT": os.getenv("TILDE_SQL_PORT", 6543),
            "NAME": os.getenv("TILDE_SQL_DB", "db"),
            "USER": os.getenv("TILDE_SQL_USER", "pguser"),
            "PASSWORD": os.getenv("TILDE_SQL_PASS", "password"),
        }
    }
# [END db_setup]

AUTHENTICATION_BACKENDS = (
    # Needed to login by username in Django admin, regardless of `allauth`
    "django.contrib.auth.backends.ModelBackend",
    # `allauth` specific authentication methods, such as login by e-mail
    # "allauth.account.auth_backends.AuthenticationBackend",
    "guardian.backends.ObjectPermissionBackend",
)


# Password validation
# https://docs.djangoproject.com/en/2.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"
    },
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]


# Internationalization
# https://docs.djangoproject.com/en/2.2/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.2/howto/static-files/

STATIC_ROOT = "collectstatic"
STATIC_URL = os.environ.get("STATIC_URL", "/static/")


################################################################################
# File Storage
# we store our uploads in a google cloud buket. Documentation is here: https://django-storages.readthedocs.io/en/latest/backends/gcloud.html

GS_PROJECT_ID = os.environ.get("GAE_PROJECT")
GS_BUCKET_NAME = os.environ.get("GS_BUCKET_NAME")

USE_CLOUD_STORAGE = RUNNING_IN_GAE

if USE_CLOUD_STORAGE:
    if GS_PROJECT_ID and GS_BUCKET_NAME:
        DEFAULT_FILE_STORAGE = "storages.backends.gcloud.GoogleCloudStorage"
        GCS_ROOT = f"https://storage.googleapis.com/{GS_BUCKET_NAME}/"

    if "GOOGLE_APPLICATION_CREDENTIALS" not in os.environ:
        from google.oauth2 import service_account
        from pathlib import Path

        credentials_path = Path(BASE_DIR) / "credentials.json"
        assert (
            credentials_path.exists()
        ), f"{credentials_path} does not exist. Please get a suitable cloud credentials file. or set your GOOGLE_APPLICATION_CREDENTIALS value"
        GS_CREDENTIALS = service_account.Credentials.from_service_account_file(
            credentials_path
        )

    MEDIA_PREFIX = "media"
    MEDIA_URL = f"{GCS_ROOT}{MEDIA_PREFIX}/"

else:
    MEDIA_ROOT = "../gitignore/media/"
    MEDIA_URL = "/media/"

AUTH_USER_MODEL = "core.User"


REST_FRAMEWORK = {
    "DEFAULT_PAGINATION_CLASS": "rest_framework.pagination.LimitOffsetPagination",
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "rest_framework.authentication.TokenAuthentication",
        "rest_framework.authentication.SessionAuthentication",
    ],
    "DEFAULT_FILTER_BACKENDS": [
        "django_filters.rest_framework.DjangoFilterBackend",
        # "filters.OrderingFilter"
        # filters.ObjectPermissionsFilter todo: use this
    ],
    "DEFAULT_RENDERER_CLASSES": (
        "rest_framework.renderers.JSONRenderer",
        "rest_framework.renderers.BrowsableAPIRenderer",
    ),
    "DEFAULT_PERMISSION_CLASSES": [
        "rest_framework.permissions.IsAdminUser",
    ],
    # "DEFAULT_THROTTLE_CLASSES": [
    #     "rest_framework.throttling.AnonRateThrottle",
    #     "rest_framework.throttling.UserRateThrottle",
    # ],
}


LOGGING = {  # TODO: copy this back into template project
    "version": 1,
    # "disable_existing_loggers": True,
    "formatters": {
        "standard": {
            "format": "[Tilde-backend] [%(asctime)s] %(levelname)s [%(name)s:%(lineno)s] %(message)s",
            # "format": "[Tilde-backend] [%(asctime)s] %(levelname)s [%(name)s:%(lineno)s] %(message)s",
            "datefmt": "%d/%b/%Y %H:%M:%S",
        }
    },
    "handlers": {
        "console": {
            "formatter": "standard",
            "class": "logging.StreamHandler",
            "level": "INFO",
        },
    },
    "root": {
        "handlers": [
            "console",
        ],
        "level": "INFO",
        "propagate": True,
    },
    "loggers": {
        "django": {
            "handlers": [
                "console",
            ],
            "level": "INFO",
            "propagate": False,
        },
        # "django.server": {
        #     "handlers": ["console"],
        #     "level": "INFO",
        #     "propagate": False,
        # },
    },
}

ROCKETCHAT = {
    "BASE_URL": os.environ.get("ROCKETCHAT_BASE_URL"),
    # "USER": os.environ.get("ROCKETCHAT_EMAIL"),
    # "PASS": os.environ.get("ROCKETCHAT_PASSWORD"),
}


RABBITMQ_USER = os.environ.get("RABBITMQ_USER", "rabbituser")
RABBITMQ_HOST = os.environ.get("RABBITMQ_HOST", "localhost")
RABBITMQ_PASSWORD = os.environ.get("RABBITMQ_PASSWORD", "password")
RABBITMQ_PORT = os.environ.get("RABBITMQ_PORT", "5672")

GIT_REAL_BOT_USERNAME = os.environ.get("GIT_REAL_BOT_USERNAME", "umuzibot")
GIT_REAL_WEBHOOK_SECRET = os.environ.get("GIT_REAL_WEBHOOK_SECRET")
if not GIT_REAL_WEBHOOK_SECRET:
    print("warning: GIT_REAL_WEBHOOK_SECRET not set!")


CURRICULUM_TRACKING_REVIEW_BOT_EMAIL = "reviewbot@noreply.org"
CURRICULUM_TRACKING_TRUST_STREAK_LENGTH = 4
