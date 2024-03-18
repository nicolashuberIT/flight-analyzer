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

def test_calculate_cA_approximation_original(analyzer):
    """
    Tests the calculate_cA_approximation_original method of the QualityAnalyzer class.
    
    Args:
    - analyzer (QualityAnalyzer): The QualityAnalyzer object to test.
    
    Returns:
    - None
    """
    assert round(27.911 * (10 ** (-1.929)), 4) == 0.3287
    assert analyzer.calculate_cA_approximation_original(10) == 27.911 * (10 ** (-1.929))
    assert analyzer.calculate_cA_approximation_original(20) == 27.911 * (20 ** (-1.929))
    assert analyzer.calculate_cA_approximation_original(30) == 27.911 * (30 ** (-1.929))
    assert analyzer.calculate_cA_approximation_original(40) == 27.911 * (40 ** (-1.929))
    assert analyzer.calculate_cA_approximation_original(50) == 27.911 * (50 ** (-1.929))

def test_calculate_cW_approximation_original(analyzer):
    """
    Tests the calculate_cW_approximation_original method of the QualityAnalyzer class.
    
    Args:
    - analyzer (QualityAnalyzer): The QualityAnalyzer object to test.
    
    Returns:
    - None
    """
    assert round(15.376 * (10 ** (-2.511)), 4) == 0.0474
    assert analyzer.calculate_cW_approximation_original(10) == 15.376 * (10 ** (-2.511))
    assert analyzer.calculate_cW_approximation_original(20) == 15.376 * (20 ** (-2.511))
    assert analyzer.calculate_cW_approximation_original(30) == 15.376 * (30 ** (-2.511))
    assert analyzer.calculate_cW_approximation_original(40) == 15.376 * (40 ** (-2.511))
    assert analyzer.calculate_cW_approximation_original(50) == 15.376 * (50 ** (-2.511))

def test_calculate_cA_approximation(analyzer):
    """
    Tests the calculate_cA_approximation method of the QualityAnalyzer class.
    
    Args:
    - analyzer (QualityAnalyzer): The QualityAnalyzer object to test.
    
    Returns:
    - None
    """
    assert round(35.8588 * (10 ** (-1.9862)), 4) == 0.3702
    assert analyzer.calculate_cA_approximation(10) == 35.8588 * (10 ** (-1.9862))
    assert analyzer.calculate_cA_approximation(20) == 35.8588 * (20 ** (-1.9862))
    assert analyzer.calculate_cA_approximation(30) == 35.8588 * (30 ** (-1.9862))
    assert analyzer.calculate_cA_approximation(40) == 35.8588 * (40 ** (-1.9862))
    assert analyzer.calculate_cA_approximation(50) == 35.8588 * (50 ** (-1.9862))

def test_calculate_cW_approximation(analyzer):
    """
    Tests the calculate_cW_approximation method of the QualityAnalyzer class.
    
    Args:
    - analyzer (QualityAnalyzer): The QualityAnalyzer object to test.
    
    Returns:
    - None
    """
    assert round(15.5624 * (10 ** (-2.5126)), 4) == 0.0478
    assert analyzer.calculate_cW_approximation(10) == 15.5624 * (10 ** (-2.5126))
    assert analyzer.calculate_cW_approximation(20) == 15.5624 * (20 ** (-2.5126))
    assert analyzer.calculate_cW_approximation(30) == 15.5624 * (30 ** (-2.5126))
    assert analyzer.calculate_cW_approximation(40) == 15.5624 * (40 ** (-2.5126))
    assert analyzer.calculate_cW_approximation(50) == 15.5624 * (50 ** (-2.5126))