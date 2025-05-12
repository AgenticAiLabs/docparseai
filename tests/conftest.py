import os
import pytest

@pytest.fixture(scope="module")
def test_files_path():
    return os.path.join(os.path.dirname(__file__), "test_files")
