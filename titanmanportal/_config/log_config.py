from .env_config import LOG_LEVEL, LOGGER_NAME


LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        # 'json': {
        #     '()': JSONFormatter,
        #     'jsondumps_kwargs': {
        #         'ensure_ascii': False,
        #         # 'indent': 2,
        #     }
        # }
    },
    'handlers': {
        # 'json2console': {
        #   'class': 'logging.StreamHandler',
        #   'level': LOG_LEVEL,
        #   'formatter': 'json',
        #   'stream': 'ext://sys.stdout'
        # },
        'console': {
          'class': 'logging.StreamHandler',
          'level': LOG_LEVEL,
          'stream': 'ext://sys.stdout'
        },
    },
    'loggers': {
        LOGGER_NAME: {
            'level': LOG_LEVEL,
            'handlers': [
                # 'json2console',
                'console',
            ],
            'propagate': False,
        },
    }
}
