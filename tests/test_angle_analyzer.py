import os
import sys
import math
import pytest
import pandas as pd

# AI content (ChatGPT, 02/21/2024), verified and adapted by Nicolas Huber.
current_directory = os.path.dirname(__file__)
flight_analyzer_directory = os.path.abspath(os.path.join(current_directory, ".."))
sys.path.insert(0, flight_analyzer_directory)

import src.constants as constants
from src.algorithms.angle_analyzer import AngleAnalyzer

PATH = (
    f"{flight_analyzer_directory}/tests/assets/angle_analyzer/test_angle_analyzer.csv"
)
INDEX_STRAIGHT_LINE = 1400
INDEX_CURVE = 270
INDEX_OVERLAP = 400
INDEX_END_CURVE = 1320
INDEX_END_STRAIGHT_LINE = 1200


@pytest.fixture()
def analyzer() -> AngleAnalyzer:
    """
    Returns an AngleAnalyzer object.

    Parameters:
    - None

    Returns:
    - A AngleAnalyzer object
    """
    return AngleAnalyzer(
        csv_file=PATH,
        latest_threshold=constants.ANGLE_PAST_THRESHOLD,
        future_threshold=constants.ANGLE_FUTURE_THRESHOLD,
        angle_threshold=constants.ANGLE_THRESHOLD,
        linear_regression_threshold=constants.LINEAR_REGRESSION_THRESHOLD,
    )


def test_init(analyzer: AngleAnalyzer) -> None:
    """
    Tests the __init__ method.

    Parameters:
    - analyzer: the AngleAnalyzer object to be tested

    Returns:
    - None
    """
    assert analyzer.csv_file == PATH, "The csv_file attribute is not correct."
    assert (
        analyzer.latest_threshold == constants.ANGLE_PAST_THRESHOLD
    ), "The past_threshold attribute is not correct."
    assert (
        analyzer.future_threshold == constants.ANGLE_FUTURE_THRESHOLD
    ), "The future_threshold attribute is not correct."
    assert (
        analyzer.angle_threshold == constants.ANGLE_THRESHOLD
    ), "The threshold attribute is not correct."


# AI content (GitHub Copilot, 01/29/2024), verified and adapted by Nicolas Huber.
def test_read_csv_file(analyzer: AngleAnalyzer) -> None:
    """
    Tests the read_csv_file method.

    Parameters:
    - analyzer: the AngleAnalyzer object to be tested

    Returns:
    - None
    """
    assert isinstance(
        analyzer.read_csv_file(), pd.DataFrame
    ), "The read_csv_file method does not return a DataFrame."


# AI content (GitHub Copilot, 01/29/2024), verified and adapted by Nicolas Huber.
def test_extract_latest_coordinates(analyzer: AngleAnalyzer) -> None:
    """
    Tests the extract_latest_coordinates method.

    Parameters:
    - analyzer: the AngleAnalyzer object to be tested

    Returns:
    - None
    """
    data = analyzer.read_csv_file()
    latest_coordinates = analyzer.extract_latest_coordinates(
        df=data, i=INDEX_STRAIGHT_LINE
    )
    assert (
        latest_coordinates.index[-1] == INDEX_STRAIGHT_LINE
    ), "The index of the DataFrame is not correct."


# AI content (GitHub Copilot, 01/29/2024), verified and adapted by Nicolas Huber.
def test_extract_future_coordinates(analyzer: AngleAnalyzer) -> None:
    """
    Tests the extract_future_coordinates method.

    Parameters:
    - analyzer: the AngleAnalyzer object to be tested

    Returns:
    - None
    """
    data = analyzer.read_csv_file()
    future_coordinates = analyzer.extract_future_coordinates(
        df=data, i=INDEX_STRAIGHT_LINE
    )
    assert (
        len(future_coordinates) == constants.ANGLE_FUTURE_THRESHOLD
    ), "The length of the DataFrame is not correct."
    assert (
        future_coordinates.index[0] == INDEX_STRAIGHT_LINE
    ), "The index of the DataFrame is not correct."


# AI content (GitHub Copilot, 01/29/2024), verified and adapted by Nicolas Huber.
def test_calculate_angles(analyzer: AngleAnalyzer) -> None:
    """
    Tests the calculate_angles method.

    Parameters:
    - analyzer: the AngleAnalyzer object to be tested

    Returns:
    - None
    """
    data = analyzer.read_csv_file()
    latest_coordinates = analyzer.extract_latest_coordinates(
        df=data, i=INDEX_STRAIGHT_LINE
    )
    angles_past = analyzer.cut_zero_angles(
        df=analyzer.calculate_angles(df=latest_coordinates)
    )
    index_coordinates = latest_coordinates.index[0]
    index_angles = angles_past.index[0]
    P1X, P2X, P3X = (
        latest_coordinates["longitude"][index_coordinates],
        latest_coordinates["longitude"][index_coordinates + 1],
        latest_coordinates["longitude"][index_coordinates + 2],
    )
    P1Y, P2Y, P3Y = (
        latest_coordinates["latitude"][index_coordinates],
        latest_coordinates["latitude"][index_coordinates + 1],
        latest_coordinates["latitude"][index_coordinates + 2],
    )
    assert (
        P1X == latest_coordinates["longitude"][index_coordinates]
    ), "The x1 coordinate is not correct."
    assert (
        P1Y == latest_coordinates["latitude"][index_coordinates]
    ), "The y1 coordinate is not correct."
    assert (
        P2X == latest_coordinates["longitude"][index_coordinates + 1]
    ), "The x2 coordinate is not correct."
    assert (
        P2Y == latest_coordinates["latitude"][index_coordinates + 1]
    ), "The y2 coordinate is not correct."
    assert round(P3X, 2) == round(
        angles_past["longitude"][index_angles], 2
    ), "The x3 coordinate does not match the row of the angle."
    assert round(P3Y, 2) == round(
        angles_past["latitude"][index_angles], 2
    ), "The y3 coordinate does not match the row of the angle."

    m1 = (P2Y - P1Y) / (P2X - P1X)
    m2 = (angles_past["latitude"][index_angles] - P1Y) / (
        angles_past["longitude"][index_angles] - P1X
    )
    angle = abs(math.degrees(math.atan((m1 - m2) / (1 + m1 * m2))))
    assert angle == angles_past["angle"][index_angles], "The angle is not correct."


# AI content (GitHub Copilot, 01/29/2024), verified and adapted by Nicolas Huber.
def test_cut_zero_angles(analyzer: AngleAnalyzer) -> None:
    """
    Tests the cut_zero_angles method.

    Parameters:
    - analyzer: the AngleAnalyzer object to be tested

    Returns:
    - None
    """
    data = analyzer.read_csv_file()
    latest_coordinates = analyzer.extract_latest_coordinates(
        df=data, i=INDEX_STRAIGHT_LINE
    )
    angles_past = analyzer.cut_zero_angles(
        df=analyzer.calculate_angles(df=latest_coordinates)
    )
    assert (
        0 not in angles_past["angle"].values
    ), "The dataset contains 0 degrees angles."


# AI content (GitHub Copilot, 01/29/2024), verified and adapted by Nicolas Huber.
def test_analyze_angles(analyzer: AngleAnalyzer) -> None:
    """
    Tests the analyze_angles method.

    Parameters:
    - analyzer: the AngleAnalyzer object to be tested

    Returns:
    - None
    """
    data = analyzer.read_csv_file()
    coordinates_straight_line = analyzer.extract_latest_coordinates(
        df=data, i=INDEX_STRAIGHT_LINE
    )
    data_coordinates_end_straight_line = analyzer.extract_latest_coordinates(
        df=data, i=INDEX_END_STRAIGHT_LINE
    )
    coordinates_curve = analyzer.extract_latest_coordinates(df=data, i=INDEX_CURVE)
    coordinates_overlap = analyzer.extract_latest_coordinates(df=data, i=INDEX_OVERLAP)
    coordinates_end_curve = analyzer.extract_latest_coordinates(
        df=data, i=INDEX_END_CURVE
    )

    angles_straight_line = analyzer.cut_zero_angles(
        df=analyzer.calculate_angles(df=coordinates_straight_line)
    )
    angles_end_straight_line = analyzer.cut_zero_angles(
        df=analyzer.calculate_angles(df=data_coordinates_end_straight_line)
    )
    angles_curve = analyzer.cut_zero_angles(
        df=analyzer.calculate_angles(df=coordinates_curve)
    )
    angles_overlap = analyzer.cut_zero_angles(
        df=analyzer.calculate_angles(df=coordinates_overlap)
    )
    angles_end_curve = analyzer.cut_zero_angles(
        df=analyzer.calculate_angles(df=coordinates_end_curve)
    )

    status_straight_line = analyzer.analyze_angles(angles=angles_straight_line)
    status_end_straight_line = analyzer.analyze_angles(angles=angles_end_straight_line)
    status_curve = analyzer.analyze_angles(angles=angles_curve)
    status_overlap = analyzer.analyze_angles(angles=angles_overlap)
    status_end_curve = analyzer.analyze_angles(angles=angles_end_curve)

    assert (
        status_straight_line == True
    ), "The status of the straight line is not correct."  # assertion determined by a test manually executed using the execute_angle_analyzer.ipynb notebook
    assert (
        status_end_straight_line == True
    ), "The status of the end of straight line is not correct."  # assertion determined by a test manually executed using the execute_angle_analyzer.ipynb notebook
    assert (
        status_curve == True
    ), "The status of the curve is not correct."  # assertion determined by a test manually executed using the execute_angle_analyzer.ipynb notebook
    assert (
        status_overlap == False
    ), "The status of the overlap is not correct."  # assertion determined by a test manually executed using the execute_angle_analyzer.ipynb notebook
    assert (
        status_end_curve == False
    ), "The status of the end of curve is not correct."  # assertion determined by a test manually executed using the execute_angle_analyzer.ipynb notebook


# AI content (GitHub Copilot, 01/29/2024), verified and adapted by Nicolas Huber.
def test_analyze_linear_regression(analyzer: AngleAnalyzer) -> None:
    """
    Tests the analyze_linear_regression method.

    Parameters:
    - analyzer: the AngleAnalyzer object to be tested

    Returns:
    - None
    """
    data = analyzer.read_csv_file()
    coordinates_straight_line = analyzer.extract_latest_coordinates(
        df=data, i=INDEX_STRAIGHT_LINE
    )
    data_coordinates_end_straight_line = analyzer.extract_latest_coordinates(
        df=data, i=INDEX_END_STRAIGHT_LINE
    )
    coordinates_curve = analyzer.extract_latest_coordinates(df=data, i=INDEX_CURVE)
    coordinates_overlap = analyzer.extract_latest_coordinates(df=data, i=INDEX_OVERLAP)
    coordinates_end_curve = analyzer.extract_latest_coordinates(
        df=data, i=INDEX_END_CURVE
    )

    angles_straight_line = analyzer.cut_zero_angles(
        df=analyzer.calculate_angles(df=coordinates_straight_line)
    )
    angles_end_straight_line = analyzer.cut_zero_angles(
        df=analyzer.calculate_angles(df=data_coordinates_end_straight_line)
    )
    angles_curve = analyzer.cut_zero_angles(
        df=analyzer.calculate_angles(df=coordinates_curve)
    )
    angles_overlap = analyzer.cut_zero_angles(
        df=analyzer.calculate_angles(df=coordinates_overlap)
    )
    angles_end_curve = analyzer.cut_zero_angles(
        df=analyzer.calculate_angles(df=coordinates_end_curve)
    )

    status_straight_line = analyzer.analyze_linear_regression(df=angles_straight_line)
    status_end_straight_line = analyzer.analyze_linear_regression(
        df=angles_end_straight_line
    )
    status_curve = analyzer.analyze_linear_regression(df=angles_curve)
    status_overlap = analyzer.analyze_linear_regression(df=angles_overlap)
    status_end_curve = analyzer.analyze_linear_regression(df=angles_end_curve)

    assert (
        status_straight_line[0] == True
    ), "The status of the straight line is not correct."  # assertion determined by a test manually executed using the execute_angle_analyzer.ipynb notebook
    assert (
        status_end_straight_line[0] == True
    ), "The status of the end of straight line is not correct."  # assertion determined by a test manually executed using the execute_angle_analyzer.ipynb notebook
    assert (
        status_curve[0] == False
    ), "The status of the curve is not correct."  # assertion determined by a test manually executed using the execute_angle_analyzer.ipynb notebook
    assert (
        status_overlap[0] == True
    ), "The status of the overlap is not correct."  # assertion determined by a test manually executed using the execute_angle_analyzer.ipynb notebook
    assert (
        status_end_curve[0] == False
    ), "The status of the end of curve is not correct."  # assertion determined by a test manually executed using the execute_angle_analyzer.ipynb notebook


# AI content (GitHub Copilot, 02/07/2024), verified and adapted by Nicolas Huber.
def test_analyze_data(analyzer: AngleAnalyzer) -> None:
    """
    Tests the analyze_data method.

    Parameters:
    - analyzer: the AngleAnalyzer object to be tested

    Returns:
    - None
    """
    data = analyzer.read_csv_file()
    latest_coordinates = analyzer.extract_latest_coordinates(
        df=data, i=INDEX_STRAIGHT_LINE
    )
    future_coordinates = analyzer.extract_future_coordinates(
        df=data, i=INDEX_STRAIGHT_LINE
    )
    angles_past = analyzer.cut_zero_angles(
        df=analyzer.calculate_angles(df=latest_coordinates)
    )
    angles_future = analyzer.cut_zero_angles(
        df=analyzer.calculate_angles(df=future_coordinates)
    )
    status_angle_past = analyzer.analyze_angles(angles=angles_past)
    status_angle_future = analyzer.analyze_angles(angles=angles_future)
    status_regression_past = analyzer.analyze_linear_regression(df=angles_past)
    status_regression_future = analyzer.analyze_linear_regression(df=angles_future)
    assert (
        analyzer.analyze_data(
            status_angle_past=status_angle_past,
            status_regression_past=status_regression_past,
            status_angle_future=status_angle_future,
            status_regression_future=status_regression_future,
        )
        == constants.INDEX_STRAIGHT_LINE
    ), "The status of the analysis is not correct."  # assertion determined by a test manually executed using the execute_angle_analyzer.ipynb notebook
