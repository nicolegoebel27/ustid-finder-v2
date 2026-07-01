from pathlib import Path
import os

from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent.parent

load_dotenv(BASE_DIR / ".env")

# API-Schlüssel
SERPAPI_KEY = os.getenv("SERPAPI_KEY")

print("===================================")
print("SERPAPI_KEY:", SERPAPI_KEY)
print("===================================")

# Ordner
UPLOAD_DIR = BASE_DIR / "uploads"
OUTPUT_DIR = BASE_DIR / "output"
TEMPLATE_DIR = BASE_DIR / "templates"

UPLOAD_DIR.mkdir(exist_ok=True)
OUTPUT_DIR.mkdir(exist_ok=True)

# Netzwerk
REQUEST_TIMEOUT = 20

# Browserkennung
USER_AGENT = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
    "AppleWebKit/537.36 "
    "(KHTML, like Gecko) "
    "Chrome/137.0 Safari/537.36"
)
