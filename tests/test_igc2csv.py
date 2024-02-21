import os
import sys
import pytest
import numpy as np
import pandas as pd

# AI content (ChatGPT, 02/21/2024), verified and adapted by Nicolas Huber.
current_directory = os.path.dirname(__file__)
flight_analyzer_directory = os.path.abspath(os.path.join(current_directory, ".."))
sys.path.insert(0, flight_analyzer_directory)

from src.packages.IGC2CSV import IGC2CSV

TEST_FILE = f"{flight_analyzer_directory}/tests/assets/igc2csv/test_igc2csv.igc"
REFERENCE_FILE = f"{flight_analyzer_directory}/tests/assets/igc2csv/test_igc2csv.csv"


@pytest.fixture
def igc2csv() -> IGC2CSV:
    """
    Fixture to create a IGC2CSV object.

    Args:
    - None

    Returns:
    - igc2csv (IGC2CSV): IGC2CSV instance."""
    return IGC2CSV()


@pytest.fixture
def reference(reference_file: str = REFERENCE_FILE) -> pd.DataFrame:
    """
    Fixture to create a reference DataFrame.

    Args:
    - reference_file (str): Path to the reference file.

    Returns:
    - reference (pd.DataFrame): Reference DataFrame.
    """
    reference: pd.DataFrame = pd.read_csv(reference_file)
    return reference


def test_len(igc2csv: IGC2CSV, reference: pd.DataFrame) -> None:
    """
    Test if the length of the resulting DataFrame is correct.

    Args:
    - igc2csv: IGC2CSV object to be tested.
    - reference: Reference DataFrame to compare the result with.

    Returns:
    - None
    """
    result = igc2csv.process_files(TEST_FILE, False)
    result_flight_analyzer = igc2csv.export_to_flight_analyzer_format(result)
    assert len(result_flight_analyzer) == len(reference)


def test_dataframe(igc2csv: IGC2CSV) -> None:
    """
    Test if the resulting DataFrame has the correct properties.

    Args:
    - igc2csv: IGC2CSV object to be tested.

    Returns:
    - None
    """
    result = igc2csv.process_files(TEST_FILE, False)
    result_flight_analyzer = igc2csv.export_to_flight_analyzer_format(result)

    assert isinstance(result, pd.DataFrame)
    assert isinstance(result_flight_analyzer, pd.DataFrame)

    assert "timestamp [UTC]" in result_flight_analyzer.columns
    assert "relative altitude [m]" in result_flight_analyzer.columns
    assert "horizontal velocity [m/s]" in result_flight_analyzer.columns
    assert "vertical velocity [m/s]" in result_flight_analyzer.columns
    assert "distance to takeoff [km]" in result_flight_analyzer.columns
    assert "longitude" in result_flight_analyzer.columns
    assert "latitude" in result_flight_analyzer.columns

    assert result_flight_analyzer["timestamp [UTC]"].dtype == "datetime64[ns]"
    assert result_flight_analyzer["relative altitude [m]"].dtype == "int64"
    assert result_flight_analyzer["horizontal velocity [m/s]"].dtype == np.float64
    assert result_flight_analyzer["vertical velocity [m/s]"].dtype == np.float64
    assert result_flight_analyzer["distance to takeoff [km]"].dtype == np.float64
    assert result_flight_analyzer["longitude"].dtype == np.float64
    assert result_flight_analyzer["latitude"].dtype == np.float64


def check_speed_data_0(igc2csv: IGC2CSV) -> None:
    """
    Check if there's any 0 value in the horizontal speed data.

    Args:
    - igc2csv: IGC2CSV object to be tested.

    Returns:
    - None
    """
    result = igc2csv.process_files(TEST_FILE, False)
    result_flight_analyzer = igc2csv.export_to_flight_analyzer_format(result)
    assert result_flight_analyzer["horizontal velocity [m/s]"].all() > 0


def check_speed_data_1(igc2csv: IGC2CSV, reference) -> None:
    """
    Check if the speed data is equal to the reference data (rounded to 1 decimal place).

    Args:
    - igc2csv: IGC2CSV object to be tested.
    - reference: Reference DataFrame to compare the result with.

    Returns:
    - None
    """
    result = igc2csv.process_files(TEST_FILE, False)
    result_flight_analyzer = igc2csv.export_to_flight_analyzer_format(result)

    assert np.allclose(
        np.round(result_flight_analyzer["horizontal velocity [m/s]"], 1),
        np.round(reference["horizontal velocity [m/s]"], 1),
    )
    assert np.allclose(
        np.round(result_flight_analyzer["vertical velocity [m/s]"], 1),
        np.round(reference["vertical velocity [m/s]"], 1),
    )


def test_longitude(igc2csv: IGC2CSV, reference) -> None:
    """
    Test of the longitude data (rounded to 1 decimal place) is equal to the reference data (rounded to 1 decimal place).

    Args:
    - igc2csv: IGC2CSV object to be tested.
    - reference: Reference DataFrame to compare the result with.

    Returns:
    - None
    """
    result = igc2csv.process_files(TEST_FILE, False)
    result_flight_analyzer = igc2csv.export_to_flight_analyzer_format(result)
    assert np.allclose(
        np.round(result_flight_analyzer["longitude"], 1),
        np.round(reference["longitude"], 1),
    )


def test_latitude(igc2csv: IGC2CSV, reference) -> None:
    """
    Test of the latitude data (rounded to 1 decimal place) is equal to the reference data (rounded to 1 decimal place).

    Args:
    - igc2csv: IGC2CSV object to be tested.
    - reference: Reference DataFrame to compare the result with.

    Returns:
    - None
    """
    result = igc2csv.process_files(TEST_FILE, False)
    result_flight_analyzer = igc2csv.export_to_flight_analyzer_format(result)
    assert np.allclose(
        np.round(result_flight_analyzer["latitude"], 1),
        np.round(reference["latitude"], 1),
    )
