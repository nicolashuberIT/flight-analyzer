# Algorithms and Helpers

[README](/README.md) > Docs > Algorithms and Helpers

Some key aspects of the program's algorithms are described below. Note that the detailed documentation can be found in the docstrings and in comments in the code. Please note that the data and plots below are merely examples and the exact results can be found in the version of the paper dated 03/31/2024.

## Contents

- [Algorithms and Helpers](#algorithms-and-helpers)
  - [Contents](#contents)
  - [Examples](#examples)
  - [FileConvertor](#fileconvertor)
  - [IGC2CSV](#igc2csv)
  - [AngleAnalyzer](#angleanalyzer)
  - [DataAnalyzer](#dataanalyzer)
  - [ThresholdOptimizer](#thresholdoptimizer)
  - [Other](#other)

## Examples

The following visualisations and data examples - if not stated differently - are based on [this](/docs/datasets/empiric-study/1_raw/20240216_SJf_skytraxx-2.1-export_flight-nr-22.igc) tracklog. For visualisation, please refer to the following two plots:

<table>
  <tr>
    <td style="width: 100%; text-align: center;">
      <img src="/docs/images/20240219_flight-analyzer_tracklog-visualisation_nicolas-huber.png" alt="Punktvariation mit relativer Höhe">
      <br>
      <em>Fig. 1: Tracklog visualisation</em>
    </td>
  </tr>
  <tr>
    <td style="width: 100%; text-align: center;">
      <img src="/docs/images/20240219_flight-analyzer_tracklog-visualisation-altitude_nicolas-huber.png" alt="Höhenvariation">
      <br>
      <em>Fig. 2: Altitude variation</em>
    </td>
  </tr>
</table>

## FileConvertor

The `FileConvertor` is a helper class that converts the manually preprocessed data, which is documented [here](/docs/documentation/basic-usage.md#preprocessing-flight-data), to data that can be consumed by the algorithms of this application. Additionally, this class filters the raw data: It removes entries where the `altitudeMode` property is not set to `clampToGround` and it removes entries of horizontal speed 0. The input data is in form of `.csv` or `.xlsx` and in the following structure (artificial data):

```txt
name,description,altitudeMode,visibility,tessellate,WKT
12:25:30 0m 5kmh 0m/s 0km,,clampToGround,,TRUE,"LINESTRING Z (7.530683 46.213083 2612, 7.5307 46.213083 2612)"
...
```

After executing the `FileConvertor` for a manually preprocessed file the data looks like this (artificial data):

```txt
timestamp [UTC],relative altitude [m],horizontal velocity [m/s],vertical velocity [m/s],distance to takeoff [km],longitude,latitude
12:25:30,0.0,1.39,0.0,0.0,7.530683,46.213083
...
```

You can manually execute the `FileConvertor` using [this](/src/executor/execute_file_convertor.ipynb) executor notebook. The source code of this class can be seen [here](/src/helpers/file_convertor.py).

## IGC2CSV

The `IGC2CSV` package can be found [here](https://github.com/nicolashuberIT/IGC2CSV). It's an application that reads `.igc` files and converts the data to a format that's compatible with the `flight-analyzer` tools.

You can manually execute the `IGC2CSV` package to convert a large amount of tracklogs to `.csv` data, e.g. to conduct individual analyses as documented below. Use [this](/src/executor/execute_IGC2CSV.ipynb) executor for this purpose.

## AngleAnalyzer

The `AngleAnalyzer` class is designed to analyze flight trajectories at a specific point by examining the angles between successive points. It reads flight data from a CSV file and calculates angles between points, determining if they form a straight line or a curve. Using provided thresholds, it extracts past and future coordinates, filters out zero angles, and performs both angle-based and linear regression analyses. These analyses help classify flight segments as either straight lines or curves. 

The input for the following examples was [this](/docs/datasets/empiric-study/2_csv/20240216_SJf_skytraxx-2.1-export_flight-nr-22.csv) file. The examples used the conditions in the box below:

<details>
<summary>Conditions</summary>

```Python
INDEX: int = 400 # point to be analyzed

ANGLE_PAST_THRESHOLD: int = (
    80  # number of points in the past that are considered for the angle evaluation
)
ANGLE_FUTURE_THRESHOLD: int = (
    35  # number of points in the future that are considered for the angle evaluation
)
ANGLE_THRESHOLD: int = 20  # angle < 20° is considered as straight line
LINEAR_REGRESSION_THRESHOLD: float = 0.9  # r-value > 0.9 is considered as straight line
```
</details>

This results in the following graphs, which represent the state at a point of index 1400 (example), which can be seen in the `Conditions` box.

<table>
  <tr>
    <td style="width: 50%; text-align: center;">
      <img src="/docs/images/20240219_flight-analyzer_punktvariation-mit-relativer-hoehe_nicolas-huber.png" alt="Punktvariation mit relativer Höhe">
      <br>
      <em>Fig. 3: Point variation with relative height</em>
    </td>
    <td style="width: 50%; text-align: center;">
      <img src="/docs/images/20240219_flight-analyzer_winkelvariation_nicolas-huber.png" alt="Winkelvariation">
      <br>
      <em>Fig. 4: Angle variation</em>
    </td>
  </tr>
  <tr>
    <td style="width: 50%; text-align: center;">
      <img src="/docs/images/20240219_flight-analyzer_punktvariation-mit-linearer-regression-vergangenheit_nicolas-huber.png" alt="Lineare Regression (Vergangenheit)">
      <br>
      <em>Fig. 5: Linear regression (past)</em>
    </td>
    <td style="width: 50%; text-align: center;">
      <img src="/docs/images/20240219_flight-analyzer_punktvariation-mit-linearer-regression-zukunft_nicolas-huber.png" alt="Lineare Regression (Zukunft)">
      <br>
      <em>Fig. 6: Linear regression (future)</em>
    </td>
  </tr>
</table>

As you can easily tell by eye the analysed point lies on a straight line. This can be seen in figure 3. Figure 4 is a visualization of the angle variaton of the analysed points, the blue line representing the analysed point. The data behind this plot is calculated by comparing the angle between the datapoint and other trackpoints of the series within the thresholds. More precisely, the slope of the straight line between the analyzed point and the current point is compared with the slope of the first line between the analyzed point and the subsequent point. Additionally, as shown in figures 5 and 6, the program also runs a linear regression analysis that is validated against the angle analysis for both the past and future values. These analyses result in a categorization of that specific datapoint, which in this case is:

<details>
<summary>Output</summary>

```txt
Angle Analysis
--> Past: True
--> Future: True

Past Linear Regression
--> Status: True
--> Slope: 2.2164114894852203
--> Intercept: 26.555641367054566
--> R-Value: 0.9993518080941215
--> P-Value: 2.2176627059165095e-114
--> Standard Error: 0.0090402637366967

Future Linear Regression
--> Status: True
--> Slope: 1.7785241117339787
--> Intercept: 30.631046248204335
--> R-Value: 0.9987142854912539
--> P-Value: 2.5304168482864756e-44
--> Standard Error: 0.015714810778103883

Data Analysis
--> Status: (True, 'Straight Line', 0)
```
</details>

You can manually execute the `AngleAnalyzer` using [this](/src/executor/execute_angle_analyzer.ipynb) executor. The source code of this algorithm can be found [here](/src/algorithms/angle_analyzer.py).

## DataAnalyzer

The `DataAnalyzer` class conducts thorough analysis of flight trajectory data by systematically applying the `AngleAnalyzer` class to every single trackpoint. This process enables the determination of whether each point lies on a straight line or a curve. It reads flight data from a CSV file, processes it by extracting past and future coordinates for each point, and performs angle-based and linear regression analyses. The analysis results, including the classification of each point as belonging to a straight-line segment or a curved segment, are appended to the dataset. Finally, the processed data, enriched with analysis outcomes, is exported to a new CSV file. This systematic approach empowers the identification of different trajectory characteristics throughout the flight path.

The input for the following examples was [this](/docs/datasets/empiric-study/2_csv/20240216_SJf_skytraxx-2.1-export_flight-nr-22.csv) file. The examples used the conditions in the box below:

<details>
<summary>Conditions</summary>

```Python
ANGLE_PAST_THRESHOLD: int = (
    80  # number of points in the past that are considered for the angle evaluation
)
ANGLE_FUTURE_THRESHOLD: int = (
    35  # number of points in the future that are considered for the angle evaluation
)
ANGLE_THRESHOLD: int = 20  # angle < 20° is considered as straight line
LINEAR_REGRESSION_THRESHOLD: float = 0.9  # r-value > 0.9 is considered as straight line
```
</details>

This results in the following plot and results:

<table>
  <tr>
    <td style="width: 100%; text-align: center;">
      <img src="/docs/images/20240219_flight-analyzer_punktvariation-mit-position-und-kategorisierung_nicolas-huber.png" alt="Kategorisierung der Punkte">
      <br>
      <em>Fig. 7: Point position and categorization</em>
    </td>
  </tr>
</table>

As you can see, the algorithm accurately flagged points on a straight line / points on a curve. For further analyses, such as the simulation of the stationary glide of a paraglider, only points on a straight line can be used, which is why this analysis needs to be as accurate as possible. To optimize the results of this analysis please refer to the [Optimizer](#thresholdoptimizer) section. The analysis in this example leads to this result:

<details>
<summary>Output</summary>

```txt
You lost 115 rows of data due to processing. The data loss is supposed to be 115 rows, which can be calculated by adding the ANGLE_FUTURE_THRESHOLD and the ANGLE_PAST_TRESHOLD.

The average accuracy of the AngleAnalyzer algorithm and the past / future tresholds of 80 / 35 for points on a straight line can be defined as follows:
--> average r_value: 0.87
--> average p_value: 0.0
--> average std_err: 0.01

A linear regression can be considered as a good fit if the r_value is close to 1, the p_value is close to 0 and the std_err is close to 0.

The system found 2487 points on straight lines, whereas the amount of points on a curve is 6114. The expected amount of points on a curve is 6114, which can be calculated by subtracting the count of points on a straight line from the total point count.

In total, you lost 71.08% of the data after applying the AngleAnalyzer algorithm as you can only use the points on a straight line for further processing.
```

</details>

You can manually execute the `DataAnalyzer` using [this](/src/executor/execute_data_analyzer.ipynb) executor. The source code of this algorithm can be found [here](/src/helpers/data_analyzer.py).

## ThresholdOptimizer

The `ThresholdOptimizer` class optimizes thresholds for the `AngleAnalyzer` algorithm by systematically testing different combinations and scoring them based on specified criteria. It iteratively evaluates threshold combinations using a `DataAnalyzer` object, calculating scores derived from linear regression values and weighted metrics. The class then selects the best-scoring threshold combinations and exports the tested combinations to a CSV file. By providing insights into the trade-offs between different threshold settings, this class enables the fine-tuning of the `AngleAnalyzer` to achieve optimal performance.

The following data and plots are artificial and are intended to visualize this process.

<details>
<summary>Conditions</summary>

```Python
R_VALUE_WEIGHT: float = 0.6  # weight of the r-value in the optimization
P_VALUE_WEIGHT: float = 0.3  # weight of the p-value in the optimization
STD_ERROR_WEIGHT: float = 0.1  # weight of the standard error in the optimization

OPTIMIZATION_LIMIT: int = 30  # upper limit of optimization loops
OPTIMIZATION_STEPS: int = 5  # step size per optimization loop
OPTIMIZATION_RUNTIME_ESTIMATION: int = 120  # estimated runtime per loop in seconds
```

</details>

This results in the following plots and results:

<table>
<tr>
    <td style="width: 50%; text-align: center;">
      <img src="/docs/images/20240215_flight-analyzer_score-und-datenverlust_nicolas-huber.png" alt="Score und Datenverlust">
      <br>
      <em>Fig. 8: Optimization score and data loss</em>
    </td>
  </tr>
  <tr>
    <td style="width: 50%; text-align: center;">
      <img src="/docs/images/20240215_flight-analyzer_score-und-datenverlust_nicolas-huber.png" alt="Score und Datenverlust">
      <br>
      <em>Fig. 9: Optimization score and data loss</em>
    </td>
    <td style="width: 50%; text-align: center;">
      <img src="/docs/images/20240215_flight-analyzer_optimierung-der-thresholds_nicolas-huber.png" alt="Optimierung der Thresholds">
      <br>
      <em>Fig. 10: Threshold optimization</em>
    </td>
  </tr>
</table>

Figure 8 plots both the optimization score and the data loss for this threshold combination on a normalized scale. Figure 9 shows how the 10 relevant linear regression values are weighted for the analysis. This specific run led to the following results:

<details>
<summary>Output</summary>

```txt
Individual thresholds with the best score:
--> past_threshold_optimized: 25
--> future_threshold_optimized: 25

Below is a tabular overview of the 5 best scores and their thresholds. This information is more meaningful here, as in the analysis later for the evaluation of a point, both the future and the past are taken into account, and thus the score considers the interaction of the two thresholds.

<<< HEADER >>>
0	25	25	0.772521	9.392513e-12	0.012124	0.462300	62.820217
1	25	20	0.753950	2.555986e-10	0.015246	0.450846	61.180948
2	25	15	0.745859	1.490066e-08	0.018904	0.445625	59.843246
3	20	25	0.740292	3.472833e-10	0.014465	0.442729	60.581248
4	25	10	0.724441	2.517912e-06	0.021627	0.432501	58.299735

The best performing thresholds are 25 (angle_past_threshold) and 25 (angle_future_threshold) with a score of 0.4623003930101672.

Another good performing set of thresholds can be found by comparing the data loss relative to the scores, which are directly related to the thresholds. In this case, the best performing thresholds are 25 (angle_past_threshold) and 15 (angle_future_threshold) with a score of 0.44562524837811207 and a data loss of 59.84324573536192. The bigger the difference between the score and the data loss, the better the thresholds are. This is the case because the precison of the thresholds is overall better if less data is lost, even if there is a small decrease in the score.
```
</details>

The `ThresholdOptimizer` needs to be executed before running any other algorithms in this application to achieve the best possible performance. Just run the optimization for the limit and step size as well as linear regression weights you like and enter the resulting angle thresholds to the `constants.py` file.

The `ThresholdOptimizer` can be executed using [this](/src/executor/execute_optimize_thresholds.ipynb) notebook. The source code of this class can be seen [here](/src/helpers/optimize_thresholds.py). 

## Other

There are more algorithms and helpers that are not documented here. You can check out the [docs/research/](/docs/research/) folder for reports or check out the source code [here](/src).

--- 

_© 2024, [Nicolas Huber](https://nicolas-huber.ch). All rights reserved._