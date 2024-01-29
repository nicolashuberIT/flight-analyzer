# %%

import pandas as pd
import math
import matplotlib.pyplot as plt
from scipy.stats import linregress


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
        coordinates = df.values.tolist()

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
        angles = angles["angle"].tolist()
        average = sum(angles) / len(angles)

        if abs(average) < self.angle_threshold:
            status_average = True
        else:
            status_average = False

        if status_average:
            return True
        else:
            return False

    def analyze_linear_regression(self, df: pd.DataFrame) -> tuple:
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
    ) -> tuple:
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
        elif status_angle_past and status_regression_past:
            return False, "Endpunkt einer geraden Linie", 1
        elif status_angle_future and status_regression_future:
            return False, "Startpunkt einer geraden Linie", 2
        else:
            return False, "Kurve / Überschneidungspunkt", 3

    def visualize_points_2d(
        self, df: pd.DataFrame, relative: int = 0, linear: bool = False, title: str = ""
    ) -> None:
        """
        Visualizes the points of a flight on a map.

        Parameters:
        - df: the DataFrame containing the coordinates
        - relative: the index of the point to be highlighted
        - linear: whether to draw a linear regression or not
        - title: the title of the plot

        Returns:
        - None
        """
        fig = plt.figure(figsize=(12, 6))
        fig.set_facecolor("#F2F2F2")
        plt.scatter(df["longitude"], df["latitude"], s=1)
        if relative != 0:
            plt.plot(
                df["longitude"].iloc[relative],
                df["latitude"].iloc[relative],
                "bo",
            )
            plt.annotate(
                "Analysepunkt",
                (df["longitude"].iloc[relative], df["latitude"].iloc[relative]),
                textcoords="offset points",
                xytext=(0, 10),
                ha="center",
            )
        # AI content (GitHub Copilot, 01/29/2024), verified and adapted by Nicolas Huber.
        if linear:
            slope, intercept, r_value, p_value, std_err = linregress(
                df["longitude"], df["latitude"]
            )
            abline_values = [slope * i + intercept for i in df["longitude"]]
            plt.plot(df["longitude"], abline_values, "grey")
            plt.text(
                0.05,
                0.95,
                f"Steigung: {slope:.2f}\nOrdinatenabschnitt: {intercept:.2f}\nR-Quadrat: {r_value**2:.2f}\np-Wert: {p_value:.2f}\nStandardfehler: {std_err:.2f}",
                transform=plt.gca().transAxes,
                verticalalignment="top",
            )
        plt.xlabel("Längengrad")
        plt.ylabel("Breitengrad")
        if relative != 0:
            plt.title("Punktvariation")
        else:
            plt.title(f"Punktvariation mit linearer Regression ({title})")
        plt.show()

    # AI content (GitHub Copilot, 01/29/2024), verified and adapted by Nicolas Huber.
    def visualize_points_colored(self, df: pd.DataFrame, relative=0) -> None:
        """
        Visualizes the points of a flight on a map.

        Parameters:
        - df: the DataFrame containing the coordinates
        - relative: the index of the point to be highlighted

        Returns:
        - None
        """
        fig = plt.figure(figsize=(12, 6))
        fig.set_facecolor("#F2F2F2")
        scatter = plt.scatter(
            df["longitude"],
            df["latitude"],
            c=df["relative altitude [m]"],
            s=1,
            cmap="jet",
        )
        plt.colorbar(scatter, label="Relative Höhe [m]")
        if relative != 0:
            plt.scatter(
                df["longitude"].iloc[relative],
                df["latitude"].iloc[relative],
                c="b",
                marker="o",
            )
            plt.annotate(
                "Analysepunkt",
                (df["longitude"].iloc[relative], df["latitude"].iloc[relative]),
                textcoords="offset points",
                xytext=(0, 10),
                ha="center",
            )
        plt.xlabel("Längengrad")
        plt.ylabel("Breitengrad")
        plt.title("Punktvariation mit relativer Höhe")
        plt.show()

    def visualize_angles(
        self, past_angles: pd.DataFrame, future_angles: pd.DataFrame
    ) -> None:
        """
        Visualizes the angles of a flight on a map.

        Parameters:
        - past_angles: the DataFrame containing the past angles
        - future_angles: the DataFrame containing the future angles

        Returns:
        - None
        """
        len_past_angles = len(past_angles)
        past_angles.drop(past_angles.index[-1], inplace=True)
        fig = plt.figure(figsize=(12, 6))
        fig.set_facecolor("#F2F2F2")
        plt.plot(
            past_angles.index,
            past_angles["angle"],
            color="green",
            label="Vergangene Winkel",
        )
        future_angles.index = range(
            len_past_angles, len_past_angles + len(future_angles)
        )
        plt.plot(
            future_angles.index,
            future_angles["angle"],
            color="red",
            label="Zukünftige Winkel",
        )
        plt.axvline(
            x=len_past_angles, color="blue", linestyle="--", label="Analysepunkt"
        )
        plt.xlabel("Index [n]")
        plt.ylabel("Winkel [°]")
        plt.title("Winkelvariation")
        plt.legend(loc="upper right")
        plt.show()


# %%
