"""
Django settings for titanmanportal project.

"""

import sys
from pathlib import Path

from django.utils.translation import ugettext_lazy as _

from .env_settings import *


# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
PROJECT_ROOT = Path(__file__).parent
BASE_DIR = PROJECT_ROOT.parent
sys.path.insert(0, str(BASE_DIR / 'apps'))

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = [
    'galavasteg.pythonanywhere.com',
    'localhost',
    'portal.titanman.ru',
    'titanman.ru',
]


# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    "django.contrib.sites",

    # Portal Apps
    'users',
    'periods',
    'moderation',
    'rating',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'titanmanportal.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'titanmanportal.wsgi.application'

AUTH_USER_MODEL = 'users.User'

# Database
# https://docs.djangoproject.com/en/3.0/ref/settings/#databases
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': str(BASE_DIR / 'db.sqlite3'),
    }
}


# Password validation
# https://docs.djangoproject.com/en/3.0/ref/settings/#auth-password-validators
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# Configure your default site. See
# https://docs.djangoproject.com/en/dev/ref/settings/#sites.
# for INSTALLED_APPS:[API auth registration]
SITE_ID = 1

# Internationalization
# https://docs.djangoproject.com/en/3.0/topics/i18n/
LANGUAGE_CODE = "ru-ru"
TIME_ZONE = 'Europe/Moscow'
USE_TZ = False
USE_L18N = True
USE_I18N = True
USE_L10N = True
LOCALE_PATHS = (str(BASE_DIR / 'titanman/locale'),)
LANGUAGES = (
    ("ru", _("Русский")),
    ("en", _("English")),
)

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.0/howto/static-files/
STATIC_URL = '/static/'

LOGOUT_REDIRECT_URL = "/"
