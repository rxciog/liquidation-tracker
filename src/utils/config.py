from pathlib import Path

# Project root directory
PROJECT_ROOT = Path(__file__).parent.parent.parent

# Data directories
DATA_DIR = PROJECT_ROOT / "data"
INPUT_DIR = DATA_DIR / "input"
OUTPUT_DIR = DATA_DIR / "output"

# CSV output path 
CSV_OUTPUT_PATH = DATA_DIR / "liquidaciones"

# Python executable for subprocess calls
VENV_PYTHON = PROJECT_ROOT / ".venv" / "bin" / "python"

# Ensure directories exist
INPUT_DIR.mkdir(parents=True, exist_ok=True)
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
CSV_OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
