# %%

import pandas as pd
import math
import matplotlib.pyplot as plt


class AngleAnalyzer:
    """
    This class analyzes the angles between the points of a flight in order to determine whether they lie on a straight line or not.

    To run this script, use Jupyter Notebook and copy the following code:

    index = 200 # 200 expects true, 270 expects false
    print("Dataset")

    Analyzer = AngleAnalyzer("/Users/nicolas/Downloads/test.csv", 30, 15)
    data = Analyzer.read_csv_file()
    print("lenght: " + str(len(data)))
    print()
    print(data)

    print()
    print("-------------------------------------------------------------------------------------------------")
    print("Filtered Dataset")

    latest_coordinates = Analyzer.extract_latest_coordinates(data, index)
    print("lenght: " + str(len(latest_coordinates)))
    print()
    print(latest_coordinates)

    print()
    print("-------------------------------------------------------------------------------------------------")
    print("Calculated Angles")
    print()

    angles = Analyzer.cut_zero_angles(Analyzer.calculate_angles(latest_coordinates))
    print(angles)

    print()
    print("-------------------------------------------------------------------------------------------------")
    print("Graphs")
    print()

    Analyzer.visualize_points(data, index)
    Analyzer.visualize_points(latest_coordinates)
    Analyzer.visualize_angles(angles)

    print()
    print("-------------------------------------------------------------------------------------------------")
    print("Log")
    print()

    status = Analyzer.analyze_point(angles)
    Analyzer.print_report(status)
    """

    def __init__(
        self, csv_file: str, latest_threshold: int, future_threshold: int
    ) -> None:
        """
        Initializes the AngleAnalyzer class.

        Parameters:
        - csv_file: the path to the CSV file to be analyzed
        - latest_threshold: the number of coordinates to be analyzed in the past
        - future_threshold: the number of coordinates to be analyzed in the future

        Returns:
        - None
        """
        self.csv_file: str = csv_file
        self.latest_threshold: int = latest_threshold
        self.future_threshold: int = future_threshold

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
            return df.iloc[i : i + self.future_threshold + 1]

    def calculate_angles(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Calculates the angles between the the starting point of a list and the other points of a flight using the formula angle = arctan((m1 - m2) / (1 + m1 * m2)).

        Parameters:
        - df: the DataFrame containing the coordinates

        Returns:
        - A DataFrame containing the angles between the points of a flight
        """
        coordinates = df.values.tolist()

        m_1 = (coordinates[0][6] - coordinates[1][6]) / coordinates[0][5] - coordinates[
            1
        ][5]

        for i in range(len(coordinates)):
            if i == 0 or i == 1:
                coordinates[i].append(0)
            elif i >= len(coordinates) - 2:
                coordinates[i].append(0)
            else:
                m_2 = (coordinates[i + 2][6] - coordinates[i + 1][6]) / coordinates[
                    i + 2
                ][5] - coordinates[i + 1][5]
                angle = math.atan((m_1 - m_2) / (1 + m_1 * m_2))
                coordinates[i].append(angle)

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

    def analyze_point(self, angles: pd.DataFrame) -> bool:
        """
        Analyzes a point of a flight to determine whether it lies on a straight line or not.

        Parameters:
        - df: the DataFrame containing the angles

        Returns:
        - True if the point lies on a straight line, False otherwise
        """
        angles = angles["angle"].tolist()
        average = sum(angles) / len(angles)

        if abs(average) > 0.00002:
            return True
        else:
            return False

    def print_report(self, status: bool) -> None:
        """
        Prints a report of the analysis.

        Parameters:
        - df: the DataFrame containing the angles

        Returns:
        - None
        """
        print("Report:")
        print("-------")
        print("The flight is straight: " + str(status))

    def visualize_points(self, df: pd.DataFrame, relative=0) -> None:
        """
        Visualizes the points of a flight on a map.

        Parameters:
        - df: the DataFrame containing the coordinates

        Returns:
        - None
        """
        plt.scatter(df["longitude"], df["latitude"], s=1)
        if relative != 0:
            plt.plot(
                df["longitude"].iloc[relative],
                df["latitude"].iloc[relative],
                "bo",
            )
            plt.annotate(
                "Relative",
                (df["longitude"].iloc[relative], df["latitude"].iloc[relative]),
                textcoords="offset points",
                xytext=(0, 10),
                ha="center",
            )
        plt.xlabel("Longitude")
        plt.ylabel("Latitude")
        plt.title("Point variation in dataset")
        plt.show()

    def visualize_angles(self, df: pd.DataFrame) -> None:
        """
        Visualizes the angles of a flight on a map.

        Parameters:
        - df: the DataFrame containing the angles

        Returns:
        - None
        """
        plt.plot(df["angle"])
        plt.xlabel("Index [n]")
        plt.ylabel("Angle [°]")
        plt.title("Angle variation in dataset")
        plt.show()


# %%
