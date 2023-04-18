from pathlib import Path
from tomllib import load as load_toml

# Read .toml file
with open("../config.toml", "rb") as f:
    data = load_toml(f)

# Constants from loaded .toml
FILE, ZIPFILE = data.get('files').values()
DATE_FORMAT = data.get('date_format')['format']
BASE_DIR = f"{Path(__file__).parent.parent}/{data.get('data_dir')['dir']}/"
