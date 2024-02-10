import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap
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

    # AI content (ChatGPT, 02/08/2024), verified and adapted by Nicolas Huber.
    def visualize_points_position(self, data: pd.DataFrame) -> None:
        """
        Visualizes the position of the points of a flight and colors them by position category.

        Parameters:
        - data: the DataFrame containing the coordinates and the position category

        Returns:
        - None
        """

        colors = ["green", "purple"]
        custom_cmap = ListedColormap(colors)

        fig = plt.figure(figsize=(12, 6))
        fig.set_facecolor("#F2F2F2")
        plt.scatter(
            data["longitude"],
            data["latitude"],
            c=data["position_int"],
            cmap=custom_cmap,
            s=1,
        )
        plt.xlabel("Längengrad")
        plt.ylabel("Breitengrad")
        plt.title("Punktvariation mit Position und Kategorisierung")

        plt.legend(
            handles=[
                plt.Line2D(
                    [0],
                    [0],
                    marker="o",
                    color="w",
                    markerfacecolor="green",
                    markersize=10,
                    label="Punkt auf einer Geraden",
                ),
                plt.Line2D(
                    [0],
                    [0],
                    marker="o",
                    color="w",
                    markerfacecolor="purple",
                    markersize=10,
                    label="Punkt auf einer Kurve / Überlappung / Fehler",
                ),
            ]
        )

        plt.show()

    # AI content (ChatGPT, 02/08/2024), verified and adapted by Nicolas Huber.
    def visualize_optimization_linear_regression(self, data: pd.DataFrame) -> None:
        """
        Visualizes the optimization process.

        Parameters:
        - data: the DataFrame containing the optimization results

        Returns:
        - None
        """
        fig = plt.figure(figsize=(12, 6))
        fig.set_facecolor("#F2F2F2")
        plt.plot(data["score"], data["average_r_value"], label="r_value")
        plt.plot(data["score"], data["average_p_value"], label="p_value")
        plt.plot(data["score"], data["average_std_err"], label="sdt_error")
        plt.xlabel("Score")
        plt.ylabel("Wert")
        plt.title("Optimierung der Thresholds")
        plt.legend(loc="lower right")
        plt.show()

    # AI content (ChatGPT, 02/08/2024), verified and adapted by Nicolas Huber.
    def visualize_optimization_score(self, data: pd.DataFrame) -> None:
        """
        Visualizes the optimization process.

        Parameters:
        - data: the DataFrame containing the optimization results

        Returns:
        - None
        """
        fig = plt.figure(figsize=(12, 6))
        fig.set_facecolor("#F2F2F2")
        plt.scatter(
            data["angle_past_threshold"],
            data["score"],
            label="past_threshold",
        )
        plt.scatter(
            data["angle_future_threshold"],
            data["score"],
            label="future_threshold",
        )
        plt.xlabel("Threshold")
        plt.ylabel("Score")
        plt.title("Score in Abhängigkeit der Thresholds")
        plt.legend(loc="lower right")
        plt.show()

    # AI content (ChatGPT, 02/08/2024), verified and adapted by Nicolas Huber.
    def visualize_optimization_rvalues(self, data: pd.DataFrame) -> None:
        """
        Visualizes the optimization process.

        Parameters:
        - data: the DataFrame containing the optimization results

        Returns:
        - None
        """
        fig = plt.figure(figsize=(12, 6))
        fig.set_facecolor("#F2F2F2")
        plt.scatter(
            data["angle_past_threshold"],
            data["average_r_value"],
            label="past_threshold",
        )
        plt.scatter(
            data["angle_future_threshold"],
            data["average_r_value"],
            label="future_threshold",
        )
        plt.xlabel("Threshold")
        plt.ylabel("r_value")
        plt.title("r_value in Abhängigkeit der Thresholds")
        plt.legend(loc="lower right")
        plt.show()

    # AI content (ChatGPT, 02/08/2024), verified and adapted by Nicolas Huber.
    def visualize_optimization_pvalues(self, data: pd.DataFrame) -> None:
        """
        Visualizes the optimization process.

        Parameters:
        - data: the DataFrame containing the optimization results

        Returns:
        - None
        """
        fig = plt.figure(figsize=(12, 6))
        fig.set_facecolor("#F2F2F2")
        plt.scatter(
            data["angle_past_threshold"],
            data["average_p_value"],
            label="past_threshold",
        )
        plt.scatter(
            data["angle_future_threshold"],
            data["average_p_value"],
            label="future_threshold",
        )
        plt.xlabel("Threshold")
        plt.ylabel("p_value")
        plt.title("p_value in Abhängigkeit der Thresholds")
        plt.legend(loc="lower right")
        plt.show()

    # AI content (ChatGPT, 02/08/2024), verified and adapted by Nicolas Huber.
    def visualize_optimization_stderrs(self, data: pd.DataFrame) -> None:
        """
        Visualizes the optimization process.

        Parameters:
        - data: the DataFrame containing the optimization results

        Returns:
        - None
        """
        fig = plt.figure(figsize=(12, 6))
        fig.set_facecolor("#F2F2F2")
        plt.scatter(
            data["angle_past_threshold"],
            data["average_std_err"],
            label="past_threshold",
        )
        plt.scatter(
            data["angle_future_threshold"],
            data["average_std_err"],
            label="future_threshold",
        )
        plt.xlabel("Threshold")
        plt.ylabel("std_error")
        plt.title("std_error in Abhängigkeit der Thresholds")
        plt.legend(loc="lower right")
        plt.show()

    # AI content (ChatGPT, 02/10/2024), verified and adapted by Nicolas Huber.
    def visualize_score_by_data_loss(self, data: pd.DataFrame) -> None:
        """
        Plots the index of the iterations on the x-axis and both the score and the data_loss on separate y-axis (left and right).
        Adds a mark at the point where the difference between data_loss and score is the highest.

        Parameters:
        - data: the DataFrame containing the optimization results

        Returns:
        - None
        """
        fig, ax1 = plt.subplots(figsize=(12, 6))
        fig.set_facecolor("#F2F2F2")

        ax1.plot(data.index, data["score"], label="Score", color="green")
        ax1.set_ylabel("Score")
        ax1.tick_params(axis="y")

        ax2 = ax1.twinx()
        ax2.plot(
            data.index,
            data["data_loss"],
            label="Prozentualer Datenverlust",
            color="blue",
        )
        ax2.set_ylabel("Prozentualer Datenverlust")
        ax2.tick_params(axis="y")

        # normalize the data_loss and score to the same scale so both can be compared between 0 and 1

        data_normalized = data.copy()
        data_normalized["score"] = (data["score"] - data["score"].min()) / (
            data["score"].max() - data["score"].min()
        )
        data_normalized["data_loss"] = (data["data_loss"] - data["data_loss"].min()) / (
            data["data_loss"].max() - data["data_loss"].min()
        )

        # calculate the index with the highest difference between data_loss and score

        max_distance_index = 0
        max_distance = 0

        for index, row in data_normalized.iterrows():
            distance = abs(row["score"] - row["data_loss"])
            if distance > max_distance and abs(row["score"]) > abs(row["data_loss"]):
                max_distance = distance
                max_distance_index = index

        plt.axvline(
            x=max_distance_index,
            color="red",
            linestyle="--",
            label="Bester Score bei minimalem Datenverlust",
        )

        handles1, labels1 = ax1.get_legend_handles_labels()
        handles2, labels2 = ax2.get_legend_handles_labels()
        handles = handles1 + handles2
        labels = labels1 + labels2

        plt.xlabel("Tabellenindex")
        plt.title("Score und Datenverlust")
        plt.legend(handles, labels)
        plt.show()
