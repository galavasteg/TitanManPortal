import json
import logging
from collections import OrderedDict
from typing import Optional

from .env_config import LOG_LEVEL, MAIN_LOG_NAME


class JSONFormatter(logging.Formatter):

    def __init__(self, jsondumps_kwargs: Optional[dict] = None,
                 *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.jsondumps_kwargs = jsondumps_kwargs or {}

    def format(self, record):
        """
        Format a log record and serialize to json, examples:

        {"time": "2020-04-28 13:26:51,910", "name": "APPNAME", "lvl": "INFO",
         "msg": "input", "place": "module.func:105"}

        {"time": "2020-04-28 14:31:37,759", "name": "APPNAME", "lvl": "ERROR",
         "msg": "\"baz\" missed =/", "place": "logger_usage.main:14",
         "exc_info": "Traceback (most recent call last):\n  File \"/module.py\", line 12, in function\n    _ = some_data['baz']\nKeyError: 'baz'"}

        """
        details = (
            ('time', self.formatTime(record)),
            ('name', record.name),
            ('lvl', record.levelname),
            ('msg', record.getMessage()),
            ('place', f'{record.module}.{record.funcName}:{record.lineno}'),
        )

        if record.exc_info:
            exc_info = self.formatException(record.exc_info)
            details += (('exc_info', exc_info),)

        log_record = OrderedDict(details)
        json_record = json.dumps(log_record, **self.jsondumps_kwargs)

        return json_record


LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'json': {
            '()': JSONFormatter,
            'jsondumps_kwargs': {
                'ensure_ascii': False,
                # 'indent': 2,
            }
        }
    },
    'handlers': {
        'json2console': {
          'class': 'logging.StreamHandler',
          # 'level': LOG_LEVEL,
          'formatter': 'json',
          'stream': 'ext://sys.stdout'
        },
        'console': {
          'class': 'logging.StreamHandler',
          # 'level': LOG_LEVEL,
          'stream': 'ext://sys.stdout'
        },
    },
    'loggers': {
        MAIN_LOG_NAME: {
            'level': LOG_LEVEL,
            'handlers': [
                'json2console',
                # 'console',
            ],
            'propagate': False,
        },
    }
}
