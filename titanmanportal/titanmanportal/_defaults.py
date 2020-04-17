import json

from . import BASE_DIR


DEFAULT_DATABASES = json.dumps({
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': str(BASE_DIR / 'db.sqlite3'),
    }
})
DEFAULT_LOG_LEVEL = 'WARNING'
