import os
import sys
import pandas as pd
from typing import Tuple

# AI content (GitHub Copilot, 01/29/2024), verified and adapted by Nicolas Huber.
src_directory: str = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
sys.path.append(src_directory)

import constants as constants
import algorithms.pressure_analyzer as pressure_analyzer

class QualityAnalyzer:
    """
    Analyzes the quality of the data analysis and the models.
    """

    def __init__(self) -> None:
        """
        Initializes the QualityAnalyzer object.

        Args:
        - None

        Returns:
        - None
        """
        self.p_analyzer: pressure_analyzer.PressureAnalyzer = pressure_analyzer.PressureAnalyzer()

    def calculate_cA_approximation_original(self, airspeed: float) -> float:
        """
        Calculates the approximation of the wing lift coefficient based on the original model in the paper dated 10/24/2022.
        - The original coefficient approximation can be found here: https://nicolas-huber.ch/docs/20221220_maturitaetsarbeit_fliegen-am-limit_public-version_nicolas-huber.pdf
        - Read more about the original model in the original paper on page 40, figure 56.

        Args:
        - airspeed (float): The airspeed to calculate the wing lift coefficient for.

        Returns:
        - (float): The approximation of the wing lift coefficient.
        """
        return 27.911 * (airspeed ** (-1.929))
    
    def calculate_cW_approximation_original(self, airspeed: float) -> float:
        """
        Calculates the approximation of the wing drag coefficient based on the original model in the paper dated 10/24/2022.
        - The original coefficient approximation can be found here: https://nicolas-huber.ch/docs/20221220_maturitaetsarbeit_fliegen-am-limit_public-version_nicolas-huber.pdf
        - Read more about the original model in the original paper on page 40, figure 56.

        Args:
        - airspeed (float): The airspeed to calculate the wing drag coefficient for.

        Returns:
        - (float): The approximation of the wing drag coefficient.
        """
        return 15.376 * (airspeed ** (-2.511))

    def calculate_cA_approximation(self, airspeed: float) -> float:
        """
        Calculates the approximation of the wing lift coefficient based on the analysis in c_values_analyzer.py"
        
        Args:
        - airspeed (float): The airspeed to calculate the wing lift coefficient for.
        
        Returns:
        - (float): The approximation of the wing lift coefficient.
        """
        return 35.8588 * (airspeed ** (-1.9862))
    
    def calculate_cW_approximation(self, airspeed: float) -> float:
        """
        Calculates the approximation of the wing drag coefficient based on the analysis in c_values_analyzer.py"
        
        Args:
        - airspeed (float): The airspeed to calculate the wing drag coefficient for.
        
        Returns:
        - (float): The approximation of the wing drag coefficient.
        """
        return 15.5624 * (airspeed ** (-2.5126))

    def analyze_quality(self, data: pd.DataFrame, model: bool = True) -> Tuple[float, float, pd.DataFrame]:
        """
        Analyzes the quality of the stationary glide model by calculating the resulting force at the wing for every airspeed data point and comparing it to the expected force.
        
        Args:
        - data (pd.DataFrame): The data to analyze.
        - model (bool): True if the new model should be used, False if the original model should be used.

        Returns:
        - (float, float, pd.DataFrame): The mean deviation, the mean percentage deviation, and the data with the resulting force and deviation columns added.
        """
        expected_force: float = (constants.MASS + constants.MASS_TRESHOLD)* constants.GRAVITY

        if model:
            data['resulting force [N]'] = data.apply(
                lambda row: self.p_analyzer.calculate_force_resultant(
                    airspeed=row['airspeed [m/s]'],
                    Ca=self.calculate_cA_approximation(row['airspeed [m/s]']),
                    Cw=self.calculate_cW_approximation(row['airspeed [m/s]']),
                ),
                axis=1
            )
        else:
            data['resulting force [N]'] = data.apply(
                lambda row: self.p_analyzer.calculate_force_resultant(
                    airspeed=row['airspeed [m/s]'],
                    Ca=self.calculate_cA_approximation_original(row['airspeed [m/s]']),
                    Cw=self.calculate_cW_approximation_original(row['airspeed [m/s]']),
                ),
                axis=1
            )

        data['deviation [N]'] = expected_force - data['resulting force [N]']
        data['deviation percentage [%]'] = (data['resulting force [N]'] / expected_force) * 100

        mean_deviation: float = data['deviation [N]'].mean()
        deviation_percentage: float = data['deviation percentage [%]'].mean() - 100

        return mean_deviation, deviation_percentage, data
