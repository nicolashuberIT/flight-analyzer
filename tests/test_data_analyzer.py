import os
import sys
import pytest
import numpy as np
import pandas as pd

# AI content (GitHub Copilot, 01/25/2024), verified and adapted by Nicolas Huber.
src_directory: str = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
sys.path.append(src_directory)

import constants as constants
import helpers.data_analyzer as data_analyzer
import algorithms.angle_analyzer as angle_analyzer

CSV_FILE: str = "tests/assets/data_analyzer/test_data_analyzer.csv"


@pytest.fixture()
def analyzer() -> data_analyzer.DataAnalyzer:
    """
    Create a DataAnalyzer object for testing purposes.

    Parameters:
    - None.

    Returns:
    - DataAnalyzer: The DataAnalyzer object.
    """
    return data_analyzer.DataAnalyzer(CSV_FILE)


def test_init(analyzer: data_analyzer.DataAnalyzer) -> None:
    """
    Test the __init__ method of the DataAnalyzer class.

    Parameters:
    - analyzer (DataAnalyzer): The DataAnalyzer object.

    Returns:
    - None.
    """
    assert analyzer.csv_file == CSV_FILE, "The csv_file attribute is not set correctly."
    assert (
        analyzer.csv_file_out == f"{os.path.splitext(CSV_FILE)[0]}_analyzed.csv"
    ), "The csv_file_out attribute is not set correctly."


def test_construct_angle_analyzer(analyzer: data_analyzer.DataAnalyzer) -> None:
    """
    Test the construct_angle_analyzer method of the DataAnalyzer class.

    Parameters:
    - analyzer (DataAnalyzer): The DataAnalyzer object.

    Returns:
    - None.
    """
    angle_analyzer: angle_analyzer.AngleAnalyzer = analyzer.construct_angle_analyzer()  # type: ignore
    assert (
        angle_analyzer.csv_file == CSV_FILE
    ), "The csv_file attribute is not set correctly."
    assert (
        angle_analyzer.latest_threshold == constants.ANGLE_PAST_THRESHOLD
    ), "The latest_threshold attribute is not set correctly."
    assert (
        angle_analyzer.future_threshold == constants.ANGLE_FUTURE_THRESHOLD
    ), "The future_threshold attribute is not set correctly."
    assert (
        angle_analyzer.angle_threshold == constants.ANGLE_THRESHOLD
    ), "The angle_threshold attribute is not set correctly."
    assert (
        angle_analyzer.linear_regression_threshold
        == constants.LINEAR_REGRESSION_THRESHOLD,
        "The linear_regression_threshold attribute is not set correctly.",
    )


def test_read_csv_data(analyzer: data_analyzer.DataAnalyzer) -> None:
    """
    Test the read_csv_data method of the DataAnalyzer class.

    Parameters:
    - analyzer (DataAnalyzer): The DataAnalyzer object.

    Returns:
    - None.
    """
    data: pd.DataFrame = analyzer.read_csv_data()
    assert data.columns.tolist() == [
        "timestamp [UTC]",
        "relative altitude [m]",
        "horizontal velocity [m/s]",
        "vertical velocity [m/s]",
        "distance to takeoff [km]",
        "longitude",
        "latitude",
    ], "The columns of the dataset are not set correctly."
    assert len(data) == 3959, "The length of the dataset is not set correctly."


def test_process_data(analyzer: data_analyzer.DataAnalyzer) -> None:
    """
    Test the process_data method of the DataAnalyzer class.

    Parameters:
    - analyzer (DataAnalyzer): The DataAnalyzer object.

    Returns:
    - None.
    """
    data: pd.DataFrame = analyzer.read_csv_data()
    angle_analyzer: angle_analyzer.AngleAnalyzer = analyzer.construct_angle_analyzer()  # type: ignore
    data_processed: pd.DataFrame = analyzer.process_data(data, angle_analyzer)

    assert data_processed.columns.tolist() == [
        "timestamp [UTC]",
        "relative altitude [m]",
        "horizontal velocity [m/s]",
        "vertical velocity [m/s]",
        "distance to takeoff [km]",
        "longitude",
        "latitude",
        "status",
        "position_str",
        "position_int",
        "average_r_value",
        "average_p_value",
        "average_std_err",
    ], "The columns of the dataset are not set correctly."
    assert (
        type(data_processed["timestamp [UTC]"].iloc[1]) == str
    ), "The type of the timestamp [UTC] column is not set correctly."
    assert (
        type(data_processed["relative altitude [m]"].iloc[1])
        == np.float64  # assert np.float63 instead of float because of the pandas library, which uses numpy for float64
    ), "The type of the relative altitude [m] column is not set correctly."
    assert (
        type(data_processed["horizontal velocity [m/s]"].iloc[1]) == np.float64
    ), "The type of the horizontal velocity [m/s] column is not set correctly."
    assert (
        type(data_processed["vertical velocity [m/s]"].iloc[1]) == np.float64
    ), "The type of the vertical velocity [m/s] column is not set correctly."
    assert (
        type(data_processed["distance to takeoff [km]"].iloc[1]) == np.float64
    ), "The type of the distance to takeoff [km] column is not set correctly."
    assert (
        type(data_processed["longitude"].iloc[1]) == np.float64
    ), "The type of the longitude column is not set correctly."
    assert (
        type(data_processed["latitude"].iloc[1]) == np.float64
    ), "The type of the latitude column is not set correctly."
    assert (
        type(data_processed["status"].iloc[1]) == bool
    ), "The type of the status column is not set correctly."
    assert (
        type(data_processed["position_str"].iloc[1]) == str
    ), "The type of the position_str column is not set correctly."
    assert (
        type(data_processed["position_int"].iloc[1]) == int
    ), "The type of the position_int column is not set correctly."
    assert (
        type(data_processed["average_r_value"].iloc[1]) == np.float64
    ), "The type of the average_r_value column is not set correctly."
    assert (
        type(data_processed["average_p_value"].iloc[1]) == np.float64
    ), "The type of the average_p_value column is not set correctly."
    assert (
        type(data_processed["average_std_err"].iloc[1]) == np.float64
    ), "The type of the average_std_err column is not set correctly."


def test_export_to_csv(analyzer: data_analyzer.DataAnalyzer) -> None:
    """
    Test the export_to_csv method of the DataAnalyzer class.

    Parameters:
    - analyzer (DataAnalyzer): The DataAnalyzer object.

    Returns:
    - None.
    """
    data: pd.DataFrame = analyzer.read_csv_data()
    angle_analyzer: angle_analyzer.AngleAnalyzer = analyzer.construct_angle_analyzer()  # type: ignore
    data_processed: pd.DataFrame = analyzer.process_data(data, angle_analyzer)
    analyzer.export_to_csv(data_processed)
    assert os.path.exists(analyzer.csv_file_out), "The csv file was not created."
    os.remove(analyzer.csv_file_out)
