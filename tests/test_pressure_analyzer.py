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
import src.algorithms.pressure_analyzer as pressure_analyzer

INPUT_DIRECTORY: str = f"{flight_analyzer_directory}/tests/assets/c_values_analyzer"
FILE_EXTENSION: str = ".igc"

@pytest.fixture()
def p_analyzer() -> pressure_analyzer.PressureAnalyzer:
    """
    Create a PressureAnalyzer object for testing purposes.

    Parameters:
    - None.

    Returns:
    - PressureAnalyzer: The PressureAnalyzer object.
    """
    return pressure_analyzer.PressureAnalyzer()

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
def dataset(files, speeds, c_analyzer) -> pd.DataFrame:
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
    data_airspeed: pd.DataFrame = c_analyzer.calculate_airspeed(speed_data=smoothed_data_grouped)
    data_cleaned: pd.DataFrame = c_analyzer.positive_vertical_speed(speed_data=data_airspeed)
    data_c_values: pd.DataFrame = c_analyzer.process_c_values(speed_data=data_cleaned)
    return data_c_values

def test_init(p_analyzer: pressure_analyzer.PressureAnalyzer) -> None:
    """
    Test the __init__ method of the PressureAnalyzer class.

    Parameters:
    - p_analyzer (PressureAnalyzer): The PressureAnalyzer object.

    Returns:
    - None.
    """
    assert p_analyzer is not None

def test_calculate_force_resultant(p_analyzer: pressure_analyzer.PressureAnalyzer) -> None:
    """
    Test the calculate_force_resultant method of the PressureAnalyzer class.

    Parameters:
    - p_analyzer (PressureAnalyzer): The PressureAnalyzer object.

    Returns:
    - None.
    """
    airspeed: float = 10.0
    Ca: float = 0.34
    Cw: float = 0.03
    force_resultant: float = p_analyzer.calculate_force_resultant(airspeed=airspeed, Ca=Ca, Cw=Cw)
    assert round(force_resultant, 4) == 860.2556

def test_calculate_dynamic_pressure(p_analyzer: pressure_analyzer.PressureAnalyzer) -> None:
    """
    Test the calculate_dynamic_pressure method of the PressureAnalyzer class.

    Parameters:
    - p_analyzer (PressureAnalyzer): The PressureAnalyzer object.

    Returns:
    - None.
    """
    airspeed: float = 10.0
    Ca: float = 0.34
    Cw: float = 0.03
    dynamic_pressure: float = p_analyzer.calculate_dynamic_pressure(airspeed=airspeed, Ca=Ca, Cw=Cw)
    assert round(dynamic_pressure, 4) == 109.107

def test_calculate_pressure_resultant(p_analyzer: pressure_analyzer.PressureAnalyzer) -> None:
    """
    Test the calculate_pressure_resultant method of the PressureAnalyzer class.

    Parameters:
    - p_analyzer (PressureAnalyzer): The PressureAnalyzer object.

    Returns:
    - None.
    """
    dynamic_pressure: float = 109.107
    pressure_resultant: float = p_analyzer.calculate_pressure_resultant(dynamic_pressure=dynamic_pressure)
    assert round(pressure_resultant, 4) == 79604.327

def test_process_pressure_data(p_analyzer: pressure_analyzer.PressureAnalyzer, dataset: pd.DataFrame) -> None:
    """
    Test the process_pressure_data method of the PressureAnalyzer class.

    Parameters:
    - p_analyzer (PressureAnalyzer): The PressureAnalyzer object.
    - dataset (pd.DataFrame): The dataset.

    Returns:
    - None.
    """
    data_processed: pd.DataFrame = p_analyzer.process_pressure_data(data=dataset)

    assert data_processed is not None
    
    assert "horizontal velocity [m/s]" in data_processed.columns
    assert "vertical velocity [m/s]" in data_processed.columns
    assert "airspeed [m/s]" in data_processed.columns
    assert "Ca [0.5]" in data_processed.columns
    assert "Cw [0.5]" in data_processed.columns
    assert "dynamic pressure [N/m^2]" in data_processed.columns
    assert "resultant pressure [N/m^2]" in data_processed.columns
