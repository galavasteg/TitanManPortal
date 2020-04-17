"""
ASGI config for titanmanportal project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.0/howto/deployment/asgi/
"""

import sys
from pathlib import Path

from django.core.asgi import get_asgi_application


this_file = Path(__file__).absolute()
PRG_DIR = this_file.parent.parent  # .../TitanManPortal/titanmanportal/
sys.path.insert(0, str(PRG_DIR))

application = get_asgi_application()
