import sys
from pathlib import Path


PROJECT_ROOT = Path(__file__).parent
BASE_DIR = PROJECT_ROOT.parent
sys.path.insert(0, str(BASE_DIR / 'apps'))
