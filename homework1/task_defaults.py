import os
from pathlib import Path

PROJECT_ROOT = Path(__file__).absolute().parent
RESULT_ROOT = PROJECT_ROOT / 'results'
DATA_ROOT = PROJECT_ROOT / 'data'

os.makedirs(RESULT_ROOT, exist_ok=True)
