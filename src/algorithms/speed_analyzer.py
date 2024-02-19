# %%
import os
import sys
import numpy as np
import pandas as pd
from typing import List, Tuple
from scipy.signal import savgol_filter

# AI content (ChatGPT, 02/19/2024), verified and adapted by Nicolas Huber.
current_directory = os.path.dirname(os.path.abspath(__file__))
os.chdir(current_directory)
src_directory = os.path.join(current_directory, "..")
sys.path.append(src_directory)

import constants as constants
import packages.IGC2CSV as igc2csv
import helpers.data_analyzer as dataanalyzer
import algorithms.angle_analyzer as angleanalyzer


class SpeedAnalyzer:
    """
    SpeedAnalyzer class is responsible for processing the files and returning a dataframe with the results.
    """

    def __init__(self) -> None:
        """
        SpeedAnalyzer class constructor

        Args:
        - None

        Returns:
        - None
        """
        self.convertor: igc2csv.IGC2CSV = igc2csv.IGC2CSV()

    def process_raw_data(self, file_paths: List[str]) -> pd.DataFrame:
        """
        Process the files and return a dataframe with the results

        Args:
        - None

        Returns:
        - pd.DataFrame: Dataframe with the results
        """
        print("Processed files:")

        flight_data: pd.DataFrame = pd.DataFrame()
        count: int = len(file_paths)
        i: int = 0

        for file_path in file_paths:
            file_name = file_path.split("/")[-1]

            result = self.convertor.process_files(file_path, False)
            result_flight_analyzer = self.convertor.export_to_flight_analyzer_format(
                result
            )
            self.convertor.export_to_csv(result_flight_analyzer, f"{file_path}.csv")

            DataAnalyzer: dataanalyzer.DataAnalyzer = dataanalyzer.DataAnalyzer(
                csv_file_in=f"{file_path}.csv"
            )
            data: pd.DataFrame = DataAnalyzer.read_csv_data()

            AngleAnalyzer: angleanalyzer.AngleAnalyzer = (
                DataAnalyzer.construct_angle_analyzer()
            )
            data_processed: pd.DataFrame = DataAnalyzer.process_data(
                data=data, AngleAnalyzer=AngleAnalyzer
            )
            flight_data = pd.concat([flight_data, data_processed], ignore_index=True)
            print(f"--> Processed {i+1} of {count} files: {file_name}")

            i += 1

        for file_path in file_paths:
            os.remove(f"{file_path}.csv")

        return flight_data

    def filter_raw_data(
        self, data: pd.DataFrame, reference: bool = False
    ) -> pd.DataFrame:
        """
        Filter the raw data and return a dataframe with the results

        Args:
        - raw_data (pd.DataFrame): Raw data
        - reference (bool): Reference flag

        Returns:
        - pd.DataFrame: Dataframe with the results
        """
        if reference:
            data_sorted = data.sort_values(by="horizontal velocity [m/s]")
            data_filtered: pd.DataFrame = data_sorted[
                (data_sorted["horizontal velocity [m/s]"] > 8)
                & (data_sorted["horizontal velocity [m/s]"] < 15.5)
                & (data_sorted["vertical velocity [m/s]"] < 0)
            ]
        else:
            data_sorted = data.sort_values(by="horizontal velocity [m/s]")
            data_filtered: pd.DataFrame = data_sorted[
                (data_sorted["position_int"] == 0)
                & (data_sorted["horizontal velocity [m/s]"] > 8)
                & (data_sorted["horizontal velocity [m/s]"] < 15.5)
                & (data_sorted["vertical velocity [m/s]"] < 0)
            ]

        return data_filtered

    # explanation: http://www.statistics4u.info/fundstat_eng/cc_filter_savgolay.html
    def savgol_filter(self, data: pd.DataFrame) -> pd.DataFrame:
        """
        Apply a Savitzky-Golay filter to the data and return a dataframe with the results

        Args:
        - data (pd.DataFrame): Data
        - window (int): Window
        - order (int): Order

        Returns:
        - pd.DataFrame: Dataframe with the results
        """
        smoothed_horizontal_velocity: pd.DataFrame = savgol_filter(
            data["horizontal velocity [m/s]"],
            constants.SAVGOL_WINDOW_LENGTH,
            constants.SAVGOl_POLYNOMIAL_ORDER,
        )
        smoothed_vertical_velocity: pd.DataFrame = savgol_filter(
            data["vertical velocity [m/s]"],
            constants.SAVGOL_WINDOW_LENGTH,
            constants.SAVGOl_POLYNOMIAL_ORDER,
        )

        return pd.DataFrame(
            {
                "horizontal velocity [m/s]": smoothed_horizontal_velocity,
                "vertical velocity [m/s]": smoothed_vertical_velocity,
            }
        )

    def group_data(self, data: pd.DataFrame) -> pd.DataFrame:
        """
        Group the data by 0.1 m/s for the horizontal velocity and average the vertical velocity for each group

        Args:
        - data (pd.DataFrame): Data

        Returns:
        - pd.DataFrame: Dataframe with the results
        """
        data["horizontal velocity [m/s]"] = data["horizontal velocity [m/s]"].round(1)
        data_grouped = data.groupby("horizontal velocity [m/s]")
        return data_grouped["vertical velocity [m/s]"].mean().reset_index()

    def export_to_csv(self, data: pd.DataFrame, file_path: str) -> None:
        """
        Export the data to a csv file

        Args:
        - data (pd.DataFrame): Data
        - file_path (str): File path

        Returns:
        - None
        """
        data.to_csv(file_path, index=False)

    # AI content (ChatGPT, 02/19/2024), verified and adapted by Nicolas Huber.
    def absolute_difference(
        self, x_experimental, y_experimental, x_theoretical, y_theoretical
    ) -> float:
        """
        Calculate the absolute difference between the experimental and theoretical data

        Args:
        - x_experimental (float): Experimental x
        - y_experimental (float): Experimental y
        - x_theoretical (float): Theoretical x
        - y_theoretical (float): Theoretical y

        Returns:
        - float: Absolute difference
        """
        y_interp = np.interp(x_experimental, x_theoretical, y_theoretical)
        return np.abs(y_experimental - y_interp)

    # AI content (ChatGPT, 02/19/2024), verified and adapted by Nicolas Huber.
    def score_stats(self, stats: Tuple[float, float, float]) -> float:
        """
        Calculate a score based on the deviation stats.

        Args:
        - stats (Tuple[float, float, float]): Deviation stats

        Returns:
        - float: Score
        """
        weights = [0.5, 0.3, 0.2]
        weighted_sum = sum(weight * stat for weight, stat in zip(weights, stats))

        return weighted_sum

    def print_report(
        self,
        score_original: float,
        score_optimized: float,
        deviation_original: Tuple[float, float, float, float],
        deviation_optimized: Tuple[float, float, float, float],
        datasets: Tuple[
            pd.DataFrame, pd.DataFrame, pd.DataFrame, pd.DataFrame
        ],  # original_reference, original_reference_filtered, data_raw, smoothed_data_grouped
    ) -> None:
        """
        Print the report for the speed data analysis

        Args:
        - score_original (float): Original score
        - score_optimized (float): Optimized score

        Returns:
        - None
        """
        percentage_improvement = abs(
            ((score_original - score_optimized) / score_original) * 100
        )
        percentage_improvement_area = abs(
            ((deviation_original[3] - deviation_optimized[3]) / deviation_original[3])
            * 100
        )

        if score_original < score_optimized:
            print("--> Original dataset is closer to the theoretical curve.")
            print(
                f"----> The precision (deviation of theoretical polar) of the optimized dataset is worse by {percentage_improvement:.2f}% compared to the original dataset."
            )
            print(
                f"----> The area between the graphs within the limits 8 to 16 is bigger (worse) by {percentage_improvement_area:.2f}% compared to the original dataset."
            )
        elif score_original > score_optimized:
            print("--> Optimized dataset is closer to the theoretical curve.")
            print(
                f"----> The precision (deviation of theoretical polar) of this dataset improved by {percentage_improvement:.2f}% compared to the original dataset."
            )
            print(
                f"----> The area between the graphs within the limits 8 to 16 is smaller (better) by {percentage_improvement_area:.2f}% compared to the original dataset."
            )
        else:
            print("--> Are equal in terms of precision.")

        print()
        print("--> Number of processed datapoints: ")
        print(
            f"----> Original dataset (before processing): {len(datasets[0])} & after processing: {len(datasets[1])}"
        )
        print(
            f"----> Optimized dataset (before processing): {len(datasets[2])} & after processing: {len(datasets[3])}"
        )
