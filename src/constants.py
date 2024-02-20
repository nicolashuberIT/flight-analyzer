from typing import Tuple

# general

AUTHOR: str = "Nicolas Huber"
AUTHOR_EMAIL: str = "info@nicolas-huber.ch"
AUTHOR_URL: str = "https://nicolas-huber.ch"
GITHUB_URL: str = "https://github.com/nicolashuberIT/flight-analyzer"
GITHUB_ACTIONS_URL: str = "https://github.com/nicolashuberIT/flight-analyzer/actions"

# data

THEORETICAL_REFERENCE_PATH: str = (
    "/Users/nicolas/Dropbox/3_Bildung/2_KZO/Stichwortverzeichnis/0 Maturarbeit/6 Wettbewerbe/1_SJf/3_Coaching/2_Projekt/software/flight-analyzer/docs/datasets/reference/theoretical_reference.csv"
)
ORIGINAL_REFERENCE_PATH: str = (
    "/Users/nicolas/Dropbox/3_Bildung/2_KZO/Stichwortverzeichnis/0 Maturarbeit/6 Wettbewerbe/1_SJf/3_Coaching/2_Projekt/software/flight-analyzer/docs/datasets/reference/original_reference.csv"
)

# algorithms

ANGLE_PAST_THRESHOLD: int = (
    95  # number of points in the past that are considered for the angle evaluation
)
ANGLE_FUTURE_THRESHOLD: int = (
    90  # number of points in the future that are considered for the angle evaluation
)
ANGLE_THRESHOLD: int = 20  # angle < 20° is considered as straight line
LINEAR_REGRESSION_THRESHOLD: float = 0.9  # r-value > 0.9 is considered as straight line

SAVGOL_WINDOW_LENGTH: int = 3  # window length of the Savitzky-Golay filter
SAVGOl_POLYNOMIAL_ORDER: int = 2  # polynomial order of the Savitzky-Golay filter

# categories

INDEX_STRAIGHT_LINE: Tuple[bool, str, int] = True, "Straight Line", 0
INDEX_CURVE: Tuple[bool, str, int] = False, "Curve / Overlap / Error", 1

# optimization

R_VALUE_WEIGHT: float = 0.6  # weight of the r-value in the optimization
P_VALUE_WEIGHT: float = 0.3  # weight of the p-value in the optimization
STD_ERROR_WEIGHT: float = 0.1  # weight of the standard error in the optimization

OPTIMIZATION_LIMIT: int = 200  # upper limit of optimization loops
OPTIMIZATION_STEPS: int = 5  # step size per optimization loop
OPTIMIZATION_RUNTIME_ESTIMATION: int = 6  # estimated runtime per loop in seconds
