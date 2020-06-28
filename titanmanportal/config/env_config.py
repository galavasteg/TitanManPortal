from os import getenv

from . import BASE_DIR


try:
    from dotenv import load_dotenv
    from pathlib import Path
    this_dir = Path(__file__).parent.parent

    dotenv_path = this_dir / '.env'
    if dotenv_path.exists():
        load_dotenv(dotenv_path)

except ImportError:  # dotenv isn't installed on PRD
    pass


# star-import for settings
__all__ = (
    'DATABASES',
    'SECRET_KEY', 'DEBUG', 'LOG_LEVEL', 'STATIC_ROOT',
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


# log settings, see log_config.py
APP_NAME = getenv('APP_NAME', 'AUTH')

default_log_level = 'DEBUG' if DEBUG else 'WARNING'
LOG_LEVEL = getenv('LOG_LEVEL', default_log_level)
LOGGER_NAME = f'{APP_NAME}_log'.lower()
