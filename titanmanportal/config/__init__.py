import sys
from pathlib import Path


this_dir = Path(__file__).absolute().parent
BASE_DIR = this_dir.parent
sys.path.insert(0, BASE_DIR / 'apps')
