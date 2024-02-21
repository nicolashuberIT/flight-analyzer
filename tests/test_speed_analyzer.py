import os
import sys
import pytest
import numpy as np
import pandas as pd
from typing import List

# AI content (ChatGPT, 02/21/2024), verified and adapted by Nicolas Huber.
current_directory = os.path.dirname(__file__)
flight_analyzer_directory = os.path.abspath(os.path.join(current_directory, ".."))
sys.path.insert(0, flight_analyzer_directory)

import src.algorithms.speed_analyzer as speed_analyzer

CSV_INPUT: str = (
    f"{flight_analyzer_directory}/tests/assets/speed_analyzer/test_speed_analyzer.csv"
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


@pytest.fixture
def dataset() -> pd.DataFrame:
    """
    Fixture to create a dataset.

    Args:
    - None

    Returns:
    - dataset (pd.DataFrame): Dataset.
    """
    return pd.read_csv(CSV_INPUT)


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


def test_filter_raw_data(analyzer, dataset) -> None:
    """
    Test filter_raw_data method.

    Args:
    - analyzer (speed_analyzer.SpeedAnalyzer): SpeedAnalyzer instance.

    Returns:
    - None
    """
    data_filtered: pd.DataFrame = analyzer.filter_raw_data(data=dataset, reference=True)
    assert data_filtered is not None
    assert data_filtered["horizontal velocity [m/s]"].is_monotonic_increasing
    assert data_filtered["horizontal velocity [m/s]"].min() >= 8
    assert data_filtered["horizontal velocity [m/s]"].max() <= 15.5
    assert data_filtered["vertical velocity [m/s]"].min() <= 0


def test_savgol_filter(analyzer, dataset) -> None:
    """
    Test savgol_filter method.

    Args:
    - analyzer (speed_analyzer.SpeedAnalyzer): SpeedAnalyzer instance.

    Returns:
    - None
    """
    data_filtered: pd.DataFrame = analyzer.filter_raw_data(data=dataset, reference=True)
    data_filtered = analyzer.savgol_filter(data_filtered)
    assert data_filtered is not None
    assert data_filtered["horizontal velocity [m/s]"].is_monotonic_increasing
    assert data_filtered["horizontal velocity [m/s]"].min() >= 8
    assert data_filtered["horizontal velocity [m/s]"].max() <= 15.5
    assert data_filtered["vertical velocity [m/s]"].min() <= 0


def test_group_data(analyzer, dataset) -> None:
    """
    Test group_data method.

    Args:
    - analyzer (speed_analyzer.SpeedAnalyzer): SpeedAnalyzer instance.

    Returns:
    - None
    """
    data_filtered: pd.DataFrame = analyzer.filter_raw_data(data=dataset, reference=True)
    data_filtered = analyzer.savgol_filter(data_filtered)
    data_grouped: pd.DataFrame = analyzer.group_data(data_filtered)
    assert data_grouped is not None
    assert data_grouped["horizontal velocity [m/s]"].is_monotonic_increasing
    assert data_grouped["horizontal velocity [m/s]"].min() >= 8
    assert data_grouped["horizontal velocity [m/s]"].max() <= 15.5
    assert data_grouped["vertical velocity [m/s]"].min() <= 0

    assert (data_grouped["horizontal velocity [m/s]"] * 10 % 1 == 0).all()
    assert data_grouped["horizontal velocity [m/s]"].nunique() == len(data_grouped)
