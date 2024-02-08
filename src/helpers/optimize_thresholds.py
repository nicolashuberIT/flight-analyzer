# %%

import os
import sys
import pandas as pd
from typing import Tuple

# AI content (GitHub Copilot, 01/29/2024), verified and adapted by Nicolas Huber.
src_directory: str = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
sys.path.append(src_directory)

import constants as constants
import helpers.data_analyzer as data_analyzer
import algorithms.angle_analyzer as angle_analyzer


class ThresholdOptimizer:
    """
    Class to optimize thresholds for the models.
    """

    def __init__(
        self,
        csv_file: str,
        r_value_weight: float,
        p_value_weight: float,
        sdt_error_weight: float,
        limit: int,
        steps: int,
    ) -> None:
        """
        Initialize the class.

        Parameters:
        - csv_file (str): The path to the csv file.
        - r_value_weight (float): The weight of the r value.
        - p_value_weight (float): The weight of the p value.
        - sdt_error_weight (float): The weight of the standard error.
        - limit (int): The limit of the optimization.
        - steps (int): The steps of the optimization.

        Returns:
        - None.
        """
        self.csv_file = csv_file
        self.r_value_weight = r_value_weight
        self.p_value_weight = p_value_weight
        self.sdt_error_weight = sdt_error_weight
        self.limit = limit
        self.steps = steps
        self.future_threshold_optimized: int = 0
        self.past_threshold_optimized: int = 0

    def construct_data_analyzer(self) -> data_analyzer.DataAnalyzer:
        """
        Construct the data analyzer object.

        Parameters:
        - None.

        Returns:
        - DataAnalyzer: The data analyzer object.
        """
        DataAnalyzer: data_analyzer.DataAnalyzer = data_analyzer.DataAnalyzer(
            self.csv_file
        )
        return DataAnalyzer

    def calculate_score(self, values: Tuple[float, float, float]) -> float:
        """
        Calculate the score of the thresholds.

        Parameters:
        - values (Tuple[float, float, float]): The linear regression values to calculate the score from.

        Returns:
        - float: The score of the thresholds.
        """
        return (
            (values[0] * self.r_value_weight)
            - (values[1] * self.p_value_weight)
            - (values[2] * self.sdt_error_weight)
        )

    def test_thresholds(
        self,
        thresholds: Tuple[int, int],
        data: pd.DataFrame,
        DataAnalyzer: data_analyzer.DataAnalyzer,
        AngleAnalyzer: angle_analyzer.AngleAnalyzer,
    ) -> Tuple[int, int, float, float, float, float]:
        """
        Test the thresholds.

        Parameters:
        - thresholds (Tuple[int, int]): The thresholds to be tested.
        - data (pd.DataFrame): The data to be analyzed.
        - DataAnalyzer (data_analyzer.DataAnalyzer): The data analyzer object.
        - AngleAnalyzer (angle_analyzer.AngleAnalyzer): The angle analyzer object.

        Returns:
        - Tuple[int, int, float, float, float, float]: The results of the test. (ANGLE_PAST_THRESHOLD, ANBGLE_FUTURE_THRESHOLD, r_value, p_value, std_err, score)
        """
        data_processed = DataAnalyzer.process_data(
            data, AngleAnalyzer, thresholds[0], thresholds[1]
        )
        average_r_value = data_processed[data_processed["position_int"] == 0][
            "average_r_value"
        ].mean()
        average_p_value = data_processed[data_processed["position_int"] == 0][
            "average_p_value"
        ].mean()
        average_std_err = data_processed[data_processed["position_int"] == 0][
            "average_std_err"
        ].mean()
        linear_regression_values: Tuple[float, float, float] = (
            average_r_value,
            average_p_value,
            average_std_err,
        )
        score = self.calculate_score(linear_regression_values)
        return (
            thresholds[0],
            thresholds[1],
            average_r_value,
            average_p_value,
            average_std_err,
            score,
        )

    def optimize_thresholds(
        self,
        data: pd.DataFrame,
        DataAnalyzer: data_analyzer.DataAnalyzer,
        AngleAnalyzer: angle_analyzer.AngleAnalyzer,
    ) -> pd.DataFrame:
        """
        Optimize the thresholds.

        Parameters:
        - data (pd.DataFrame): The data to be analyzed.
        - DataAnalyzer (data_analyzer.DataAnalyzer): The data analyzer object.
        - AngleAnalyzer (angle_analyzer.AngleAnalyzer): The angle analyzer object.

        Returns:
        - pd.DataFrame: DataFrame with optimization data to be analyzed.
        """
        results: pd.DataFrame = pd.DataFrame(
            columns=[
                "angle_past_threshold",
                "angle_future_threshold",
                "average_r_value",
                "average_p_value",
                "average_std_err",
                "score",
            ]
        )

        num_iterations_i = (self.limit - 10) // self.steps
        num_iterations_j = (self.limit - 10) // self.steps
        total_iterations = num_iterations_i * num_iterations_j

        for i in range(10, self.limit, self.steps):
            for j in range(10, self.limit, self.steps):

                print(f"Iteration f = {i}, p = {j} from {total_iterations}:")
                print("--> Testing thresholds...")

                thresholds: Tuple[int, int] = (i, j)
                result: Tuple[int, int, float, float, float, float] = (
                    self.test_thresholds(thresholds, data, DataAnalyzer, AngleAnalyzer)
                )

                print("--> Results:")
                print(f"----> ANGLE_PAST_THRESHOLD: {result[0]}")
                print(f"----> ANGLE_FUTURE_THRESHOLD: {result[1]}")
                print(f"----> AVERAGE_R_VALUE: {result[2]}")
                print(f"----> AVERAGE_P_VALUE: {result[3]}")
                print(f"----> AVERAGE_STD_ERR: {result[4]}")
                print(f"----> SCORE: {result[5]}")
                print("--> Appending results...")
                print("--> Preparing next iteration...")
                print()

                results = pd.concat(
                    [
                        results,
                        pd.DataFrame(
                            {
                                "angle_past_threshold": [result[0]],
                                "angle_future_threshold": [result[1]],
                                "average_r_value": [result[2]],
                                "average_p_value": [result[3]],
                                "average_std_err": [result[4]],
                                "score": [result[5]],
                            }
                        ),
                    ],
                    ignore_index=True,
                )

        self.future_threshold_optimized = results.loc[
            results["score"].idxmax(), "angle_future_threshold"
        ]
        self.past_threshold_optimized = results.loc[
            results["score"].idxmax(), "angle_past_threshold"
        ]
        return results
