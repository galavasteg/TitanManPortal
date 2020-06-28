from pathlib import Path


this_dir = Path(__file__).absolute().parent
BASE_DIR = this_dir.parent
PROJECT_NAME = BASE_DIR.stem
