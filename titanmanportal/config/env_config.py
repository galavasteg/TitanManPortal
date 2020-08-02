from os import getenv

import utils
from . import BASE_DIR


utils.try_load_dotenv()


PROJECT_NAME = 'TitanManPortal'

SECRET_KEY = getenv('SECRET_KEY')
SITE_URL = getenv('SITE_URL', '')
STATIC_ROOT = getenv('STATIC_ROOT', '/static/')
MEDIA_ROOT = getenv('MEDIA_ROOT', '/data/')
DEBUG = getenv('DEBUG', 'true').lower() == 'true'

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

# social providers' credentials
SOCIALACCOUNT_PROVIDERS = {
    'vk': {
        'APP': {
            'client_id': getenv('VK_APP_ID'),
            'secret': getenv('VK_OAUTH2_KEY'),
            'key': getenv('VK_OAUTH2_SECRET')
        },
    },
    'facebook': {
        'SCOPE': ['email'],
        'AUTH_PARAMS': {'auth_type': 'reauthenticate'},
        'METHOD': 'oauth2',
        'VERIFIED_EMAIL': False,
        'APP': {
            'client_id': getenv('FB_APP_ID'),
            'secret': getenv('FB_OAUTH2_KEY'),
            # 'key': getenv('FB_OAUTH2_SECRET')
        },
    }
}

# used by log_config.py
default_log_level = 'DEBUG' if DEBUG else 'INFO'
LOG_LEVEL = getenv('LOG_LEVEL', default_log_level)
MAIN_LOG_NAME = PROJECT_NAME.lower()
