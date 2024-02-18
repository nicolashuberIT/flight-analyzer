import os
import sys
import pytest
from typing import List

# AI content (GitHub Copilot, 01/25/2024), verified and adapted by Nicolas Huber.
src_directory: str = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
sys.path.append(src_directory)

import src.constants as constants
import src.helpers.file_processor as file_processor

DIRECTORY: str = "tests/assets/file_processor/"
FILE_EXTENSION: str = ".csv"


@pytest.fixture
def processor() -> file_processor.FileProcessor:
    return file_processor.FileProcessor()


def test_init(processor: file_processor.FileProcessor) -> None:
    """
    Test __init__ method.

    Args:
    - processor (file_processor.FileProcessor): FileProcessor instance.

    Returns:
    - None.
    """
    assert processor is not None


def test_get_file_paths(processor: file_processor.FileProcessor) -> None:
    """
    Test get_file_paths method.

    Args:
    - processor (file_processor.FileProcessor): FileProcessor instance.

    Returns:
    - None.
    """
    file_paths: List[str] = processor.get_file_paths(DIRECTORY, FILE_EXTENSION)
    assert len(file_paths) == 2
    assert file_paths[0] == f"{DIRECTORY}test_1.csv"
    assert file_paths[1] == f"{DIRECTORY}test_2.csv"
    assert f"{DIRECTORY}test.igc" not in file_paths
