import sys
import os

# Add parent directory (backend) to python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from app.main import app
