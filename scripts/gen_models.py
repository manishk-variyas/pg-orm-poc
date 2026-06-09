import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from app.settings import settings
import subprocess

url = settings.database_url
outfile = sys.argv[1] if len(sys.argv) > 1 else "app/models.py"

subprocess.run(["sqlacodegen", url, "--outfile", outfile])
