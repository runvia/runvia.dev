# backend/conftest.py
import os
import sys
from pathlib import Path

# Add the backend directory itself to sys.path so `import app` works
sys.path.insert(0, str(Path(__file__).parent.resolve()))

os.environ["DATABASE_URL"] = "sqlite://"
os.environ["SECRET_KEY"] = "test-secret-key-not-for-production"
os.environ["SESSION_SECRET_KEY"] = "test-secret-key-not-for-production"
