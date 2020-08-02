"""
Django settings for titanmanportal project.

"""

from django.utils.translation import gettext_lazy as _

# Build paths inside the project like this:
#  path = str(BASE_DIR / ...))
from . import BASE_DIR
from .env_config import (
    SECRET_KEY, DEBUG, STATIC_ROOT,
    DATABASES,
    # social providers credentials
    SOCIALACCOUNT_PROVIDERS,
)
from .log_config import LOGGING


ALLOWED_HOSTS = [
    'galavasteg.pythonanywhere.com',
    'localhost', '127.0.0.1',
    'portal.titanman.ru',
    'titanman.ru',
]

# Application definition
INSTALLED_APPS = [
    # 'material.admin',
    # 'material.admin.default',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    "django.contrib.sites",

    'admin_reorder',
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'allauth.socialaccount.providers.vk',
    'allauth.socialaccount.providers.facebook',

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

    'admin_reorder.middleware.ModelAdminReorder',
]

ROOT_URLCONF = 'config.urls'

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

WSGI_APPLICATION = 'config.wsgi.application'

# Internationalization
# https://docs.djangoproject.com/en/3.0/topics/i18n/
LANGUAGE_CODE = "ru-ru"
TIME_ZONE = 'Europe/Moscow'
# USE_TZ = True
USE_L18N = True
USE_I18N = True
USE_L10N = True
LOCALE_PATHS = (str(BASE_DIR / 'titanman/locale'),)
LANGUAGES = (
    ("ru", _("Русский")),
    ("en", _("English")),
)

# Configure your default site. See
# https://docs.djangoproject.com/en/dev/ref/settings/#sites.
# for INSTALLED_APPS:[API auth registration]
SITE_ID = 1

# SECURE_SSL_REDIRECT = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.0/howto/static-files/
STATIC_URL = '/static/'


ADMIN_REORDER = (
    # MODERATION group
    {
        'app': 'moderation',
        'label': _('Модерация'),
    },
    # PERIODS group
    {
        'app': 'periods',
        'label': _('Periods'),
    },
    # USER group
    {
        'app': 'users',
        'label': _('Участник'),
        'models': (
            {
                'model': 'rating.Rating',
                'label': _('Рейтинг'),
            },
        ),
    }
)

AUTH_USER_MODEL = 'users.User'
LOGIN_REDIRECT_URL = '/'
LOGOUT_REDIRECT_URL = '/accounts/login/'
ACCOUNT_LOGOUT_REDIRECT_URL = '/accounts/login/'
EMAIL_LOG_NAME = 'email'
# ACCOUNT_DEFAULT_HTTP_PROTOCOL = 'https'
ACCOUNT_USER_MODEL_USERNAME_FIELD = None
ACCOUNT_AUTHENTICATION_METHOD = 'email'
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_USERNAME_REQUIRED = False
ACCOUNT_EMAIL_VERIFICATION = 'optional'
ACCOUNT_EMAIL_CONFIRMATION_EXPIRE_DAYS = 365
ACCOUNT_UNIQUE_EMAIL = True
ACCOUNT_USER_EMAIL_FIELD = 'email'
ACCOUNT_LOGOUT_ON_GET = True
ACCOUNT_CONFIRM_EMAIL_ON_GET = True
ACCOUNT_EMAIL_CONFIRMATION_HMAC = False

SOCIALACCOUNT_EMAIL_VERIFICATION = 'none'
SOCIALACCOUNT_AUTO_SIGNUP = True
SOCIALACCOUNT_ADAPTER = 'users.socialaccount_adapter.SocialAccountAdapter'

# Password validation
# https://docs.djangoproject.com/en/3.0/ref/settings/#auth-password-validators
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
        'OPTIONS': dict(min_length=6),
    },
    # TODO: enable if not DEBUG
    # {
    #     'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    # },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

AUTHENTICATION_BACKENDS = (
    # Needed to login by username in Django admin, regardless of `allauth`
    'django.contrib.auth.backends.ModelBackend',
    # `allauth` specific authentication methods, such as login by e-mail
    'allauth.account.auth_backends.AuthenticationBackend',
)

EMAIL_BACKEND = 'django.core.mail.backends.dummy.EmailBackend'
