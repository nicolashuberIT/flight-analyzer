# %%

import pandas as pd
import math
from scipy.stats import linregress
from typing import List, Tuple


class AngleAnalyzer:
    """
    This class analyzes the angles between the points of a flight in order to determine whether they lie on a straight line or not.
    The process is based on the following steps:
    - check if the angles exceed a certain threshold
    - check if linear regression approves the result

    To test this script the example code can be used: src/helpers/execute_angle_analyzer.py
    """

    def __init__(
        self,
        csv_file: str,
        latest_threshold: int,
        future_threshold: int,
        angle_threshold: float,
    ) -> None:
        """
        Initializes the AngleAnalyzer class.

        Parameters:
        - csv_file: the path to the CSV file to be analyzed
        - latest_threshold: the number of coordinates to be analyzed in the past
        - future_threshold: the number of coordinates to be analyzed in the future
        - angle_threshold: the threshold for the angle analysis

        Returns:
        - None
        """
        self.csv_file: str = csv_file
        self.latest_threshold: int = latest_threshold
        self.future_threshold: int = future_threshold
        self.angle_threshold: float = angle_threshold

    def read_csv_file(self) -> pd.DataFrame:
        """
        Reads the CSV file and returns a Pandas DataFrame.

        Parameters:
        - None

        Returns:
        - A Pandas DataFrame
        """
        return pd.read_csv(self.csv_file)

    def extract_latest_coordinates(self, df: pd.DataFrame, i: int) -> pd.DataFrame:
        """
        Extract the latest n coordinates at the index i.

        Parameters:
        - df: the DataFrame to be filtered
        - i: the index of the coordinates to be extracted

        Returns:
        - A DataFrame containing the latest n coordinates at the index i
        """

        if i < 0 or i >= len(df):
            raise IndexError("Index out of range")

        if i < self.latest_threshold:
            return df.iloc[0 : i + 1]
        else:
            return df.iloc[i - self.latest_threshold + 1 : i + 1]

    def extract_future_coordinates(self, df: pd.DataFrame, i: int) -> pd.DataFrame:
        """
        Extract the future n coordinates at the index i.

        Parameters:
        - df: the DataFrame to be filtered
        - i: the index of the coordinates to be extracted

        Returns:
        - A DataFrame containing the future n coordinates at the index i
        """
        if i < 0 or i >= len(df):
            raise IndexError("Index out of range")

        if i + self.future_threshold >= len(df):
            return df.iloc[i:]
        else:
            return df.iloc[i : i + self.future_threshold]

    def calculate_angles(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Calculates the angles between the the starting point of a list and the other points of a flight using the formula angle = arctan((m1 - m2) / (1 + m1 * m2)).

        Parameters:
        - df: the DataFrame containing the coordinates

        Returns:
        - A DataFrame containing the angles between the points of a flight
        """
        coordinates: List[List[float]] = df.values.tolist()

        PX_1, PX_2 = coordinates[0][5], coordinates[1][5]
        PY_1, PY_2 = coordinates[0][6], coordinates[1][6]
        M_1 = (PY_2 - PY_1) / (PX_2 - PX_1)

        for i in range(len(coordinates)):
            if i == 0 or i == 1 or i >= len(coordinates) - 2:
                coordinates[i].append(0)
            else:
                try:
                    px_3 = coordinates[i][5]
                    py_3 = coordinates[i][6]
                    m_2 = (PY_1 - py_3) / (PX_1 - px_3)
                    angle = abs(math.degrees(math.atan((M_1 - m_2) / (1 + M_1 * m_2))))
                    coordinates[i].append(angle)
                except ZeroDivisionError:
                    coordinates[i].append(0)

        df = pd.DataFrame(
            coordinates,
            columns=[
                "timestamp",
                "altitude",
                "horizontal",
                "vertical",
                "distance",
                "longitude",
                "latitude",
                "angle",
            ],
        )
        return df

    def cut_zero_angles(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Cuts all rows with an angle of 0.

        Parameters:
        - df: the DataFrame containing the angles

        Returns:
        - A DataFrame containing the angles between the points of a flight
        """
        return df[df["angle"] != 0]

    def analyze_angles(self, angles: pd.DataFrame) -> bool:
        """
        Analyzes a point of a flight to determine whether it lies on a straight line or not, based on angle.

        Parameters:
        - df: the DataFrame containing the angles

        Returns:
        - True if the point lies on a straight line, False otherwise
        """
        angles_list: List[float] = angles["angle"].tolist()
        average = sum(angles_list) / len(angles_list)

        if abs(average) < self.angle_threshold:
            status_average = True
        else:
            status_average = False

        if status_average:
            return True
        else:
            return False

    def analyze_linear_regression(
        self, df: pd.DataFrame
    ) -> Tuple[bool, float, float, float, float, float]:
        """
        Analyzes a point of a flight to determine whether it lies on a straight line or not, based on linear regression.

        Parameters:
        - df: the DataFrame containing the coordinates

        Returns:
        - tuple containing the status of the analysis, the slope, the intercept, the r-value, the p-value and the standard error
        """
        slope, intercept, r_value, p_value, std_err = linregress(
            df["longitude"], df["latitude"]
        )
        if abs(r_value) > 0.9:
            status = True
        else:
            status = False

        return status, slope, intercept, r_value, p_value, std_err

    def analyze_data(
        self,
        status_angle_past: bool,
        status_regression_past: bool,
        status_angle_future: bool,
        status_regression_future: bool,
    ) -> Tuple[bool, str, int]:
        """
        Analyzes the data of a flight to determine whether it lies on a straight line or not.

        Parameters:
        - status_angle: the status of the angle analysis
        - status_regression: the status of the linear regression analysis

        Returns:
        - True if the point lies on a straight line, False otherwise
        """
        if (
            status_angle_past
            and status_regression_past
            and status_angle_future
            and status_regression_future
        ):
            return True, "Gerade", 0
        elif (status_angle_past and status_regression_past) and (
            not status_angle_future or not status_regression_future
        ):
            return False, "Endpunkt einer geraden Linie", 1
        elif (not status_angle_past and not status_regression_past) and (
            status_angle_future and status_regression_future
        ):
            return False, "Startpunkt einer geraden Linie", 2
        else:
            return False, "Kurve oder Überlappung", 3


# %%
