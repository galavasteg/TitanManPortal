from os import getenv

from . import BASE_DIR, PROJECT_NAME


__all__ = (
    'SECRET_KEY', 'DEBUG', 'STATIC_ROOT',
    'DATABASES',
    # social providers' credentials
    'VK_APP_ID', 'VK_OAUTH2_KEY', 'VK_OAUTH2_SECRET',
    'FB_APP_ID', 'FB_OAUTH2_KEY', 'FB_OAUTH2_SECRET',
)


SECRET_KEY = getenv('SECRET_KEY')

SITE_URL = getenv('SITE_URL', '')

# DJANGO MODE
DEBUG = getenv('DEBUG', 'true').lower() == 'true'

# Database
# https://docs.djangoproject.com/en/3.0/ref/settings/#databases
DATABASES = {
    'default': {
        'ENGINE': getenv('DB_ENGINE', 'django.db.backends.sqlite3'),
        'NAME': getenv('DB_NAME', str(BASE_DIR / 'db.sqlite3')),
        'USER': getenv('DB_USER', ''),
        'PASSWORD': getenv('DB_PASSWORD', ''),
        'HOST': getenv('DB_HOST', ''),
        'PORT': getenv('DB_PORT', 8080),
    }
}

VK_APP_ID = getenv('VK_APP_ID')
VK_OAUTH2_KEY = getenv('VK_OAUTH2_KEY')
VK_OAUTH2_SECRET = getenv('VK_OAUTH2_SECRET')

FB_APP_ID = getenv('FB_APP_ID')
FB_OAUTH2_KEY = getenv('FB_OAUTH2_KEY')
FB_OAUTH2_SECRET = getenv('FB_OAUTH2_SECRET')

STATIC_ROOT = getenv('STATIC_ROOT', '/static/')


# used by log_config.py
default_log_level = 'DEBUG' if DEBUG else 'WARNING'
LOG_LEVEL = getenv('LOG_LEVEL', default_log_level)
LOGGER_NAME = f'{PROJECT_NAME}_log'.lower()
