# %%

import os
import sys
import pandas as pd
from typing import Tuple

# AI content (GitHub Copilot, 01/29/2024), verified and adapted by Nicolas Huber.
src_directory: str = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
sys.path.append(src_directory)

import constants as constants


class CAnalyzer:
    """
    This class is responsible for analyzing the C values to simulate the stationary glide of a paraglider.
    """

    def __init__(self) -> None:
        """
        Constructor method.

        Args:
        - None

        Returns:
        - None
        """
        pass

    def positive_vertical_speed(self, speed_data: pd.DataFrame) -> pd.DataFrame:
        """
        This method makes all vertical speeds positive.

        Args:
        - speed_data: pd.DataFrame - The speed data of the paraglider.

        Returns:
        - pd.DataFrame - a new DataFrame containing positive vertical speeds.
        """
        speed_data["vertical velocity [m/s]"] = speed_data[
            "vertical velocity [m/s]"
        ].abs()
        return speed_data

    def calculate_airspeed(self, speed_data: pd.DataFrame) -> pd.DataFrame:
        """
        This method calculates the airspeed of the paraglider based on horizontal speed and vertical speed.

        Args:
        - speed_data: pd.DataFrame - The speed data of the paraglider.

        Returns:
        - pd.DataFrame - a new DataFrame containing horizontal speed, vertical speed and airspeed.
        """
        speed_data["airspeed [m/s]"] = (
            speed_data["horizontal velocity [m/s]"] ** 2
            + speed_data["vertical velocity [m/s]"] ** 2
        ) ** 0.5
        return speed_data

    def calculate_ca_value(
        self, cw: float, horizontal_speed: float, vertical_speed: float
    ) -> float:
        """
        This method calculates the Ca value of the paraglider based on the airspeed, the horizontal speed and the vertical speed.

        Args:
        - cw: float - The Cw value of the paraglider.
        - horizontal_speed: float - The horizontal speed of the paraglider.
        - vertical_speed: float - The vertical speed of the paraglider.

        Returns:
        - float - The Ca value.
        """
        return (cw * horizontal_speed) / vertical_speed

    def calculate_cw_value_simplified(
        self, horizontal_speed: float, vertical_speed: float, airspeed: float
    ) -> float:
        """
        This method calculates the Cw value of the paraglider based on the airspeed and the vertical speed.

        Args:
        - horizontal_speed: float - The horizontal speed of the paraglider.
        - vertical_speed: float - The vertical speed of the paraglider.
        - airspeed: float - The airspeed of the paraglider.

        Returns:
        - float - The Cw value.
        """
        return (constants.MASS * constants.GRAVITY * vertical_speed) / (
            constants.AIR_DENSITY
            * constants.WING_AREA
            * airspeed**2
            * (horizontal_speed + vertical_speed)
        )

    def calculate_cw_value_optimized(
        self, horizontal_speed: float, vertical_speed: float, airspeed: float
    ) -> float:
        """
        This method calculates the Cw value of the paraglider based on the airspeed, the horizontal speed and the vertical speed.

        Args:
        - horizontal_speed: float - The horizontal speed of the paraglider.
        - vertical_speed: float - The vertical speed of the paraglider.
        - airspeed: float - The airspeed of the paraglider.

        Returns:
        - float - The Cw value.
        """
        return (
            ((constants.MASS**2) * (constants.GRAVITY**2) * (vertical_speed**2))
            / (
                (constants.AIR_DENSITY**2)
                * (constants.WING_AREA**2)
                * (airspeed**4)
                * ((horizontal_speed**2) + (vertical_speed**2))
            )
        ) ** 0.5

    def process_c_values(
        self, speed_data: pd.DataFrame, algorithm=False
    ) -> pd.DataFrame:
        """
        This methods processes the c values of the paraglider and returns a new DataFrame containing the horizontal speed, vertical speed, airspeed, Cw and Ca values.

        Args:
        - speed_data: pd.DataFrame - The speed data of the paraglider, incuding airspeed
        - algorithm: bool - The algorithm to use for the Cw value calculation. If False, the simplified algorithm is used. If True, the optimized algorithm is used.

        Returns:
        - pd.DataFrame - a new DataFrame containing horizontal speed, vertical speed, airspeed, Cw and Ca values.
        """
        if algorithm:
            speed_data["Cw [0.5]"] = self.calculate_cw_value_optimized(
                speed_data["horizontal velocity [m/s]"],
                speed_data["vertical velocity [m/s]"],
                speed_data["airspeed [m/s]"],
            )
        else:
            speed_data["Cw [0.5]"] = self.calculate_cw_value_simplified(
                speed_data["horizontal velocity [m/s]"],
                speed_data["vertical velocity [m/s]"],
                speed_data["airspeed [m/s]"],
            )

        speed_data["Ca [0.5]"] = self.calculate_ca_value(
            speed_data["Cw [0.5]"],
            speed_data["horizontal velocity [m/s]"],
            speed_data["vertical velocity [m/s]"],
        )
        return speed_data

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
        score_original_ca_simplified: float,
        score_original_cw_simplified: float,
        score_experimental_ca_simplified: float,
        score_experimental_cw_simplified: float,
        score_original_ca_optimized: float,
        score_original_cw_optimized: float,
        score_experimental_ca_optimized: float,
        score_experimental_cw_optimized: float,
    ) -> None:
        """
        Print a report of the C values analysis.

        Args:
        - score_original_ca_simplified (float): Score for the original reference dataset (simplified algorithm)
        - score_original_cw_simplified (float): Score for the original reference dataset (simplified algorithm)
        - score_experimental_ca_simplified (float): Score for the experimental dataset (simplified algorithm)
        - score_experimental_cw_simplified (float): Score for the experimental dataset (simplified algorithm)
        - score_original_ca_optimized (float): Score for the original reference dataset (optimized algorithm)
        - score_original_cw_optimized (float): Score for the original reference dataset (optimized algorithm)
        - score_experimental_ca_optimized (float): Score for the experimental dataset (optimized algorithm)
        - score_experimental_cw_optimized (float): Score for the experimental dataset (optimized algorithm)

        Returns:
        - None
        """
        print(f"Scores:")
        print(
            f"--> The scores for the original reference dataset (simplified algorithm) are as follows:"
        )
        print(f"----> Ca: {score_original_ca_simplified}")
        print(f"----> Cw: {score_original_cw_simplified}")
        print(
            f"--> The scores for the experimental dataset (simplified algorithm) are as follows:"
        )
        print(f"----> Ca: {score_experimental_ca_simplified}")
        print(f"----> Cw: {score_experimental_cw_simplified}")
        print(
            f"--> The scores for the original reference dataset (optimized algorithm) are as follows:"
        )
        print(f"----> Ca: {score_original_ca_optimized}")
        print(f"----> Cw: {score_original_cw_optimized}")
        print(
            f"--> The scores for the experimental dataset (optimized algorithm) are as follows:"
        )
        print(f"----> Ca: {score_experimental_ca_optimized}")
        print(f"----> Cw: {score_experimental_cw_optimized}")
        print()

        print(f"Evaluation:")
        print(f"--> The lower the score, the better the algorithm.")
        print(f"--> The evaluation of the scores is as follows:")
        print(
            f"----> Relative to the original reference dataset (simplified algorithm), the experimental dataset (simplified algorithm) has a score of {abs(score_experimental_ca_simplified - score_original_ca_simplified)} for Ca and {abs(score_experimental_cw_simplified - score_original_cw_simplified)} for Cw, which translates to a quality increase of {((abs(score_experimental_ca_simplified - score_original_ca_simplified)) / abs(score_original_ca_simplified)) * 100}% for Ca and {((abs(score_experimental_cw_simplified - score_original_cw_simplified)) / abs(score_original_cw_simplified)) * 100}% for Cw."
        )
        print(
            f"----> Relative to the original reference dataset (optimized algorithm), the experimental dataset (optimized algorithm) has a score of {abs(score_experimental_ca_optimized - score_original_ca_optimized)} for Ca and {abs(score_experimental_cw_optimized - score_original_cw_optimized)} for Cw, which translates to a quality increase of {((abs(score_experimental_ca_optimized - score_original_ca_optimized)) / abs(score_original_ca_optimized)) * 100}% for Ca and {((abs(score_experimental_cw_optimized - score_original_cw_optimized)) / abs(score_original_cw_optimized)) * 100}% for Cw."
        )
        print()

        print(f"Final Score:")
        print(
            f"--> Relative to the original reference dataset (simplified algorithm), the experimental dataset (optimized algorithm) has a score of {abs(score_experimental_ca_optimized - score_original_ca_simplified)} for Ca and {abs(score_experimental_cw_optimized - score_original_cw_simplified)} for Cw, which translates to a quality increase of {((abs(score_experimental_ca_optimized - score_original_ca_simplified)) / abs(score_original_ca_simplified)) * 100}% for Ca and {((abs(score_experimental_cw_optimized - score_original_cw_simplified)) / abs(score_original_cw_simplified)) * 100}% for Cw."
        )
        print(
            f"--> The final quality increase of the experimental dataset (optimized algorithm) relative to the original reference dataset (simplified algorithm) is {abs((score_experimental_ca_optimized + score_experimental_cw_optimized - score_original_ca_simplified + score_original_cw_simplified) / (score_original_ca_simplified + score_original_cw_simplified)) * 100}%."
        )
