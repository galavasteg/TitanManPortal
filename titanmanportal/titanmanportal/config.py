from os import getenv


# DJANGO MODE
DEBUG = getenv('DEBUG', 'True').lower() == 'true'

SECRET_KEY = getenv('SECRET_KEY')

default_log_level = 'DEBUG' if DEBUG else 'WARNING'
LOG_LEVEL = getenv('LOG_LEVEL', default_log_level)

SITE_URL = getenv('SITE_URL', '')
STATIC_ROOT = getenv('STATIC_ROOT', '/data/')
