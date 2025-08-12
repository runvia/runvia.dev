# backend/conftest.py

import sys
from pathlib import Path

# Add the backend directory itself to sys.path so `import app` works
sys.path.insert(0, str(Path(__file__).parent.resolve()))
