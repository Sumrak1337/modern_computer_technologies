import os
from pathlib import Path

PROJECT_ROOT = Path(__file__).absolute().parent
DATA_ROOT = PROJECT_ROOT / 'data'
RESULTS_ROOT = PROJECT_ROOT / 'results'

os.makedirs(RESULTS_ROOT, exist_ok=True)
