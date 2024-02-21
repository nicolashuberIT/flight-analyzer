import numpy as np
import pandas as pd
from typing import Tuple
import matplotlib.pyplot as plt
from scipy.integrate import simps
from scipy.stats import linregress
from scipy.interpolate import interp1d
from scipy.interpolate import CubicSpline
from matplotlib.colors import ListedColormap


class DataVisualizer:
    """
    Class to visualize data generated using the AngleAnalyzer class, which can be found in the src/algorithms/angle_analyzer.py file.
    """

    def __init__(self, output_path: str = None) -> None:
        """
        Initialize the DataVisualizer object.

        Parameters:
        - output_path (str): The path to the output directory.

        Returns:
        - None.
        """
        self.output_path = output_path

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

    def visualize_altitude(self, df: pd.DataFrame) -> None:
        """
        Visualizes the altitude levels of a flight.

        Parameters:
        - df: the DataFrame containing the altitude levels

        Returns:
        - None
        """
        fig = plt.figure(figsize=(12, 6))
        fig.set_facecolor("#F2F2F2")

        plt.plot(df.index, df["relative altitude [m]"], label="Höhe")

        plt.xlabel("Index [n]")
        plt.ylabel("Höhe [m]")
        plt.title("Höhenvariation")
        plt.legend(loc="upper right")
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
    def visualize_score_by_data_loss(self, data: pd.DataFrame, index: int) -> None:
        """
        Plots the index of the iterations on the x-axis and both the score and the data_loss on separate y-axis (left and right).
        Adds a mark at the point where the difference between data_loss and score is the highest.

        Parameters:
        - data: the DataFrame containing the optimization results
        - index: the index of the best score

        Returns:
        - None
        """
        fig, ax1 = plt.subplots(figsize=(12, 6))
        fig.set_facecolor("#F2F2F2")

        ax1.plot(data.index, data["score"], label="Score", color="green")
        ax1.set_ylabel("Score")
        ax1.tick_params(axis="y")
        ax1.set_xlabel("Tabellenindex")

        ax2 = ax1.twinx()
        ax2.plot(
            data.index,
            data["data_loss"],
            label="Prozentualer Datenverlust",
            color="blue",
        )
        ax2.set_ylabel("Prozentualer Datenverlust")
        ax2.tick_params(axis="y")

        plt.axvline(
            x=index,
            color="red",
            linestyle="--",
            label="Bester Score bei minimalem Datenverlust",
        )

        handles1, labels1 = ax1.get_legend_handles_labels()
        handles2, labels2 = ax2.get_legend_handles_labels()
        handles = handles1 + handles2
        labels = labels1 + labels2

        plt.title("Score und Datenverlust")
        plt.legend(handles, labels)
        plt.show()

    def visualize_raw_speed_data(
        self,
        experimental_data: pd.DataFrame,
        theoretical_data: pd.DataFrame,
        std_error: float,
        title: str,
    ) -> None:
        """
        Plots the experimental and theoretical speed data and also includes the standard error for the experimental data.

        Parameters:
        - experimental_data: the DataFrame containing the experimental speed data
        - theoretical_data: the DataFrame containing the theoretical speed data
        - std_error: the standard error of the experimental speed data
        - title: the title of the plot

        Returns:
        - None
        """
        fig = plt.figure(figsize=(12, 6))
        fig.set_facecolor("#F2F2F2")

        # experimental data
        sorted_horizontal_experimental: pd.Series = experimental_data[
            "horizontal velocity [m/s]"
        ].sort_values()
        sorted_vertical_experimental: pd.Series = experimental_data[
            "vertical velocity [m/s]"
        ].loc[sorted_horizontal_experimental.index]

        cs_experimental: CubicSpline = CubicSpline(
            sorted_horizontal_experimental, sorted_vertical_experimental
        )

        x_values_experimental: np.ndarray = np.linspace(
            sorted_horizontal_experimental.min(),
            sorted_horizontal_experimental.max(),
            100,
        )

        plt.plot(
            x_values_experimental,
            cs_experimental(x_values_experimental),
            color="grey",
            label="Experimentelle Geschwindigkeitsdaten",
        )

        # std error for experimental data
        upper_bound = cs_experimental(x_values_experimental) + std_error
        lower_bound = cs_experimental(x_values_experimental) - std_error
        plt.fill_between(
            x_values_experimental,
            upper_bound,
            lower_bound,
            color="lightblue",
            alpha=0.5,
            label=f"Standardfehler ({std_error:.2f} m/s)",
        )

        # polynomial fit for experimental data (2nd degree)
        coefficients = np.polyfit(
            sorted_horizontal_experimental, sorted_vertical_experimental, 2
        )
        polynomial = np.poly1d(coefficients)
        x_values_experimental = np.linspace(
            sorted_horizontal_experimental.min(),
            sorted_horizontal_experimental.max(),
            100,
        )
        plt.plot(
            x_values_experimental,
            polynomial(x_values_experimental),
            color="blue",
            label="Experimentelle Geschwindigkeitspolare",
        )

        # cubic spline interpolation for theoretical data
        sorted_theoretical = theoretical_data.sort_values(
            by="horizontal velocity [m/s]"
        )
        cs_theoretical = CubicSpline(
            sorted_theoretical["horizontal velocity [m/s]"],
            sorted_theoretical["vertical velocity [m/s]"],
        )
        x_values_theoretical = np.linspace(
            sorted_theoretical["horizontal velocity [m/s]"].min(),
            sorted_theoretical["horizontal velocity [m/s]"].max(),
            100,
        )
        plt.plot(
            x_values_theoretical,
            cs_theoretical(x_values_theoretical),
            color="green",
            label="Theoretische Geschwindigkeitspolare",
        )

        plt.xlim(8.0, 15.7)
        plt.ylim(-2.75, -0.4)

        plt.title(title)
        plt.xlabel("Horizontalgeschwindigkeit [m/s]")
        plt.ylabel("Vertikalgeschwindigkeit [m/s]")
        plt.grid(True)
        plt.legend()
        plt.show()

    def visualize_speed_deviation(
        self,
        experimental_data: pd.DataFrame,
        theoretical_data: pd.DataFrame,
        speed_analyzer: object,
        title: str,
    ) -> Tuple[float, float, float, float]:
        """
        Plots the deviation between the experimental and theoretical speed data.

        Parameters:
        - experimental_data: the DataFrame containing the experimental speed data
        - theoretical_data: the DataFrame containing the theoretical speed data
        - title: the title of the plot
        - speed_analyzer: the SpeedAnalyzer object

        Returns:
        - Tuple[float, float, float, float]: mean_deviation, max_deviation, rms_deviation, area
        """
        fig: plt.Figure = plt.figure(figsize=(12, 6))
        fig.set_facecolor("#F2F2F2")

        # experimental data
        sorted_horizontal_experimental = experimental_data[
            "horizontal velocity [m/s]"
        ].sort_values()
        sorted_vertical_experimental = experimental_data["vertical velocity [m/s]"].loc[
            sorted_horizontal_experimental.index
        ]

        coefficients = np.polyfit(
            sorted_horizontal_experimental, sorted_vertical_experimental, 2
        )
        polynomial = np.poly1d(coefficients)
        x_values_experimental = np.linspace(
            sorted_horizontal_experimental.min(),
            sorted_horizontal_experimental.max(),
            100,
        )

        plt.plot(
            x_values_experimental,
            polynomial(x_values_experimental),
            color="blue",
            label="Experimentelle Geschwindigkeitspolare",
        )

        # theoretical data
        sorted_theoretical = theoretical_data.sort_values(
            by="horizontal velocity [m/s]"
        )
        cs_theoretical = CubicSpline(
            sorted_theoretical["horizontal velocity [m/s]"],
            sorted_theoretical["vertical velocity [m/s]"],
        )
        x_values_theoretical = np.linspace(
            sorted_theoretical["horizontal velocity [m/s]"].min(),
            sorted_theoretical["horizontal velocity [m/s]"].max(),
            100,
        )

        plt.plot(
            x_values_theoretical,
            cs_theoretical(x_values_theoretical),
            color="green",
            label="Theoretische Geschwindigkeitspolare",
        )

        # deviation area
        intersection_x = x_values_experimental
        intersection_y = polynomial(x_values_experimental)
        experimental_mask = (x_values_experimental >= 8) & (x_values_experimental <= 16)
        theoretical_mask = (x_values_theoretical >= 8) & (x_values_theoretical <= 16)

        area = simps(
            speed_analyzer.absolute_difference(
                x_values_experimental[experimental_mask],
                polynomial(x_values_experimental[experimental_mask]),
                x_values_theoretical[theoretical_mask],
                cs_theoretical(x_values_theoretical[theoretical_mask]),
            ),
            x_values_experimental[experimental_mask],
        )

        plt.fill_between(
            intersection_x,
            intersection_y,
            cs_theoretical(intersection_x),
            color="orange",
            alpha=0.5,
            label=f"Abweichungsbereich: {area:.2f}",
        )

        # deviation metrics
        deviations = np.abs(
            polynomial(x_values_experimental) - cs_theoretical(x_values_experimental)
        )
        mean_deviation = np.mean(deviations)
        max_deviation = np.max(deviations)
        rms_deviation = np.sqrt(np.mean(deviations**2))

        plt.xlim(8.0, 15.7)
        plt.ylim(-2.75, -0.4)

        plt.title(title)
        plt.xlabel("Horizontalgeschwindigkeit [m/s]")
        plt.ylabel("Vertikalgeschwindigkeit [m/s]")
        plt.grid(True)
        plt.legend()
        plt.show()

        return mean_deviation, max_deviation, rms_deviation, area

    def visualize_c_values_theoretical(
        self,
        theoretical_data: pd.DataFrame,
        key: str,
        title: str,
    ) -> None:
        """
        Plots the C values of the experimental and theoretical speed data.

        Parameters:
        - experimental_data: the DataFrame containing the experimental speed data
        - theoretical_data: the DataFrame containing the theoretical speed data
        - key: the key of the c values (either Ca [0.5] or Cw [1.0])
        - title: the title of the plot

        Returns:
        - None
        """
        fig = plt.figure(figsize=(12, 6))
        fig.set_facecolor("#F2F2F2")

        airspeed: pd.Series = theoretical_data["airspeed [m/s]"].sort_values()
        c_value: pd.Series = theoretical_data[key].loc[airspeed.index]

        cs: CubicSpline = CubicSpline(airspeed, c_value)

        x_values: np.ndarray = np.linspace(
            airspeed.min(),
            airspeed.max(),
            100,
        )

        plt.plot(
            x_values,
            cs(x_values),
            color="green",
            label=f"Theoretische C-Werte ({key})",
        )

        plt.xlim(8.0, 15.7)
        if key == "Cw [0.5]":
            plt.ylim(0.0, 0.13)
        else:
            plt.ylim(0.0, 0.6)

        plt.title(title)
        plt.xlabel("Anströmgeschwindigkeit [m/s]")
        plt.ylabel("C-Wert [0.5]")
        plt.grid(True)
        plt.legend()
        plt.show()

    # AI content (ChatGPT, 02/21/2024), verified and adapted by Nicolas Huber.
    def visualize_c_values(
        self,
        experimental_data: pd.DataFrame,
        theoretical_data: pd.DataFrame,
        key: str,
        title: str,
    ) -> None:
        """
        Plots the C values of the experimental and theoretical speed data.

        Parameters:
        - experimental_data: the DataFrame containing the experimental speed data
        - theoretical_data: the DataFrame containing the theoretical speed data
        - key: the key of the c values (either Ca [0.5] or Cw [1.0])
        - title: the title of the plot

        Returns:
        - None
        """
        fig = plt.figure(figsize=(12, 6))
        fig.set_facecolor("#F2F2F2")

        # experimental data
        x_exp = experimental_data["horizontal velocity [m/s]"]
        y_exp = experimental_data[key]
        plt.scatter(
            x_exp,
            y_exp,
            color="grey",
            label=f"Experimentelle C-Werte ({key})",
            s=3,
        )

        # power-law trendline for experimental data
        log_x = np.log10(x_exp)
        log_y = np.log10(y_exp)
        coeffs = np.polyfit(log_x, log_y, 1)
        poly = np.poly1d(coeffs)
        y_fit = lambda x: np.power(10, poly(np.log10(x)))
        plt.plot(x_exp, y_fit(x_exp), "b-", label="Annäherung der c-Werte")

        # theoretical data
        airspeed: pd.Series = theoretical_data["airspeed [m/s]"].sort_values()
        c_value: pd.Series = theoretical_data[key].loc[airspeed.index]

        cs: CubicSpline = CubicSpline(airspeed, c_value)

        x_values: np.ndarray = np.linspace(
            airspeed.min(),
            airspeed.max(),
            100,
        )

        plt.plot(
            x_values,
            cs(x_values),
            color="green",
            label=f"Theoretische C-Werte ({key})",
        )

        plt.xlim(8.0, 15.7)
        if key == "Cw [0.5]":
            plt.ylim(0.0, 0.13)
        else:
            plt.ylim(0.0, 0.6)

        plt.title(title)
        plt.xlabel("Anströmgeschwindigkeit [m/s]")
        plt.ylabel("C-Wert [0.5]")
        plt.grid(True)
        plt.legend()
        plt.show()

    # AI content (ChatGPT, 02/21/2024), verified and adapted by Nicolas Huber.
    def visualize_c_values_deviation(
        self,
        experimental_data: pd.DataFrame,
        theoretical_data: pd.DataFrame,
        key: str,
        title: str,
    ) -> Tuple[float, float, float, float]:
        """
        Plots the deviation between the experimental and theoretical C values, and calculates the deviation metrics.

        Parameters:
        - experimental_data: the DataFrame containing the experimental speed data
        - theoretical_data: the DataFrame containing the theoretical speed data
        - key: the key of the c values (either Ca [0.5] or Cw [1.0])
        - title: the title of the plot

        Returns:
        - Tuple[float, float, float, float]: mean_deviation, max_deviation, rms_deviation, area
        """
        fig: plt.Figure = plt.figure(figsize=(12, 6))
        fig.set_facecolor("#F2F2F2")

        # experimental data
        x_exp = experimental_data["horizontal velocity [m/s]"]
        y_exp = experimental_data[key]
        plt.scatter(
            x_exp,
            y_exp,
            color="grey",
            label=f"Experimentelle C-Werte ({key})",
            s=3,
        )

        # power-law trendline for experimental data
        log_x = np.log10(x_exp)
        log_y = np.log10(y_exp)
        coeffs = np.polyfit(log_x, log_y, 1)
        poly = np.poly1d(coeffs)
        y_fit = lambda x: np.power(10, poly(np.log10(x)))
        plt.plot(x_exp, y_fit(x_exp), "b-", label="Annäherung der c-Werte")

        power_law_equation = f"c(x) = {10**coeffs[1]:.2f} * x^{coeffs[0]:.2f}"
        plt.text(
            0.05,
            0.05,
            power_law_equation,
            transform=plt.gca().transAxes,
            fontsize=14,
            verticalalignment="bottom",
        )

        # theoretical data
        airspeed: pd.Series = theoretical_data["airspeed [m/s]"].sort_values()
        c_value: pd.Series = theoretical_data[key].loc[airspeed.index]

        cs: CubicSpline = CubicSpline(airspeed, c_value)

        x_values: np.ndarray = np.linspace(
            airspeed.min(),
            airspeed.max(),
            100,
        )

        plt.plot(
            x_values,
            cs(x_values),
            color="green",
            label=f"Theoretische C-Werte ({key})",
        )

        # deviation area
        intersection_x = x_exp
        intersection_y = y_fit(x_exp)
        experimental_mask = (x_exp >= 8) & (x_exp <= 16)
        theoretical_mask = (x_values >= 8) & (x_values <= 16)

        y_fit_func = interp1d(x_exp, y_fit(x_exp), fill_value="extrapolate")
        y_fit_theoretical_mask = y_fit_func(x_values[theoretical_mask])

        area = simps(
            np.abs(y_fit_theoretical_mask - cs(x_values[theoretical_mask])),
            x_values[theoretical_mask],
        )

        # deviation metrics
        y_fit_func = interp1d(x_exp, y_fit(x_exp), fill_value="extrapolate")
        y_fit_all = y_fit_func(x_values)

        deviations = np.abs(y_fit_all - cs(x_values))
        mean_deviation = np.mean(deviations)
        max_deviation = np.max(deviations)
        rms_deviation = np.sqrt(np.mean(deviations**2))

        plt.fill_between(
            intersection_x,
            intersection_y,
            cs(intersection_x),
            color="orange",
            alpha=0.5,
            label=f"Abweichungsbereich: {area:.2f}",
        )

        plt.xlim(8.0, 15.7)
        if key == "Cw [0.5]":
            plt.ylim(0.0, 0.13)
        else:
            plt.ylim(0.0, 0.6)

        plt.title(title)
        plt.xlabel("Anströmgeschwindigkeit [m/s]")
        plt.ylabel("c(x) [0.5]")
        plt.grid(True)
        plt.legend()
        plt.show()

        return mean_deviation, max_deviation, rms_deviation, area
