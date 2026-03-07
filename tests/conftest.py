import sys
import os

# This tells Python where to find our app code (the models, schemas, etc.)
# Without this, pytest wouldn't know where "models" or "schemas" live.
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "app"))
