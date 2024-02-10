# %%

import os
import sys
import pandas as pd

# AI content (GitHub Copilot, 01/29/2024), verified and adapted by Nicolas Huber.
src_directory: str = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
sys.path.append(src_directory)

from helpers import data_analyzer as data_analyzer
from algorithms import angle_analyzer as angle_analyzer
from helpers import data_visualizer as data_visualizer
from helpers import optimize_thresholds as optimizer
import constants as constants

CSV_FILE = "/Users/nicolas/Downloads/test_angle_analyzer.csv"

print("\n<------- START: CONDITIONS------> \n")

print("The automated threshold optimizer is executed for the following configuration:")
print(f"--> CSV file: {CSV_FILE}")
print(
    f"--> Runtime estimation: {constants.OPTIMIZATION_RUNTIME_ESTIMATION} seconds per iteration"
)
print(f"--> Optimization limit: {constants.OPTIMIZATION_LIMIT}")
print(f"--> Optimization step size: {constants.OPTIMIZATION_STEPS}")

print("\n<------- END: CONDITIONS ------>")
print("<------- START: INITIALISATION ------>\n")

Optimizer: optimizer.ThresholdOptimizer = optimizer.ThresholdOptimizer(
    CSV_FILE,
    constants.R_VALUE_WEIGHT,
    constants.P_VALUE_WEIGHT,
    constants.STD_ERROR_WEIGHT,
    constants.OPTIMIZATION_LIMIT,
    constants.OPTIMIZATION_STEPS,
    constants.OPTIMIZATION_RUNTIME_ESTIMATION,
)
AngleAnalyzer: angle_analyzer.AngleAnalyzer = angle_analyzer.AngleAnalyzer(
    CSV_FILE,
    constants.ANGLE_PAST_THRESHOLD,
    constants.ANGLE_FUTURE_THRESHOLD,
    constants.ANGLE_THRESHOLD,
    constants.LINEAR_REGRESSION_THRESHOLD,
)
DataAnalyzer: data_analyzer.DataAnalyzer = Optimizer.construct_data_analyzer()
Visualizer: data_visualizer.DataVisualizer = data_visualizer.DataVisualizer()

print("The initisalisation process is completed.")

print("\n<------- END: INITIALISATION ------>")
print("<------- START: IMPORTING DATA ------>\n")

data: pd.DataFrame = AngleAnalyzer.read_csv_file()
print("The data import is completed.")

print("\n<------- END: IMPORTING DATA ------>")
print("<------- START: OPTIMIZATION ------>\n")

optimization = Optimizer.optimize_thresholds(data, DataAnalyzer, AngleAnalyzer)
Optimizer.export_to_csv(optimization)

print("\n<------- END: OPTIMIZATION ------>")
print("<------- START: VISUALISATION ------>\n")

Visualizer.visualize_optimization_linear_regression(optimization)
Visualizer.visualize_score_by_data_loss(optimization)
Visualizer.visualize_optimization_score(optimization)
Visualizer.visualize_optimization_rvalues(optimization)
Visualizer.visualize_optimization_pvalues(optimization)
Visualizer.visualize_optimization_stderrs(optimization)

print("\n<------- END: VISUALISATION ------>")
print("<------- START: REPORT ------>\n")

print("Individuelle Threasholds mit dem besten Score:")
print(f"--> past_threshold_optimized: {Optimizer.past_threshold_optimized}")
print(f"--> future_threshold_optimized: {Optimizer.future_threshold_optimized}")
print()

print(
    "Unten findet sich eine tabellarische Übersicht der 5 besten Scores und deren Threasholds. Diese Angabe ist hier aussagekräftiger, da in der Analyse später für die Evaulierung eines Punktes sowohl die Zukunft als auch die Vergangenheit berücksichtigt werden und der Score somit die Interaktion der beiden Threasholds berücksichtigt."
)
print()
print(Optimizer.best_scores)
print()
print(
    f"The recommended thresholds are {Optimizer.best_scores.iloc[0, 0]} (angle_past_threshold) and {Optimizer.best_scores.iloc[0, 1]} (angle_future_threshold) with a score of {Optimizer.best_scores.iloc[0, 5]}."
)

print("\n<------- END: REPORT ------>")
print("<------- START: SYSTEM INFO ------>\n")

print(f"@ Version {constants.VERSION}")
print(f"@ Author {constants.AUTHOR}")
print(f"@ Author Email {constants.AUTHOR_EMAIL}")
print(f"@ Author URL {constants.AUTHOR_URL}")
print(f"@ GitHub URL {constants.GITHUB_URL}")

print("\n<------- END: SYSTEM INFO ------>")
print("Process finished with exit code 0")
