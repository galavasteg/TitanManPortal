from os import getenv

# DJANGO MODE
DEBUG = bool(getenv('DEBUG', 'True') == 'True')

try:
    from dotenv import load_dotenv
    from pathlib import Path
    this_dir = Path(__file__).parent

    dotenv_path = this_dir / '.env'
    if dotenv_path.exists() and DEBUG:
        load_dotenv(dotenv_path)

except ImportError:  # dotenv not installed on PRD
    pass


SECRET_KEY = getenv('SECRET_KEY')

default_log_level = 'DEBUG' if DEBUG else 'WARNING'
LOG_LEVEL = getenv('LOG_LEVEL', default_log_level)

SITE_URL = getenv('SITE_URL', '')
STATIC_ROOT = getenv('STATIC_ROOT', '/data/')
