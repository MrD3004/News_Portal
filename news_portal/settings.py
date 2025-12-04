"""
Django settings for news_portal project.
"""

from pathlib import Path

import environ

# ---------------------------
# Environment Setup
# ---------------------------
BASE_DIR = Path(__file__).resolve().parent.parent
env = environ.Env(
    DEBUG=(bool, False),
    ALLOWED_HOSTS=(list, ["127.0.0.1", "localhost"]),
)
environ.Env.read_env(BASE_DIR / ".env")

# ---------------------------
# Security
# ---------------------------
SECRET_KEY = env("DJANGO_SECRET_KEY", default="unsafe-secret-key")
DEBUG = env.bool("DEBUG", default=False)
ALLOWED_HOSTS = env.list("ALLOWED_HOSTS", default=["127.0.0.1", "localhost"])

# ---------------------------
# Custom User Model
# ---------------------------
AUTH_USER_MODEL = "articles.CustomUser"

# ---------------------------
# Authentication Redirects
# ---------------------------
LOGIN_URL = "/login/"
LOGIN_REDIRECT_URL = "/"
LOGOUT_REDIRECT_URL = "/"

# ---------------------------
# Application Definition
# ---------------------------
INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django.contrib.sites",  # required for Site.objects.get_current()
    # Local apps
    "articles",
    # Third-party
    "rest_framework",
]

SITE_ID = 1

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "news_portal.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "news_portal.wsgi.application"

# ---------------------------
# Database (MySQL)
# ---------------------------
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.mysql",
        "NAME": env("DB_NAME", default="news_portal"),
        "USER": env("DB_USER", default="news_user"),  # ✅ non-root default
        "PASSWORD": env("DB_PASSWORD", default=""),
        "HOST": env("DB_HOST", default="db"),
        "PORT": env.int("DB_PORT", default=3306),
    }
}

# ---------------------------
# Password Validation
# ---------------------------
AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"
    },
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

# ---------------------------
# Internationalization
# ---------------------------
LANGUAGE_CODE = "en-us"
TIME_ZONE = "UTC"
USE_I18N = True
USE_TZ = True

# ---------------------------
# Static & Media Files
# ---------------------------
STATIC_URL = "/static/"
STATICFILES_DIRS = [BASE_DIR / "static"] if (BASE_DIR / "static").exists() else []
STATIC_ROOT = BASE_DIR / "staticfiles"

MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media"

# ---------------------------
# Default Primary Key Field Type
# ---------------------------
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# ---------------------------
# Django REST Framework
# ---------------------------
REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "rest_framework.authentication.SessionAuthentication",
        # "rest_framework.authentication.TokenAuthentication",  # optional
    ]
}

# ---------------------------
# Email
# ---------------------------
DEFAULT_FROM_EMAIL = env("DEFAULT_FROM_EMAIL", default="webmaster@localhost")

# ---------------------------
# Twitter / X API Integration (Tweepy v2)
# ---------------------------
TWITTER_ENABLED = env.bool("TWITTER_ENABLED", default=False)

if TWITTER_ENABLED:
    TWITTER_CONSUMER_KEY = env("TWITTER_CONSUMER_KEY")
    TWITTER_CONSUMER_SECRET = env("TWITTER_CONSUMER_SECRET")
    TWITTER_ACCESS_TOKEN = env("TWITTER_ACCESS_TOKEN")
    TWITTER_ACCESS_SECRET = env("TWITTER_ACCESS_SECRET")
    TWITTER_BEARER_TOKEN = env("TWITTER_BEARER_TOKEN", default="")
    TWITTER_PREFIX = env("TWITTER_PREFIX", default="📰 New article:")
else:
    TWITTER_CONSUMER_KEY = ""
    TWITTER_CONSUMER_SECRET = ""
    TWITTER_ACCESS_TOKEN = ""
    TWITTER_ACCESS_SECRET = ""
    TWITTER_BEARER_TOKEN = ""
    TWITTER_PREFIX = "📰 New article:"
