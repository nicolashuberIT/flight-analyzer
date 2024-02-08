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

ANGLE_PAST_THRESHOLD: int = 30
ANGLE_FUTURE_THRESHOLD: int = 30
ANGLE_THRESHOLD: int = 20
LINEAR_REGRESSION_THRESHOLD: float = 0.9

# categories

INDEX_STRAIGHT_LINE: Tuple[bool, str, int] = True, "Straight Line", 0
INDEX__ENDPOINT_STRAIGHT_LINE: Tuple[bool, str, int] = True, "Endpoint Straight Line", 1
INDEX_ENDPOINT_CURVE: Tuple[bool, str, int] = True, "Endpoint Curve", 2
INDEX_CURVE: Tuple[bool, str, int] = True, "Curve / Overlap / Error", 3
