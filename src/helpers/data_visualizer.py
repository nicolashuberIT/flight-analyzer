import pandas as pd
import matplotlib.pyplot as plt
from scipy.stats import linregress


class DataVisualizer:
    """
    Class to visualize data generated using the AngleAnalyzer class, which can be found in the src/algorithms/angle_analyzer.py file.
    """

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
