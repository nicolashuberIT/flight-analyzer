import os
import sys
import pytest
import pandas as pd
from typing import Tuple

# AI content (ChatGPT, 02/21/2024), verified and adapted by Nicolas Huber.
current_directory = os.path.dirname(__file__)
flight_analyzer_directory = os.path.abspath(os.path.join(current_directory, ".."))
sys.path.insert(0, flight_analyzer_directory)

import src.constants as constants
import src.helpers.data_analyzer as dataanalyzer
import src.helpers.optimize_thresholds as optimize_thresholds

CSV_FILE: str = (
    f"{flight_analyzer_directory}/tests/assets/data_analyzer/test_data_analyzer.csv"
)
OPTIMIZATION_LIMIT: int = 20
OPTIMIZATION_STEPS: int = 5
OPTIMIZATION_COLUMNS: Tuple[str, str, str, str, str, str, str] = [
    "angle_past_threshold",
    "angle_future_threshold",
    "average_r_value",
    "average_p_value",
    "average_std_err",
    "score",
    "data_loss",
]


@pytest.fixture()
def optimizer() -> optimize_thresholds.ThresholdOptimizer:
    """
    Create a OptimizeThresholds object for testing purposes.

    Parameters:
    - None.

    Returns:
    - OptimizeThresholds: The OptimizeThresholds object.
    """
    return optimize_thresholds.ThresholdOptimizer(
        CSV_FILE,
        constants.R_VALUE_WEIGHT,
        constants.P_VALUE_WEIGHT,
        constants.STD_ERROR_WEIGHT,
        OPTIMIZATION_LIMIT,
        OPTIMIZATION_STEPS,
        constants.OPTIMIZATION_RUNTIME_ESTIMATION,
    )


# AI content (GitHub Copilot, 02/11/2024), verified and adapted by Nicolas Huber.
def test_init(optimizer: optimize_thresholds.ThresholdOptimizer) -> None:
    """
    Test the __init__ method of the OptimizeThresholds class.

    Parameters:
    - optimizer (OptimizeThresholds): The OptimizeThresholds object.

    Returns:
    - None.
    """
    assert (
        optimizer.csv_file == CSV_FILE
    ), "The csv_file attribute is not set correctly."
    assert (
        optimizer.r_value_weight == constants.R_VALUE_WEIGHT
    ), "The r_value_weight attribute is not set correctly."
    assert (
        optimizer.p_value_weight == constants.P_VALUE_WEIGHT
    ), "The p_value_weight attribute is not set correctly."
    assert (
        optimizer.std_error_weight == constants.STD_ERROR_WEIGHT
    ), "The std_error_weight attribute is not set correctly."
    assert (
        optimizer.limit == OPTIMIZATION_LIMIT
    ), "The limit attribute is not set correctly."
    assert (
        optimizer.steps == OPTIMIZATION_STEPS
    ), "The steps attribute is not set correctly."
    assert (
        optimizer.runtime_estimation == constants.OPTIMIZATION_RUNTIME_ESTIMATION
    ), "The runtime_estimation attribute is not set correctly."


# AI content (GitHub Copilot, 02/11/2024), verified and adapted by Nicolas Huber.
def test_construct_data_analyzer(
    optimizer: optimize_thresholds.ThresholdOptimizer,
) -> None:
    """
    Test the construct_data_analyzer method of the OptimizeThresholds class.

    Parameters:
    - optimizer (OptimizeThresholds): The OptimizeThresholds object.

    Returns:
    - None.
    """
    data_analyzer: pd.DataFrame = optimizer.construct_data_analyzer()
    assert data_analyzer is not None, "The data_analyzer is None."
    assert (
        data_analyzer.csv_file_in == CSV_FILE
    ), "The csv_file_in is not set correctly."


def test_calculate_score(optimizer: optimize_thresholds.ThresholdOptimizer) -> None:
    """
    Test the calculate_score method of the OptimizeThresholds class.

    Parameters:
    - optimizer (OptimizeThresholds): The OptimizeThresholds object.
    - SCORE_VALUES (Tuple[float, float, float]): The weights for the score calculation.

    Returns:
    - None.
    """
    score_values: Tuple[float, float, float] = (0.5, 0.3, 0.2)
    result: float = optimizer.calculate_score(score_values)

    assert (
        result
        == score_values[0] * constants.R_VALUE_WEIGHT
        - score_values[1] * constants.P_VALUE_WEIGHT
        - score_values[2] * constants.STD_ERROR_WEIGHT
    ), "The score is not calculated correctly."


def test_test_thresholds(
    optimizer: optimize_thresholds.ThresholdOptimizer,
) -> None:
    """
    Test the test_thresholds method of the OptimizeThresholds class.

    Parameters:
    - optimizer (OptimizeThresholds): The OptimizeThresholds object.

    Returns:
    - None.
    """
    DataAnalyzer: dataanalyzer.DataAnalyzer = dataanalyzer.DataAnalyzer(CSV_FILE)
    data = DataAnalyzer.read_csv_data()
    data_processed: Tuple[int, int, float, float, float, float, float] = (
        optimizer.test_thresholds(
            [constants.ANGLE_FUTURE_THRESHOLD, constants.ANGLE_PAST_THRESHOLD],
            data,
            DataAnalyzer,
        )
    )

    # AI content (GitHub Copilot, 02/11/2024), verified and adapted by Nicolas Huber.
    assert isinstance(data_processed, tuple), "The result is not a tuple."
    assert len(data_processed) == 7, "The result does not have the correct length."
    assert isinstance(data_processed[0], int), "The first element is not an integer."
    assert isinstance(data_processed[1], int), "The second element is not an integer."
    assert isinstance(data_processed[2], float), "The third element is not a float."
    assert isinstance(data_processed[3], float), "The fourth element is not a float."
    assert isinstance(data_processed[4], float), "The fifth element is not a float."
    assert isinstance(data_processed[5], float), "The sixth element is not a float."
    assert isinstance(data_processed[6], float), "The seventh element is not a float."


# AI content (GitHub Copilot, 02/11/2024), verified and adapted by Nicolas Huber.
def test_calculate_time_remaining(
    optimizer: optimize_thresholds.ThresholdOptimizer,
    n: int = 10,
    total_iterations: int = 100,
    previous: int = 12,
) -> None:
    """
    Test the calculate_time_remaining method of the OptimizeThresholds class.

    Parameters:
    - optimizer (OptimizeThresholds): The OptimizeThresholds object.

    Returns:
    - None.
    """
    result: float = optimizer.calculate_time_remaining(n, total_iterations, previous)
    assert isinstance(result, int), "The result is not an integer."


def test_optimize_thresholds(optimizer: optimize_thresholds.ThresholdOptimizer) -> None:
    """
    Test the optimize_thresholds method of the OptimizeThresholds class.

    Parameters:
    - optimizer (OptimizeThresholds): The OptimizeThresholds object.

    Returns:
    - None.
    """

    DataAnalyzer: dataanalyzer.DataAnalyzer = optimizer.construct_data_analyzer()
    data = DataAnalyzer.read_csv_data()
    results: pd.DataFrame = optimizer.optimize_thresholds(data, DataAnalyzer)

    # AI content (GitHub Copilot, 02/11/2024), verified and adapted by Nicolas Huber.
    assert results is not None, "The results are None."
    assert isinstance(results, pd.DataFrame), "The results are not a DataFrame."
    assert all(
        column in results.columns for column in OPTIMIZATION_COLUMNS
    ), "The results do not contain the correct columns."
    assert results[
        "score"
    ].is_monotonic_decreasing, "The results are not sorted by score."


def test_export_to_csv(optimizer: optimize_thresholds.ThresholdOptimizer) -> None:
    """
    Test the export_to_csv method of the OptimizeThresholds class.

    Parameters:
    - optimizer (OptimizeThresholds): The OptimizeThresholds object.

    Returns:
    - None.
    """
    DataAnalyzer: dataanalyzer.DataAnalyzer = optimizer.construct_data_analyzer()
    data = DataAnalyzer.read_csv_data()
    results: pd.DataFrame = optimizer.optimize_thresholds(data, DataAnalyzer)

    optimizer.export_to_csv(results)

    assert os.path.exists(
        f"{os.path.splitext(CSV_FILE)[0]}_optimized.csv"
    ), "The file was not created."

    os.remove(f"{os.path.splitext(CSV_FILE)[0]}_optimized.csv")


# AI content (GitHub Copilot, 02/11/2024), verified and adapted by Nicolas Huber.
def test_calculate_optimized_data_loss(
    optimizer: optimize_thresholds.ThresholdOptimizer,
) -> None:
    """
    Test the calculate_optimized_data_loss method of the OptimizeThresholds class.

    Parameters:
    - optimizer (OptimizeThresholds): The OptimizeThresholds object.

    Returns:
    - None.
    """
    DataAnalyzer: dataanalyzer.DataAnalyzer = optimizer.construct_data_analyzer()
    data = DataAnalyzer.read_csv_data()
    results: pd.DataFrame = optimizer.optimize_thresholds(data, DataAnalyzer)

    data_loss: int = optimizer.calculate_optimized_data_loss(results)

    assert isinstance(data_loss, int), "The data_loss is not a float."
