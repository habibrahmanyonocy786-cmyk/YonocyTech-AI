import pytest
from tools.file_processor import FileProcessor

def test_file_processor_read_text(tmp_path):
    p = tmp_path / "test.txt"
    p.write_text("Hello World")
    res = FileProcessor.read_text(str(p))
    assert res == "Hello World"

def test_unsupported_format():
    # Using a non-existent file to simulate error
    res = FileProcessor.auto_read("non_existent.unknown")
    assert "Error" in res or res is None
