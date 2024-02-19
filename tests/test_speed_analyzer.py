import os
import sys
import pytest
import numpy as np
import pandas as pd
from typing import List

# AI content (GitHub Copilot, 01/25/2024), verified and adapted by Nicolas Huber.
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import src.algorithms.speed_analyzer as speed_analyzer

EXAMPLE_FILE_PATH: str = "tests/assets/speed_analyzer/test_speed_analyzer.csv"
TEST_DATA: List[List[float]] = [
    [7.5, -1],
    [7.777777778, -2],
    [8.055555556, -1],
    [8.333333333, -2],
    [8.611111111, -1.5],
    [8.888888889, -2.333333333],
    [9.166666667, -0.8],
    [9.444444444, -1],
    [9.722222222, -1.333333333],
    [10, -1.333333333],
    [10.27777778, -1.666666667],
    [10.55555556, -1.714285714],
    [10.83333333, -1.444444444],
    [11.11111111, -1],
    [11.38888889, -1.5],
    [11.66666667, -1.857142857],
    [11.94444444, -1],
    [12.22222222, -1.428571429],
    [12.5, -1.5],
    [12.77777778, -1.666666667],
    [13.05555556, -1.857142857],
    [13.33333333, -1.5],
    [13.61111111, -1.285714286],
    [13.88888889, -1.666666667],
    [14.16666667, -1.5],
    [14.44444444, -1.2],
    [14.72222222, -2.111111111],
    [15, -2],
    [15.27777778, -2.142857143],
    [15.55555556, -1.5],
    [15.83333333, -1.5],
    [16.11111111, -2],
    [16.38888889, -2.5],
    [16.66666667, -1],
    [17.5, -4],
]
TEST_DATA: pd.DataFrame = pd.DataFrame(
    TEST_DATA, columns=["horizontal velocity [m/s]", "vertical velocity [m/s]"]
)


@pytest.fixture
def analyzer() -> speed_analyzer.SpeedAnalyzer:
    """
    Fixture to create a SpeedAnalyzer object.

    Args:
    - None

    Returns:
    - speed_analyzer (speed_analyzer.SpeedAnalyzer): SpeedAnalyzer instance.
    """
    return speed_analyzer.SpeedAnalyzer()


def test_init(analyzer) -> None:
    """
    Test __init__ method.

    Args:
    - None

    Returns:
    - None
    """
    assert analyzer is not None
    assert analyzer.convertor is not None


def test_filter_raw_data(analyzer) -> None:
    """
    Test filter_raw_data method.

    Args:
    - analyzer (speed_analyzer.SpeedAnalyzer): SpeedAnalyzer instance.

    Returns:
    - None
    """
    data_filtered: pd.DataFrame = analyzer.filter_raw_data(
        data=TEST_DATA, reference=True
    )
    assert data_filtered is not None
    assert data_filtered["horizontal velocity [m/s]"].is_monotonic_increasing
    assert data_filtered["horizontal velocity [m/s]"].min() >= 8
    assert data_filtered["horizontal velocity [m/s]"].max() <= 15.5
    assert data_filtered["vertical velocity [m/s]"].min() <= 0


def test_savgol_filter(analyzer) -> None:
    """
    Test savgol_filter method.

    Args:
    - analyzer (speed_analyzer.SpeedAnalyzer): SpeedAnalyzer instance.

    Returns:
    - None
    """
    data_filtered: pd.DataFrame = analyzer.filter_raw_data(
        data=TEST_DATA, reference=True
    )
    data_filtered = analyzer.savgol_filter(data_filtered)
    assert data_filtered is not None
    assert data_filtered["horizontal velocity [m/s]"].is_monotonic_increasing
    assert data_filtered["horizontal velocity [m/s]"].min() >= 8
    assert data_filtered["horizontal velocity [m/s]"].max() <= 15.5
    assert data_filtered["vertical velocity [m/s]"].min() <= 0


def test_group_data(analyzer) -> None:
    """
    Test group_data method.

    Args:
    - analyzer (speed_analyzer.SpeedAnalyzer): SpeedAnalyzer instance.

    Returns:
    - None
    """
    data_filtered: pd.DataFrame = analyzer.filter_raw_data(
        data=TEST_DATA, reference=True
    )
    data_filtered = analyzer.savgol_filter(data_filtered)
    data_grouped: pd.DataFrame = analyzer.group_data(data_filtered)
    assert data_grouped is not None
    assert data_grouped["horizontal velocity [m/s]"].is_monotonic_increasing
    assert data_grouped["horizontal velocity [m/s]"].min() >= 8
    assert data_grouped["horizontal velocity [m/s]"].max() <= 15.5
    assert data_grouped["vertical velocity [m/s]"].min() <= 0

    assert (data_grouped["horizontal velocity [m/s]"] * 10 % 1 == 0).all()
    assert data_grouped["horizontal velocity [m/s]"].nunique() == len(data_grouped)
