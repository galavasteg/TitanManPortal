"""
WSGI config for titanmanportal project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.0/howto/deployment/wsgi/
"""

import sys
from pathlib import Path

from django.core.wsgi import get_wsgi_application


this_file = Path(__file__).absolute()
PRG_DIR = this_file.parent.parent  # .../TitanManPortal/titanmanportal/
sys.path.insert(0, str(PRG_DIR))

application = get_wsgi_application()
