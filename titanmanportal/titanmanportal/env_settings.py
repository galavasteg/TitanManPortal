import json
from os import getenv

from .defaults import DEFAULT_LOG_LEVEL, DEFAULT_DATABASES

__all__ = (
    'DATABASES',
    'SECRET_KEY', 'DEBUG', 'LOG_LEVEL', 'STATIC_ROOT',
    'VK_APP_ID', 'VK_OAUTH2_KEY', 'VK_OAUTH2_SECRET',
)

SECRET_KEY = getenv('SECRET_KEY')

# Database
# https://docs.djangoproject.com/en/3.0/ref/settings/#databases
DATABASES = json.loads(getenv('DATABASES', DEFAULT_DATABASES))

VK_APP_ID = getenv('VK_APP_ID')
VK_OAUTH2_KEY = getenv('VK_OAUTH2_KEY')
VK_OAUTH2_SECRET = getenv('VK_OAUTH2_SECRET')

SITE_URL = getenv('SITE_URL', '')

# DJANGO MODE
DEBUG = getenv('DEBUG', 'true').lower() == 'true'

default_log_level = 'DEBUG' if DEBUG else DEFAULT_LOG_LEVEL
LOG_LEVEL = getenv('LOG_LEVEL', default_log_level)

STATIC_ROOT = getenv('STATIC_ROOT', '/static/')
