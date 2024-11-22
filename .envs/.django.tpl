# General
# ------------------------------------------------------------------------------
USE_DOCKER=${USE_DOCKER}
IPYTHONDIR=${IPYTHONDIR}
# Redis
# ------------------------------------------------------------------------------
REDIS_URL=${REDIS_URL}

# Celery
# ------------------------------------------------------------------------------

# Flower
CELERY_FLOWER_USER=${CELERY_FLOWER_USER}
CELERY_FLOWER_PASSWORD=${CELERY_FLOWER_PASSWORD}
CELERY_FLOWER_PORT=${CELERY_FLOWER_PORT}


# General
# ------------------------------------------------------------------------------
# DJANGO_READ_DOT_ENV_FILE=${}
DJANGO_SETTINGS_MODULE=${DJANGO_SETTINGS_MODULE}
DJANGO_SECRET_KEY=${DJANGO_SECRET_KEY}
DJANGO_ADMIN_URL=${DJANGO_ADMIN_URL}
DJANGO_ALLOWED_HOSTS=${DJANGO_ALLOWED_HOSTS}

# Security
# ------------------------------------------------------------------------------
# TIP: better off using DNS, however, redirect is OK too
DJANGO_SECURE_SSL_REDIRECT=${DJANGO_SECURE_SSL_REDIRECT}

# Email
# ------------------------------------------------------------------------------
DJANGO_SERVER_EMAIL=${DJANGO_SERVER_EMAIL}
EMAIL_BACKEND=${EMAIL_BACKEND}
EMAIL_HOST=${EMAIL_HOST}
EMAIL_HOST_USER=${EMAIL_HOST_USER}
EMAIL_HOST_PASSWORD=${EMAIL_HOST_PASSWORD}
EMAIL_PORT=${EMAIL_PORT}
EMAIL_SENDER=${EMAIL_SENDER}
EMAIL_USE_TLS=${EMAIL_USE_TLS}
EMAIL_USE_SSL=${EMAIL_USE_SSL}

# django-allauth
# ------------------------------------------------------------------------------
DJANGO_ACCOUNT_ALLOW_REGISTRATION=${DJANGO_ACCOUNT_ALLOW_REGISTRATION}

# Gunicorn
# ------------------------------------------------------------------------------
WEB_CONCURRENCY=${WEB_CONCURRENCY}

# Sentry
# ------------------------------------------------------------------------------
SENTRY_DSN=${SENTRY_DSN}


# Redis
# ------------------------------------------------------------------------------
REDIS_URL=${REDIS_URL}

# Celery
# ------------------------------------------------------------------------------

# Flower
CELERY_FLOWER_USER=${CELERY_FLOWER_USER}
CELERY_FLOWER_PASSWORD=${CELERY_FLOWER_PASSWORD}
