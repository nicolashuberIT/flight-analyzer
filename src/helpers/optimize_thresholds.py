# %%

import os
import sys
import time
import warnings
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
        self.best_scores: pd.DataFrame
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
        warnings.simplefilter(
            action="ignore", category=FutureWarning
        )  # suppress FutureWarning

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

        n = 1
        start_time = time.time()
        num_iterations_i = (self.limit - 10) // self.steps
        num_iterations_j = (self.limit - 10) // self.steps
        total_iterations = num_iterations_i * num_iterations_j

        print(f"Total iterations: {total_iterations}")
        print(
            f"--> Expected duration: {round(total_iterations * 10, 2)} seconds, {round(total_iterations * 10 / 60, 2)} minutes, {round(total_iterations * 10 / 3600, 2)} hours."
        )
        print("--> Testing thresholds...")

        for i in range(10, self.limit, self.steps):
            for j in range(10, self.limit, self.steps):

                print(
                    f"----> Iteration {n} of {total_iterations}, testing thresholds: {i}, {j}, estimated time remaining: {round((total_iterations - n) * 10, 2)} seconds, {round((total_iterations - n) * 10 / 60, 2)} minutes, {round((total_iterations - n) * 10 / 3600, 2)} hours."
                )

                thresholds: Tuple[int, int] = (i, j)
                result: Tuple[int, int, float, float, float, float] = (
                    self.test_thresholds(thresholds, data, DataAnalyzer, AngleAnalyzer)
                )

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

                n += 1

        print("--> Processing results...")

        results = results.sort_values(by="score", ascending=False).reset_index(
            drop=True
        )
        self.best_scores = results.head(5)
        self.future_threshold_optimized = results.loc[
            results["score"].idxmax(), "angle_future_threshold"
        ]
        self.past_threshold_optimized = results.loc[
            results["score"].idxmax(), "angle_past_threshold"
        ]

        print("--> Results processed.")
        print(
            f"----> Total runtime: {round(time.time() - start_time, 2)} seconds, {round((time.time() - start_time) / 60, 2)} minutes, {round((time.time() - start_time) / 3600, 2)} hours."
        )
        return results

    def export_to_csv(self, results: pd.DataFrame) -> None:
        """
        Export the results to a csv file.

        Parameters:
        - results (pd.DataFrame): The results to be exported.

        Returns:
        - None.
        """
        results.to_csv(
            f"{os.path.splitext(self.csv_file)[0]}_optimized.csv",
            index=False,
        )
        print("--> Results exported to csv.")


# %%
