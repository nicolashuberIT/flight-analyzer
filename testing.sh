#!/bin/bash

# Automatically generated shell script to run all test files with pytest. Check update_testing.sh for further reference

pytest -v "tests/test_angle_analyzer.py"
pytest -v "tests/test_c_values_analyzer.py"
pytest -v "tests/test_data_analyzer.py"
pytest -v "tests/test_file_converter.py"
pytest -v "tests/test_file_processor.py"
pytest -v "tests/test_igc2csv.py"
pytest -v "tests/test_optimize_thresholds.py"
pytest -v "tests/test_pressure_analyzer.py"
pytest -v "tests/test_speed_analyzer.py"
