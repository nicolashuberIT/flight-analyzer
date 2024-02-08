# %%

from ..algorithms import angle_analyzer


class DataAnalyzer:
    """
    Class to loop through the data and analyze it by applying the AngleAnalyzer class. The foundation of this class is a csv file containing coordinates, speed data etc. The output will be a new csv file containing the same data but flagged with an index:

    - 0 = point lies on a straight line
    - 1 = end point of a straight line
    - 2 = end point of curve
    - 3 = point lies on curve
    """
