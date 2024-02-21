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


import src.constants as constants
import src.helpers.file_processor as file_processor
import src.algorithms.c_values_analyzer as c_values_analyzer
import src.algorithms.speed_analyzer as speed_analyzer

INPUT_DIRECTORY: str = f"{flight_analyzer_directory}/tests/assets/c_values_analyzer"
FILE_EXTENSION: str = ".igc"


@pytest.fixture()
def c_analyzer() -> c_values_analyzer.CAnalyzer:
    """
    Create a CValuesAnalyzer object for testing purposes.

    Parameters:
    - None.

    Returns:
    - CValuesAnalyzer: The CValuesAnalyzer object.
    """
    return c_values_analyzer.CAnalyzer()


@pytest.fixture()
def speeds() -> speed_analyzer.SpeedAnalyzer:
    """
    Create a SpeedAnalyzer object for testing purposes.

    Parameters:
    - None.

    Returns:
    - SpeedAnalyzer: The SpeedAnalyzer object.
    """
    return speed_analyzer.SpeedAnalyzer()


@pytest.fixture()
def files() -> file_processor.FileProcessor:
    """
    Create a FileProcessor object for testing purposes.

    Parameters:
    - None.

    Returns:
    - FileProcessor: The FileProcessor object.
    """
    return file_processor.FileProcessor()


@pytest.fixture()
def dataset(files, speeds) -> pd.DataFrame:
    """
    Load the dataset from the input directory.

    Parameters:
    - file_processor (FileProcessor): The FileProcessor object.
    - speed_analyzer (SpeedAnalyzer): The SpeedAnalyzer object.

    Returns:
    - pd.DataFrame: The dataset.
    """
    file_paths: List[str] = files.get_file_paths(
        path=INPUT_DIRECTORY, file_extension=FILE_EXTENSION
    )
    data_raw: pd.DataFrame = speeds.process_raw_data(file_paths=file_paths)
    data_raw_filtered: pd.DataFrame = speeds.filter_raw_data(data=data_raw)
    smoothed_data_raw: pd.DataFrame = speeds.savgol_filter(data=data_raw_filtered)
    smoothed_data_grouped: pd.DataFrame = speeds.group_data(data=smoothed_data_raw)
    return smoothed_data_grouped


def test_init(c_analyzer) -> None:
    """
    Test the initialization of the CValuesAnalyzer object.

    Parameters:
    - analyzer (CValuesAnalyzer): The CValuesAnalyzer object to test.

    Returns:
    - None.
    """
    assert c_analyzer is not None


def test_positive_vertical_speed(c_analyzer, dataset) -> None:
    """
    Test if only positive vertical speeds are within the dataset.

    Parameters:
    - analyzer (CValuesAnalyzer): The CValuesAnalyzer object to test.
    - dataset (pd.DataFrame): The dataset to test.

    Returns:
    - None.
    """
    data: pd.DataFrame = c_analyzer.positive_vertical_speed(speed_data=dataset)
    assert (data["vertical velocity [m/s]"] >= 0).all()


def test_calculate_airspeed(c_analyzer, dataset) -> None:
    """
    Test the calculation of the airspeed.

    Parameters:
    - analyzer (CValuesAnalyzer): The CValuesAnalyzer object to test.
    - dataset (pd.DataFrame): The dataset to test.

    Returns:
    - None.
    """
    data: pd.DataFrame = c_analyzer.positive_vertical_speed(speed_data=dataset)
    airspeed: pd.DataFrame = c_analyzer.calculate_airspeed(speed_data=data)

    assert "horizontal velocity [m/s]" in airspeed.columns
    assert "vertical velocity [m/s]" in airspeed.columns
    assert "airspeed [m/s]" in airspeed.columns
    assert (
        airspeed["airspeed [m/s]"]
        == np.sqrt(
            airspeed["horizontal velocity [m/s]"] ** 2
            + airspeed["vertical velocity [m/s]"] ** 2
        )
    ).all()


def test_calculate_ca_value(c_analyzer) -> None:
    """
    Test the calculation of the Ca value.

    Parameters:
    - analyzer (CValuesAnalyzer): The CValuesAnalyzer object to test.

    Returns:
    - None.
    """
    cw: float = 0.02
    horizontal_velocity: float = 10
    vertical_velocity: float = 2

    ca = c_analyzer.calculate_ca_value(
        cw=cw,
        horizontal_speed=horizontal_velocity,
        vertical_speed=vertical_velocity,
    )

    assert ca == 0.1


def test_calculate_cw_value_simplified(c_analyzer) -> None:
    """
    Test the calculation of the Cw value.

    Parameters:
    - analyzer (CValuesAnalyzer): The CValuesAnalyzer object to test.

    Returns:
    - None.
    """
    horizontal_velocity: float = 10
    vertical_velocity: float = 2
    airspeed: float = np.sqrt(horizontal_velocity**2 + vertical_velocity**2)

    cw = c_analyzer.calculate_cw_value_simplified(
        horizontal_speed=horizontal_velocity,
        vertical_speed=vertical_velocity,
        airspeed=airspeed,
    )

    assert round(cw, 4) == 0.0609


def test_calculate_cw_value_optimized(c_analyzer) -> None:
    """
    Test the calculation of the Cw value.

    Parameters:
    - analyzer (CValuesAnalyzer): The CValuesAnalyzer object to test.

    Returns:
    - None.
    """
    horizontal_velocity: float = 10
    vertical_velocity: float = 2
    airspeed: float = np.sqrt(horizontal_velocity**2 + vertical_velocity**2)

    cw = c_analyzer.calculate_cw_value_optimized(
        horizontal_speed=horizontal_velocity,
        vertical_speed=vertical_velocity,
        airspeed=airspeed,
    )

    assert round(cw, 4) == 0.0716


def test_process_c_values(c_analyzer, dataset) -> None:
    """
    Test the calculation of the Cw and Ca values.

    Parameters:
    - analyzer (CValuesAnalyzer): The CValuesAnalyzer object to test.
    - dataset (pd.DataFrame): The dataset to test.

    Returns:
    - None.
    """
    data: pd.DataFrame = c_analyzer.positive_vertical_speed(speed_data=dataset)
    airspeed: pd.DataFrame = c_analyzer.calculate_airspeed(speed_data=data)
    values: pd.DataFrame = c_analyzer.process_c_values(
        speed_data=airspeed, algorithm=True
    )

    assert "horizontal velocity [m/s]" in values.columns
    assert "vertical velocity [m/s]" in values.columns
    assert "airspeed [m/s]" in values.columns
    assert "Cw [0.5]" in values.columns
    assert "Ca [0.5]" in values.columns
