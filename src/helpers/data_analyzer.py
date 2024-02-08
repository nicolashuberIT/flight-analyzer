# %%

import os
import sys
import pandas as pd
from typing import Tuple

# AI content (GitHub Copilot, 01/29/2024), verified and adapted by Nicolas Huber.
src_directory: str = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
sys.path.append(src_directory)

import constants as constants
import algorithms.angle_analyzer as angle_analyzer


class DataAnalyzer:
    """
    Class to loop through the data and analyze it by applying the AngleAnalyzer class. The foundation of this class is a csv file containing coordinates, speed data etc. The output will be a new csv file containing the same data but flagged with an index:

    - 0 = point lies on a straight line
    - 1 = end point of a straight line
    - 2 = end point of curve
    - 3 = point lies on curve
    """

    def __init__(self, csv_file: str) -> None:
        self.csv_file = csv_file
        self.csv_file_out = f"{os.path.splitext(csv_file)[0]}_analyzed.csv"

    def construct_angle_analyzer(self) -> angle_analyzer.AngleAnalyzer:
        """
        Construct the angle analyzer object.

        Parameters:
        - None.

        Returns:
        - AngleAnalyzer: The angle analyzer object.
        """
        AngleAnalyzer: angle_analyzer.AngleAnalyzer = angle_analyzer.AngleAnalyzer(
            self.csv_file,
            constants.ANGLE_PAST_THRESHOLD,
            constants.ANGLE_FUTURE_THRESHOLD,
            constants.ANGLE_THRESHOLD,
            constants.LINEAR_REGRESSION_THRESHOLD,
        )
        return AngleAnalyzer

    def read_csv_data(self) -> pd.DataFrame:
        """
        Read the csv file containing the data to be analyzed.

        Parameters:
        - None.

        Returns:
        - pd.DataFrame: The dataset to be analyzed.
        """
        self.data = pd.read_csv(self.csv_file)
        return self.data

    def process_data(
        self, data: pd.DataFrame, AngleAnalyzer: angle_analyzer.AngleAnalyzer
    ) -> pd.DataFrame:
        """
        Apply the AngleAnalyzer to every line of the dataset and append three new columns to the dataset: status, position_str, and position_int

        Parameters:
        - data (pd.DataFrame): The dataset to be analyzed.

        Returns:
        - pd.DataFrame: The dataset with the new columns.
        """

        data_processed = pd.DataFrame(
            columns=[
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
            ]
        )

        for i in range(
            constants.ANGLE_PAST_THRESHOLD, len(data) - constants.ANGLE_FUTURE_THRESHOLD
        ):
            latest_coordinates = AngleAnalyzer.extract_latest_coordinates(data, i)
            future_coordinates = AngleAnalyzer.extract_future_coordinates(data, i)

            angles_past: pd.DataFrame = AngleAnalyzer.cut_zero_angles(
                AngleAnalyzer.calculate_angles(latest_coordinates)
            )
            angles_future: pd.DataFrame = AngleAnalyzer.cut_zero_angles(
                AngleAnalyzer.calculate_angles(future_coordinates)
            )

            status_angle_past: bool = AngleAnalyzer.analyze_angles(angles_past)
            status_angle_future: bool = AngleAnalyzer.analyze_angles(angles_future)
            (
                status_regression_past,
                slope_past,
                intercept_past,
                r_value_past,
                p_value_past,
                std_err_past,
            ) = AngleAnalyzer.analyze_linear_regression(latest_coordinates)
            (
                status_regression_future,
                slope_future,
                intercept_future,
                r_value_future,
                p_value_future,
                std_err_future,
            ) = AngleAnalyzer.analyze_linear_regression(future_coordinates)

            status: Tuple[bool, str, int] = AngleAnalyzer.analyze_data(
                status_angle_past,
                status_regression_past,
                status_angle_future,
                status_regression_future,
            )

            data_processed.loc[i, "timestamp [UTC]"] = data.iloc[i]["timestamp [UTC]"]
            data_processed.loc[i, "relative altitude [m]"] = data.iloc[i][
                "relative altitude [m]"
            ]
            data_processed.loc[i, "horizontal velocity [m/s]"] = data.iloc[i][
                "horizontal velocity [m/s]"
            ]
            data_processed.loc[i, "vertical velocity [m/s]"] = data.iloc[i][
                "vertical velocity [m/s]"
            ]
            data_processed.loc[i, "distance to takeoff [km]"] = data.iloc[i][
                "distance to takeoff [km]"
            ]
            data_processed.loc[i, "longitude"] = data.iloc[i]["longitude"]
            data_processed.loc[i, "latitude"] = data.iloc[i]["latitude"]
            data_processed.loc[i, "status"] = status[0]
            data_processed.loc[i, "position_str"] = status[1]
            data_processed.loc[i, "position_int"] = status[2]
            data_processed.loc[i, "average_r_value"] = (
                r_value_past + r_value_future
            ) / 2
            data_processed.loc[i, "average_p_value"] = (
                p_value_past + p_value_future
            ) / 2
            data_processed.loc[i, "average_std_err"] = (
                std_err_past + std_err_future
            ) / 2

        return data_processed

    def export_to_csv(self, data_processed: pd.DataFrame) -> None:
        """
        Export the processed data to a new csv file.

        Parameters:
        - data_processed (pd.DataFrame): The processed data.

        Returns:
        - None.
        """
        data_processed.to_csv(self.csv_file_out, index=False)
        print(f"Data exported to {self.csv_file_out}")
