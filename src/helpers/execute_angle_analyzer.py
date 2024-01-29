# %%

import os
import sys

# AI content (GitHub Copilot, 01/29/2024), verified and adapted by Nicolas Huber.
src_directory = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
sys.path.append(src_directory)

import algorithms.angle_analyzer as angle_analyzer
import constants as constants

index = 230  # 200 expects linear, 230 expects end of straight line, 270 expects curve, 400 expects overlap,
print("Dataset")

Analyzer = angle_analyzer.AngleAnalyzer(
    "/Users/nicolas/Downloads/test.csv", 30, 30, constants.ANGLE_THRESHOLD
)
data = Analyzer.read_csv_file()
print("lenght: " + str(len(data)))
print()
print(data)

print()
print(
    "-------------------------------------------------------------------------------------------------"
)
print("Past Coordinates")

latest_coordinates = Analyzer.extract_latest_coordinates(data, index)
print("lenght: " + str(len(latest_coordinates)))
print()
print(latest_coordinates)

print()
print(
    "-------------------------------------------------------------------------------------------------"
)
print("Future Coordinates")

future_coordinates = Analyzer.extract_future_coordinates(data, index)
print("lenght: " + str(len(future_coordinates)))
print()
print(future_coordinates)

print()
print(
    "-------------------------------------------------------------------------------------------------"
)
print("Calculated Angles")
print()

angles_past = Analyzer.cut_zero_angles(Analyzer.calculate_angles(latest_coordinates))
angles_future = Analyzer.cut_zero_angles(Analyzer.calculate_angles(future_coordinates))

print("Past Angles")
print("lenght: " + str(len(angles_past)))
print()
print(angles_past)

print("Future Angles")
print("lenght: " + str(len(angles_future)))
print()
print(angles_future)

print()
print(
    "-------------------------------------------------------------------------------------------------"
)
print("Graphs")
print()

Analyzer.visualize_points_colored(data, index)
Analyzer.visualize_points_2d(latest_coordinates, 0, True, "Vergangenheit")
Analyzer.visualize_points_2d(future_coordinates, 0, True, "Zukunft")
Analyzer.visualize_angles(angles_past, angles_future)

print()
print(
    "-------------------------------------------------------------------------------------------------"
)
print("Log")
print()

status_angle_past = Analyzer.analyze_angles(angles_past)
status_angle_future = Analyzer.analyze_angles(angles_future)
(
    status_regression_past,
    slope_past,
    intercept_past,
    r_value_past,
    p_value_past,
    std_err_past,
) = Analyzer.analyze_linear_regression(latest_coordinates)
(
    status_regression_future,
    slope_future,
    intercept_future,
    r_value_future,
    p_value_future,
    std_err_future,
) = Analyzer.analyze_linear_regression(future_coordinates)

print("Angle Analysis")
print("Past: " + str(status_angle_past))
print("Future: " + str(status_angle_future))

print()

print("Past Linear Regression")
print("Status: " + str(status_regression_past))
print("Slope: " + str(slope_past))
print("Intercept: " + str(intercept_past))
print("R-Value: " + str(r_value_past))
print("P-Value: " + str(p_value_past))
print("Standard Error: " + str(std_err_past))

print()

print("Future Linear Regression")
print("Status: " + str(status_regression_future))
print("Slope: " + str(slope_future))
print("Intercept: " + str(intercept_future))
print("R-Value: " + str(r_value_future))
print("P-Value: " + str(p_value_future))
print("Standard Error: " + str(std_err_future))

print()

print("Data Analysis")
print(
    Analyzer.analyze_data(
        status_angle_past,
        status_regression_past,
        status_angle_future,
        status_regression_future,
    )
)

# %%
