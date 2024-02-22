import os
import sys
import pandas as pd
from typing import Tuple

# AI content (GitHub Copilot, 01/29/2024), verified and adapted by Nicolas Huber.
src_directory: str = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
sys.path.append(src_directory)

import constants as constants


class PressureAnalyzer:
    """
    This class simulates the dynamic pressure at a paraglider wind.
    """

    def __init__(self) -> None:
        """
        Initialize the PressureAnalyzer class.
        """

    def calculate_force_resultant(self, airspeed: float, Ca: float, Cw: float) -> float:
        """
        Calculate resultant force at a paraglider wing.

        Args:
        - airspeed (float): The airspeed at the paraglider wing.
        - Ca (float): The lift coefficient at the paraglider wing.
        - Cw (float): The drag coefficient at the paraglider wing.

        Returns:
        - float: The resultant force at the paraglider wing.
        """
        return (
            constants.AIR_DENSITY
            * constants.WING_AREA
            * (airspeed**2)
            * ((Ca**2) + (Cw**2))
        ) ** 0.5

    def calculate_dynamic_pressure(
        self, airspeed: float, Ca: float, Cw: float
    ) -> float:
        """
        Calculate dynamic pressure at a paraglider wing.

        Args:
        - airspeed (float): The airspeed at the paraglider wing.
        - Ca (float): The lift coefficient at the paraglider wing.
        - Cw (float): The drag coefficient at the paraglider wing.

        Returns:
        - float: The dynamic pressure at the paraglider wing.
        """
        return self.calculate_force_resultant(airspeed, Ca, Cw) / (
            constants.WING_AREA * (((Ca**2) + (Cw**2)) ** 0.5)
        )

    def calculate_pressure_resultant(self, dynamic_pressure: float) -> float:
        """
        Calculate resultant pressure at a paraglider wing.

        Args:
        - dynamic_pressure (float): The dynamic pressure at the paraglider wing.

        Returns:
        - float: The resultant pressure at the paraglider wing.
        """
        return constants.STATIC_PRESSURE + dynamic_pressure

    def process_pressure_data(self, data: pd.DataFrame) -> pd.DataFrame:
        """
        Process a dataset containing speed data and c coefficients to calculate the dynamic pressure.

        Args:
        - data (pd.DataFrame): The dataset containing speed data and c coefficients.

        Returns:
        - pd.DataFrame: The dataset containing the speed data, c coefficients, the dynamic pressure and the resultant pressure.
        """
        data["dynamic pressure [N/m^2]"] = self.calculate_dynamic_pressure(
            data["airspeed [m/s]"], data["Ca [0.5]"], data["Cw [0.5]"]
        )
        data["resultant pressure [N/m^2]"] = self.calculate_pressure_resultant(
            data["dynamic pressure [N/m^2]"]
        )

        return data

    def export_to_csv(self, data: pd.DataFrame, path: str) -> None:
        """
        Export a dataset to a csv file.

        Args:
        - data (pd.DataFrame): The dataset to export.
        - path (str): The path to the csv file.
        """
        data.to_csv(path, index=False)
