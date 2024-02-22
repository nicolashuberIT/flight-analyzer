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

    def calculate_cA_approximation(self, airspeed: float) -> float:
        """
        Calculates the approximation of the wing lift coefficient based on the analysis in c_values_analyzer.py"
        
        Args:
        - airspeed (float): The airspeed to calculate the wing lift coefficient for.
        
        Returns:
        - (float): The approximation of the wing lift coefficient.
        """
        return 35.86 * (airspeed ** (-1.99))
    
    def calculate_cW_approximation(self, airspeed: float) -> float:
        """
        Calculates the approximation of the wing drag coefficient based on the analysis in c_values_analyzer.py"
        
        Args:
        - airspeed (float): The airspeed to calculate the wing drag coefficient for.
        
        Returns:
        - (float): The approximation of the wing drag coefficient.
        """
        return 15.56 * (airspeed ** (-2.51))

    def analyze_quality(self, data: pd.DataFrame) -> Tuple[float, float, pd.DataFrame]:
        """
        Analyzes the quality of the stationary glide model by calculating the resulting force at the wing for every airspeed data point and comparing it to the expected force.
        
        Args:
        - data (pd.DataFrame): The data to analyze.

        Returns:
        - (float, float, pd.DataFrame): The mean deviation, the mean percentage deviation, and the data with the resulting force and deviation columns added.
        """
        data['resulting force [N]'] = data.apply(
            lambda row: self.p_analyzer.calculate_force_resultant(
                airspeed=row['airspeed [m/s]'],
                Ca=self.calculate_cA_approximation(row['airspeed [m/s]']),
                Cw=self.calculate_cW_approximation(row['airspeed [m/s]']),
            ),
            axis=1
        )

        expected_force: float = constants.MASS * constants.GRAVITY
        data['deviation [N]'] = expected_force - data['resulting force [N]']
        data['deviation percentage [%]'] = (data['resulting force [N]'] / expected_force) * 100

        mean_deviation: float = data['deviation [N]'].mean()
        deviation_percentage: float = data['deviation percentage [%]'].mean() - 100

        return mean_deviation, deviation_percentage, data
