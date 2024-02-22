import os
import sys
import pytest
import numpy as np
import pandas as pd
from typing import List

# AI content (ChatGPT, 02/21/2024), verified and adapted by Nicolas Huber.
current_directory = os.path.dirname(__file__)
flight_analyzer_directory = os.path.abspath(os.path.join(current_directory, ".."))
sys.path.insert(0, flight_analyzer_directory)


import src.constants as constants
import src.helpers.quality_analyzer

@pytest.fixture
def analyzer():
    """
    Returns a QualityAnalyzer object.
    
    Args:
    - None
    
    Returns:
    - (QualityAnalyzer): A QualityAnalyzer object."""
    return src.helpers.quality_analyzer.QualityAnalyzer()

def test_calculate_cA_approximation(analyzer):
    """
    Tests the calculate_cA_approximation method of the QualityAnalyzer class.
    
    Args:
    - analyzer (QualityAnalyzer): The QualityAnalyzer object to test.
    
    Returns:
    - None
    """
    assert round(35.86 * (10 ** (-1.99)), 4) == 0.367
    assert analyzer.calculate_cA_approximation(10) == 35.86 * (10 ** (-1.99))
    assert analyzer.calculate_cA_approximation(20) == 35.86 * (20 ** (-1.99))
    assert analyzer.calculate_cA_approximation(30) == 35.86 * (30 ** (-1.99))
    assert analyzer.calculate_cA_approximation(40) == 35.86 * (40 ** (-1.99))
    assert analyzer.calculate_cA_approximation(50) == 35.86 * (50 ** (-1.99))

def test_calculate_cW_approximation(analyzer):
    """
    Tests the calculate_cW_approximation method of the QualityAnalyzer class.
    
    Args:
    - analyzer (QualityAnalyzer): The QualityAnalyzer object to test.
    
    Returns:
    - None
    """
    assert round(15.56 * (10 ** (-2.51)), 4) == 0.0481
    assert analyzer.calculate_cW_approximation(10) == 15.56 * (10 ** (-2.51))
    assert analyzer.calculate_cW_approximation(20) == 15.56 * (20 ** (-2.51))
    assert analyzer.calculate_cW_approximation(30) == 15.56 * (30 ** (-2.51))
    assert analyzer.calculate_cW_approximation(40) == 15.56 * (40 ** (-2.51))
    assert analyzer.calculate_cW_approximation(50) == 15.56 * (50 ** (-2.51))