from typing import Tuple

# general

VERSION: str = "0.1.0"
AUTHOR: str = "Nicolas Huber"
AUTHOR_EMAIL: str = "info@nicolas-huber.ch"
AUTHOR_URL: str = "https://nicolas-huber.ch"

# links

GITHUB_URL: str = "https://github.com/nicolashuberIT/flight-analyzer"
GITHUB_ACTIONS_URL: str = "https://github.com/nicolashuberIT/flight-analyzer/actions"

# algorithms

ANGLE_PAST_THRESHOLD: int = (
    215  # 80 by score (by data loss 60): optimized with limit 100, step 5 / adapted by eye under consideration of the optimization table
)
ANGLE_FUTURE_THRESHOLD: int = (
    25  # 35 by score (by data loss 15): optimized with limit 100, step 5 / adapted by eye under consideration of the optimization table
)
ANGLE_THRESHOLD: int = 20
LINEAR_REGRESSION_THRESHOLD: float = 0.9

# categories

INDEX_STRAIGHT_LINE: Tuple[bool, str, int] = True, "Straight Line", 0
INDEX_CURVE: Tuple[bool, str, int] = False, "Curve / Overlap / Error", 1

# optimization

R_VALUE_WEIGHT: float = 0.6
P_VALUE_WEIGHT: float = 0.3
STD_ERROR_WEIGHT: float = 0.1
OPTIMIZATION_LIMIT: int = 250
OPTIMIZATION_STEPS: int = 5
OPTIMIZATION_RUNTIME_ESTIMATION: int = 12
