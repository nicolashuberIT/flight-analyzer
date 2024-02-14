from typing import Tuple

# general

AUTHOR: str = "Nicolas Huber"
AUTHOR_EMAIL: str = "info@nicolas-huber.ch"
AUTHOR_URL: str = "https://nicolas-huber.ch"
GITHUB_URL: str = "https://github.com/nicolashuberIT/flight-analyzer"
GITHUB_ACTIONS_URL: str = "https://github.com/nicolashuberIT/flight-analyzer/actions"

# algorithms

ANGLE_PAST_THRESHOLD: int = (
    80  # number of points in the past that are considered for the angle evaluation
)
ANGLE_FUTURE_THRESHOLD: int = (
    35  # number of points in the future that are considered for the angle evaluation
)
ANGLE_THRESHOLD: int = 20  # angle < 20° is considered as straight line
LINEAR_REGRESSION_THRESHOLD: float = 0.9  # r-value > 0.9 is considered as straight line

# categories

INDEX_STRAIGHT_LINE: Tuple[bool, str, int] = True, "Straight Line", 0
INDEX_CURVE: Tuple[bool, str, int] = False, "Curve / Overlap / Error", 1

# optimization

R_VALUE_WEIGHT: float = 0.6  # weight of the r-value in the optimization
P_VALUE_WEIGHT: float = 0.3  # weight of the p-value in the optimization
STD_ERROR_WEIGHT: float = 0.1  # weight of the standard error in the optimization
OPTIMIZATION_LIMIT: int = 30  # upper limit of optimization loops
OPTIMIZATION_STEPS: int = 5  # step size per optimization loop
OPTIMIZATION_RUNTIME_ESTIMATION: int = 120  # estimated runtime per loop in seconds
