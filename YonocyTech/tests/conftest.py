"""Pytest fixtures for the test suite."""
import os
import sys
import tempfile
import shutil
import pytest

# Ensure YonocyTech/ is on the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

# Use a temp DB for all tests — set before any module imports happen
_test_db = os.environ.get("YONOCYTECH_DB_PATH")
if not _test_db:
    _test_tmp = tempfile.mkdtemp()
    _test_db = os.path.join(_test_tmp, "test.db")
    os.environ["YONOCYTECH_DB_PATH"] = _test_db

    # Clean up at exit
    import atexit
    atexit.register(lambda: shutil.rmtree(_test_tmp, ignore_errors=True))

# Run migrations so tables exist
from database.schema import migrate
migrate()
