"""
WSGI config for titanmanportal project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.0/howto/deployment/wsgi/
"""

import os
import sys
from pathlib import Path

from django.core.wsgi import get_wsgi_application


this_file = Path(__file__).absolute()
# target is ".../TitanManPortal/titanmanportal/"
PRG_DIR = this_file.parent.parent
sys.path.insert(0, str(PRG_DIR))

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'titanmanportal.settings')

application = get_wsgi_application()
