# Research Report

[README](/README.md) > Docs > Research Report

This report describes how the analyses presented in the scientific paper **Fliegen am Limit - Aktive Sicherheit im Gleitschirmsport** came about. This includes the preprocessing as well as the optimization of the algorithms and finally the evaluation of the data. Detailed documentation of the algorithms used and the concepts and objectives behind them can be found in the [technical documentation](/README.md#algorithms-and-helpers) and in the paper dated 03/31/2024.

Happy reading!

## Contents

- [Research Report](#research-report)
  - [Contents](#contents)
  - [Empirical Dataset](#empirical-dataset)
  - [Testing](#testing)
  - [Algorithm Optimization](#algorithm-optimization)
    - [Overview](#overview)
    - [Optimization Runs](#optimization-runs)
      - [Run 1 - Limit 100 \& Step 5](#run-1---limit-100--step-5)
      - [Run 2 - Limit 150 \& Step 5](#run-2---limit-150--step-5)
      - [Run 3 - Limit 200 \& Step 5](#run-3---limit-200--step-5)
    - [Optimization Summary](#optimization-summary)
  - [Flight Data Analysis](#flight-data-analysis)
    - [Conditions](#conditions)
    - [Track Log Matrix](#track-log-matrix)
    - [Speed Data Analysis](#speed-data-analysis)
      - [Speed Data Processing](#speed-data-processing)
      - [Speed Data Visualisation](#speed-data-visualisation)
      - [Speed Data Analysis Report](#speed-data-analysis-report)
      - [Speed Data Analysis Conclusion](#speed-data-analysis-conclusion)
    - [C Value Modeling](#c-value-modeling)
      - [C Model Data Processing](#c-model-data-processing)
      - [C Model Data Visualisation](#c-model-data-visualisation)
      - [C Model Report](#c-model-report)
    - [Stagnation Pressure Modeling](#stagnation-pressure-modeling)
    - [Quality Analysis](#quality-analysis)
  - [Summary](#summary)

## Empirical Dataset

The empirical data set on which the analyses are based was collected by a variometer (Skytraxx 2.1) of [this](https://www.skytraxx.eu/en/skytraxx-2-1) type. The data set consists of 30 track logs of flights, which were manually selected and checked for clean data. The data set contains pure gliding flights and preferably no disturbances such as thermals or strong wind flights.

Please find the raw input files in `.igc` format listed [here](/docs/datasets/empiric-study/1_raw/). Alternatively, you can check out the input in `.csv` format [here](/docs/datasets/empiric-study/2_csv/).

## Testing

To ensure that the `flight-analyzer` application does not generate incorrect data and analyses, the code was tested extensively. Unit tests can be found [here](/tests/), the CI/CD pipeline configuration can be viewed [here](https://github.com/nicolashuberIT/flight-analyzer/blob/main/.github/workflows/testing.yaml) and the testing status is as follows:

![Testing](https://github.com/nicolashuberIT/flight-analyzer/actions/workflows/testing.yaml/badge.svg)

## Algorithm Optimization

The analysis of the flight data is based on some constant values that must be set in the `constants.py` file before the data evaluation. The `AngleAnalyzer` algorithm in particular requires careful calibration. The `ThresholdOptimizer` algorithm, which can be viewed [here](/src/helpers/optimize_thresholds.py), is used for this purpose.

### Overview

There are two parameters for optimizing the `AngleAnalyzer` algorithm: 

- `OPTIMIZATION_LIMIT` - defines the highest threshold that's to be tested, starts from threshold 10
- `OPTIMIZATION_STEPS` - defines the step size between the tested thresholds

When the optimization is performed for these parameters, the algorithm forms a cartesian product of all combinations for `ANGLE_PAST_THRESHOLD` and `ANGLE_FUTURE_THRESHOLD` within the specified range and calculates how well these combinations perform in the analysis of the flight data.

The basis for this optimization is the track log visualized below. The raw file can be found [here](/docs/datasets/empiric-study/1_raw/20240216_SJf_skytraxx-2.1-export_flight-nr-22.igc), the corresponding `.csv` file can be found [here](/docs/datasets/empiric-study/2_csv/20240216_SJf_skytraxx-2.1-export_flight-nr-22.csv).

<table>
<tr>
  <th>Analyzed track log (optimization)</th>
</tr>
<tr>
  <td>
    <img src="/docs/optimization/input/20240220_SJf_threshold-optimization_flight-visualisation_nicolas-huber.png" alt="Tracklog">
      <br>
      <em>Fig. 1: Track log visualisation (optimization)</em>
    </td>
</tr>
</table>

### Optimization Runs

Because the optimization parameters have a large effect on the resolution of the data (the larger the cartesian product, the more high-performance combinations are potentially lost in the set), three different calculation runs were performed, each under the following conditions:

- Run 1: `OPTIMIZATION_LIMIT` = 100, `OPTIMIZATION_STEP` = 5
- Run 2: `OPTIMIZATION_LIMIT` = 150, `OPTIMIZATION_STEP` = 5
- Run 3: `OPTIMIZATION_LIMIT` = 200, `OPTIMIZATION_STEP` = 5

The findings of each run can be found below.

#### Run 1 - Limit 100 & Step 5

Run one was executed for the following conditions:

- `OPTIMIZATION_LIMIT` = 100
- `OPTIMIZATION_STEP` = 5

The test ended with the following result (see figures 2 and 3 and the report below).

<table>
<tr>
    <th>Thresholds</th>
    <th>Linear regression</th>
</tr>
<tr>
    <td>
        <img src="/docs/optimization/limit-100-step-5/20240220_SJf_threshold-optimization_limit-100-step-5_best-thresholds_nicolas-huber.png" alt="Tracklog">
        <br>
        <em>Fig. 2: Best thresholds (run 1)</em>
    </td>
    <td>
        <img src="/docs/optimization/limit-100-step-5/20240220_SJf_threshold-optimization_limit-100-step-5_score-linear-regression-values_nicolas-huber.png" alt="Tracklog">
        <br>
        <em>Fig. 3: Linear regression values (run 1)</em>
    </td>
</tr>
</table>

Check out the report of this optimization run:

<details>
<summary>Show Report</summary>

```txt
Individual thresholds with the best score:
--> past_threshold_optimized: 95
--> future_threshold_optimized: 90

Below is a tabular overview of the 5 best scores and their thresholds. This information is more meaningful here, as in the analysis later for the evaluation of a point, both the future and the past are taken into account, and thus the score considers the interaction of the two thresholds.

<<< LISTING >>>

The best performing thresholds are 95 (angle_past_threshold) and 90 (angle_future_threshold) with a score of 0.5949858988489289.

Another good performing set of thresholds can be found by comparing the data loss relative to the scores, which are directly related to the thresholds. In this case, the best performing thresholds are 10 (angle_past_threshold) and 50 (angle_future_threshold) with a score of 0.5696515553401256 and a data loss of 43.728813559322035. The bigger the difference between the score and the data loss, the better the thresholds are. This is the case because the precison of the thresholds is overall better if less data is lost, even if there is a small decrease in the score.
```

</details>

In summary, the optimization run for limit 100 and step size 5 resolved in the following result:

- Best performing thresholds by score: 
  - `ANGLE_PAST_THRESHOLD` = 95
  - `ANGLE_FUTURE_THRESHOLD` = 90
- Best performing thesholds by score-data-loss-ratio: 
  - `ANGLE_PAST_THRESHOLD` = 10
  - `ANGLE_FUTURE_THRESHOLD` = 50

For reference, the optimized thresholds result in the following track log analyses:

<table>
<tr>
  <th>Track log visualisation by score</th>
  <th>Track log visualisation by ratio</th>
</tr>
<tr>
    <td>
        <img src="/docs/optimization/limit-100-step-5/20240220_SJf_threshold-optimization_limit-100-step-5_tracklog-analysis_95-90_nicolas-huber.png" alt="Optimization by score">
        <br>
        <em>Fig. 4: Track log visualisation by score (95 & 90, run 1)</em>
    </td>
    <td>
        <img src="/docs/optimization/limit-100-step-5/20240220_SJf_threshold-optimization_limit-100-step-5_tracklog-analysis_10-50_nicolas-huber.png" alt="Optimization by ratio">
        <br>
        <em>Fig. 5: Track log visualisation by ratio (10 & 50, run 1)</em>
    </td>
</tr>
</table>

A detailed report on this optimization run including imformation about runtime etc. in `.html` format can be found [here](/docs/optimization/limit-100-step-5/20240220_SJf_threshold-optimization_limit-100-step-5_report_nicolas-huber.html).

#### Run 2 - Limit 150 & Step 5

Run two was executed for the following conditions:

- `OPTIMIZATION_LIMIT` = 150
- `OPTIMIZATION_STEP` = 5

The test ended with the following result (see figures 6 and 7 and the report below).

<table>
<tr>
    <th>Thresholds</th>
    <th>Linear regression</th>
</tr>
<tr>
    <td>
        <img src="/docs/optimization/limit-150-step-5/20240220_SJf_threshold-optimization_limit-150-step-5_best-thresholds_nicolas-huber.png" alt="Tracklog">
        <br>
        <em>Fig. 6: Best thresholds (run 2)</em>
    </td>
    <td>
        <img src="/docs/optimization/limit-150-step-5/20240220_SJf_threshold-optimization_limit-150-step-5_score-linear-regression-values_nicolas-huber.png" alt="Tracklog">
        <br>
        <em>Fig. 7: Linear regression values (run 2)</em>
    </td>
</tr>
</table>

Check out the report of this optimization run:

<details>
<summary>Show Report</summary>

```txt
Individual thresholds with the best score:
--> past_threshold_optimized: 95
--> future_threshold_optimized: 90

Below is a tabular overview of the 5 best scores and their thresholds. This information is more meaningful here, as in the analysis later for the evaluation of a point, both the future and the past are taken into account, and thus the score considers the interaction of the two thresholds.

<<< LISTING >>>

The best performing thresholds are 95 (angle_past_threshold) and 90 (angle_future_threshold) with a score of 0.5949858988489289.

Another good performing set of thresholds can be found by comparing the data loss relative to the scores, which are directly related to the thresholds. In this case, the best performing thresholds are 10 (angle_past_threshold) and 50 (angle_future_threshold) with a score of 0.5696515553401256 and a data loss of 43.728813559322035. The bigger the difference between the score and the data loss, the better the thresholds are. This is the case because the precison of the thresholds is overall better if less data is lost, even if there is a small decrease in the score.

```

</details>

In summary, the optimization run for limit 100 and step size 5 resolved in the following result:

- Best performing thresholds by score: 
  - `ANGLE_PAST_THRESHOLD` = 95
  - `ANGLE_FUTURE_THRESHOLD` = 90
- Best performing thesholds by score-data-loss-ratio: 
  - `ANGLE_PAST_THRESHOLD` = 10
  - `ANGLE_FUTURE_THRESHOLD` = 50

For reference, the optimized thresholds result in the following track log analyses:

<table>
<tr>
  <th>Track log visualisation by score</th>
  <th>Track log visualisation by ratio</th>
</tr>
<tr>
    <td>
        <img src="/docs/optimization/limit-150-step-5/20240220_SJf_threshold-optimization_limit-150-step-5_tracklog-analysis_95-90_nicolas-huber.png" alt="Optimization by score">
        <br>
        <em>Fig. 8: Track log visualisation by score (95 & 90, run 2)</em>
    </td>
    <td>
        <img src="/docs/optimization/limit-150-step-5/20240220_SJf_threshold-optimization_limit-150-step-5_tracklog-analysis_10-50_nicolas-huber.png" alt="Optimization by ratio">
        <br>
        <em>Fig. 9: Track log visualisation by ratio (10 & 50, run 2)</em>
    </td>
</tr>
</table>

A detailed report on this optimization run including imformation about runtime etc. in `.html` format can be found [here](/docs/optimization/limit-150-step-5/20240220_SJf_threshold-optimization_limit-150-step-5_report_nicolas-huber.html).

#### Run 3 - Limit 200 & Step 5

This optimization run isn't further documented as it resolved in exactly the same result as runs 1 and 2.

### Optimization Summary

Three calculation runs were carried out with different parameters to optimize the thresholds. All runs produced the same result. The optimization algorithm recommends the following thresholds for further analyses:

- By score:
  - `ANGLE_PAST_THRESHOLD` = 95
  - `ANGLE_FUTURE_THRESHOLD` = 90
- By ratio:
  - `ANGLE_PAST_THRESHOLD` = 10
  - `ANGLE_FUTURE_THRESHOLD` = 50

Now the question arises as to which of the combinations works better in practice. Some tests based on the `SpeedAnalyzer` algorithm have shown that the Thresholds by score are the better combination. The combination 95 & 90 produces the best results. This high-performance threshold pair is therefore the basis for all further analyses.

## Flight Data Analysis

### Conditions

The analyses presented in the paper **Fliegen am Limit - Aktive Sicherheit im Gleitschirmsport**, dated 03/31/2024, have been conducted for the following conditions, which can be found in the [constants.py](/src/constants.py) file.

<details>
<summary>Show Conditions</summary>

```Python
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

# simulation

ALTITUDE: float = 2000  # altitude of the paraglider in flight [m]
MASS: float = 90  # mass of the paraglider in flight [kg]
GRAVITY: float = 9.81  # gravitational accelaration in Zurich, Switzerland [m/s^2]
AIR_DENSITY: float = 1.0065  # air density at altitude 2000m [kg/m^3]
WING_AREA: float = 23.1  # wing area of the paraglider [m^2]
STATIC_PRESSURE: float = 79495.22  # static air pressure at altitude [N/m^2], ICAO standard atmosphere, 15°C at altitude 2000m

# simulation quality

MASS_TRESHOLD: int = 8  # mass threshold for the quality analysis to account for variations in the pilot's weight
```

</details>

Additionally, the following two reference datasets are imported:

- theoretical reference: [This](/docs/datasets/reference/theoretical_reference.csv) contains theoretical speed data for the Ozone Alpina 4 in size MS, provided by Ozone Gliders LTD.
- original reference: [This](/docs/datasets/reference/original_reference.csv) contains experimental speed data that has been used for the analyses presented in the original paper **Fliegen am Limit - Aktive Sicherheit im Gleitschirmsport**, dated 10/24/2022. The data is normalized by horizontal speed to match the analyses of the revised paper, dated 03/31/2024.

### Track Log Matrix

The following analyses are based on the flight data mentioned [here](#empiric-dataset). Below is a visualization of all these flights.

<table>
<tr>
  <th>Track log visualisation</th>
  <th>Altitude variation</th>
</tr>
<tr>
    <td>
        <img src="/docs/research/images/tracks/map/20240222_SJf_track-log-visualisation_map-1_nicolas-huber.png" alt="Track log visualisation">
        <br>
        <em>Fig. 10: Track log visualisation (flight 1)</em>
    </td>
    <td>
        <img src="/docs/research/images/tracks/altitude/20240222_SJf_track-log-visualisation_altitude-1_nicolas-huber.png" alt="Altitude variation">
        <br>
        <em>Fig. 11: Altitude variation (flight 1)</em>
    </td>
</tr>
<tr>
    <td>
        <img src="/docs/research/images/tracks/map/20240222_SJf_track-log-visualisation_map-2_nicolas-huber.png" alt="Track log visualisation">
        <br>
        <em>Fig. 12: Track log visualisation (flight 5)</em>
    </td>
    <td>
        <img src="/docs/research/images/tracks/altitude/20240222_SJf_track-log-visualisation_altitude-2_nicolas-huber.png" alt="Altitude variation">
        <br>
        <em>Fig. 13: Altitude variation (flight 5)</em>
    </td>
</tr>
<tr>
    <td>
        <img src="/docs/research/images/tracks/map/20240222_SJf_track-log-visualisation_map-3_nicolas-huber.png" alt="Track log visualisation">
        <br>
        <em>Fig. 14: Track log visualisation (flight 10)</em>
    </td>
    <td>
        <img src="/docs/research/images/tracks/altitude/20240222_SJf_track-log-visualisation_altitude-3_nicolas-huber.png" alt="Altitude variation">
        <br>
        <em>Fig. 15: Altitude variation (flight 10)</em>
    </td>
</tr>
<tr>
    <td>
        <img src="/docs/research/images/tracks/map/20240222_SJf_track-log-visualisation_map-4_nicolas-huber.png" alt="Track log visualisation">
        <br>
        <em>Fig. 16: Track log visualisation (flight 12)</em>
    </td>
    <td>
        <img src="/docs/research/images/tracks/altitude/20240222_SJf_track-log-visualisation_altitude-4_nicolas-huber.png" alt="Altitude variation">
        <br>
        <em>Fig. 17: Altitude variation (flight 12)</em>
    </td>
</tr>
<tr>
    <td>
        <img src="/docs/research/images/tracks/map/20240222_SJf_track-log-visualisation_map-5_nicolas-huber.png" alt="Track log visualisation">
        <br>
        <em>Fig. 18: Track log visualisation (flight 15)</em>
    </td>
    <td>
        <img src="/docs/research/images/tracks/altitude/20240222_SJf_track-log-visualisation_altitude-5_nicolas-huber.png" alt="Altitude variation">
        <br>
        <em>Fig. 19: Altitude variation (flight 15)</em>
    </td>
</tr>
<tr>
    <td>
        <img src="/docs/research/images/tracks/map/20240222_SJf_track-log-visualisation_map-6_nicolas-huber.png" alt="Track log visualisation">
        <br>
        <em>Fig. 20: Track log visualisation (flight 16)</em>
    </td>
    <td>
        <img src="/docs/research/images/tracks/altitude/20240222_SJf_track-log-visualisation_altitude-6_nicolas-huber.png" alt="Altitude variation">
        <br>
        <em>Fig. 21: Altitude variation (flight 16)</em>
    </td>
</tr>
<tr>
    <td>
        <img src="/docs/research/images/tracks/map/20240222_SJf_track-log-visualisation_map-7_nicolas-huber.png" alt="Track log visualisation">
        <br>
        <em>Fig. 22: Track log visualisation (flight 17)</em>
    </td>
    <td>
        <img src="/docs/research/images/tracks/altitude/20240222_SJf_track-log-visualisation_altitude-7_nicolas-huber.png" alt="Altitude variation">
        <br>
        <em>Fig. 23: Altitude variation (flight 17)</em>
    </td>
</tr>
<tr>
    <td>
        <img src="/docs/research/images/tracks/map/20240222_SJf_track-log-visualisation_map-8_nicolas-huber.png" alt="Track log visualisation">
        <br>
        <em>Fig. 24: Track log visualisation (flight 18)</em>
    </td>
    <td>
        <img src="/docs/research/images/tracks/altitude/20240222_SJf_track-log-visualisation_altitude-8_nicolas-huber.png" alt="Altitude variation">
        <br>
        <em>Fig. 25: Altitude variation (flight 18)</em>
    </td>
</tr>
<tr>
    <td>
        <img src="/docs/research/images/tracks/map/20240222_SJf_track-log-visualisation_map-9_nicolas-huber.png" alt="Track log visualisation">
        <br>
        <em>Fig. 26: Track log visualisation (flight 20)</em>
    </td>
    <td>
        <img src="/docs/research/images/tracks/altitude/20240222_SJf_track-log-visualisation_altitude-9_nicolas-huber.png" alt="Altitude variation">
        <br>
        <em>Fig. 27: Altitude variation (flight 20)</em>
    </td>
</tr>
<tr>
    <td>
        <img src="/docs/research/images/tracks/map/20240222_SJf_track-log-visualisation_map-10_nicolas-huber.png" alt="Track log visualisation">
        <br>
        <em>Fig. 28: Track log visualisation (flight 21)</em>
    </td>
    <td>
        <img src="/docs/research/images/tracks/altitude/20240222_SJf_track-log-visualisation_altitude-10_nicolas-huber.png" alt="Altitude variation">
        <br>
        <em>Fig. 29: Altitude variation (flight 21)</em>
    </td>
</tr>
<tr>
    <td>
        <img src="/docs/research/images/tracks/map/20240222_SJf_track-log-visualisation_map-11_nicolas-huber.png" alt="Track log visualisation">
        <br>
        <em>Fig. 30: Track log visualisation (flight 22)</em>
    </td>
    <td>
        <img src="/docs/research/images/tracks/altitude/20240222_SJf_track-log-visualisation_altitude-11_nicolas-huber.png" alt="Altitude variation">
        <br>
        <em>Fig. 31: Altitude variation (flight 22)</em>
    </td>
</tr>
<tr>
    <td>
        <img src="/docs/research/images/tracks/map/20240222_SJf_track-log-visualisation_map-12_nicolas-huber.png" alt="Track log visualisation">
        <br>
        <em>Fig. 32: Track log visualisation (flight 23)</em>
    </td>
    <td>
        <img src="/docs/research/images/tracks/altitude/20240222_SJf_track-log-visualisation_altitude-12_nicolas-huber.png" alt="Altitude variation">
        <br>
        <em>Fig. 33: Altitude variation (flight 23)</em>
    </td>
</tr>
<tr>
    <td>
        <img src="/docs/research/images/tracks/map/20240222_SJf_track-log-visualisation_map-13_nicolas-huber.png" alt="Track log visualisation">
        <br>
        <em>Fig. 34: Track log visualisation (flight 24)</em>
    </td>
    <td>
        <img src="/docs/research/images/tracks/altitude/20240222_SJf_track-log-visualisation_altitude-13_nicolas-huber.png" alt="Altitude variation">
        <br>
        <em>Fig. 35: Altitude variation (flight 24)</em>
    </td>
</tr>
<tr>
    <td>
        <img src="/docs/research/images/tracks/map/20240222_SJf_track-log-visualisation_map-14_nicolas-huber.png" alt="Track log visualisation">
        <br>
        <em>Fig. 36: Track log visualisation (flight 31)</em>
    </td>
    <td>
        <img src="/docs/research/images/tracks/altitude/20240222_SJf_track-log-visualisation_altitude-14_nicolas-huber.png" alt="Altitude variation">
        <br>
        <em>Fig. 37: Altitude variation (flight 31)</em>
    </td>
</tr>
<tr>
    <td>
        <img src="/docs/research/images/tracks/map/20240222_SJf_track-log-visualisation_map-15_nicolas-huber.png" alt="Track log visualisation">
        <br>
        <em>Fig. 38: Track log visualisation (flight 33)</em>
    </td>
    <td>
        <img src="/docs/research/images/tracks/altitude/20240222_SJf_track-log-visualisation_altitude-15_nicolas-huber.png" alt="Altitude variation">
        <br>
        <em>Fig. 39: Altitude variation (flight 33)</em>
    </td>
</tr>
<tr>
    <td>
        <img src="/docs/research/images/tracks/map/20240222_SJf_track-log-visualisation_map-16_nicolas-huber.png" alt="Track log visualisation">
        <br>
        <em>Fig. 40: Track log visualisation (flight 35)</em>
    </td>
    <td>
        <img src="/docs/research/images/tracks/altitude/20240222_SJf_track-log-visualisation_altitude-16_nicolas-huber.png" alt="Altitude variation">
        <br>
        <em>Fig. 41: Altitude variation (flight 35)</em>
    </td>
</tr>
<tr>
    <td>
        <img src="/docs/research/images/tracks/map/20240222_SJf_track-log-visualisation_map-17_nicolas-huber.png" alt="Track log visualisation">
        <br>
        <em>Fig. 42: Track log visualisation (flight 36)</em>
    </td>
    <td>
        <img src="/docs/research/images/tracks/altitude/20240222_SJf_track-log-visualisation_altitude-17_nicolas-huber.png" alt="Altitude variation">
        <br>
        <em>Fig. 43: Altitude variation (flight 36)</em>
    </td>
</tr>
<tr>
    <td>
        <img src="/docs/research/images/tracks/map/20240222_SJf_track-log-visualisation_map-18_nicolas-huber.png" alt="Track log visualisation">
        <br>
        <em>Fig. 44: Track log visualisation (flight 37)</em>
    </td>
    <td>
        <img src="/docs/research/images/tracks/altitude/20240222_SJf_track-log-visualisation_altitude-18_nicolas-huber.png" alt="Altitude variation">
        <br>
        <em>Fig. 45: Altitude variation (flight 37)</em>
    </td>
</tr>
<tr>
    <td>
        <img src="/docs/research/images/tracks/map/20240222_SJf_track-log-visualisation_map-19_nicolas-huber.png" alt="Track log visualisation">
        <br>
        <em>Fig. 46: Track log visualisation (flight 40)</em>
    </td>
    <td>
        <img src="/docs/research/images/tracks/altitude/20240222_SJf_track-log-visualisation_altitude-19_nicolas-huber.png" alt="Altitude variation">
        <br>
        <em>Fig. 47: Altitude variation (flight 40)</em>
    </td>
</tr>
<tr>
    <td>
        <img src="/docs/research/images/tracks/map/20240222_SJf_track-log-visualisation_map-20_nicolas-huber.png" alt="Track log visualisation">
        <br>
        <em>Fig. 48: Track log visualisation (flight 44)</em>
    </td>
    <td>
        <img src="/docs/research/images/tracks/altitude/20240222_SJf_track-log-visualisation_altitude-20_nicolas-huber.png" alt="Altitude variation">
        <br>
        <em>Fig. 49: Altitude variation (flight 44)</em>
    </td>
</tr>
<tr>
    <td>
        <img src="/docs/research/images/tracks/map/20240222_SJf_track-log-visualisation_map-21_nicolas-huber.png" alt="Track log visualisation">
        <br>
        <em>Fig. 50: Track log visualisation (flight 45)</em>
    </td>
    <td>
        <img src="/docs/research/images/tracks/altitude/20240222_SJf_track-log-visualisation_altitude-21_nicolas-huber.png" alt="Altitude variation">
        <br>
        <em>Fig. 51: Altitude variation (flight 45)</em>
    </td>
</tr>
<tr>
    <td>
        <img src="/docs/research/images/tracks/map/20240222_SJf_track-log-visualisation_map-22_nicolas-huber.png" alt="Track log visualisation">
        <br>
        <em>Fig. 52: Track log visualisation (flight 46)</em>
    </td>
    <td>
        <img src="/docs/research/images/tracks/altitude/20240222_SJf_track-log-visualisation_altitude-22_nicolas-huber.png" alt="Altitude variation">
        <br>
        <em>Fig. 53: Altitude variation (flight 46)</em>
    </td>
</tr>
<tr>
    <td>
        <img src="/docs/research/images/tracks/map/20240222_SJf_track-log-visualisation_map-23_nicolas-huber.png" alt="Track log visualisation">
        <br>
        <em>Fig. 54: Track log visualisation (flight 50)</em>
    </td>
    <td>
        <img src="/docs/research/images/tracks/altitude/20240222_SJf_track-log-visualisation_altitude-23_nicolas-huber.png" alt="Altitude variation">
        <br>
        <em>Fig. 55: Altitude variation (flight 50)</em>
    </td>
</tr>
<tr>
    <td>
        <img src="/docs/research/images/tracks/map/20240222_SJf_track-log-visualisation_map-24_nicolas-huber.png" alt="Track log visualisation">
        <br>
        <em>Fig. 56: Track log visualisation (flight 53)</em>
    </td>
    <td>
        <img src="/docs/research/images/tracks/altitude/20240222_SJf_track-log-visualisation_altitude-24_nicolas-huber.png" alt="Altitude variation">
        <br>
        <em>Fig. 57: Altitude variation (flight 53)</em>
    </td>
</tr>
<tr>
    <td>
        <img src="/docs/research/images/tracks/map/20240222_SJf_track-log-visualisation_map-25_nicolas-huber.png" alt="Track log visualisation">
        <br>
        <em>Fig. 58: Track log visualisation (flight 65)</em>
    </td>
    <td>
        <img src="/docs/research/images/tracks/altitude/20240222_SJf_track-log-visualisation_altitude-25_nicolas-huber.png" alt="Altitude variation">
        <br>
        <em>Fig. 59: Altitude variation (flight 65)</em>
    </td>
</tr>
<tr>
    <td>
        <img src="/docs/research/images/tracks/map/20240222_SJf_track-log-visualisation_map-26_nicolas-huber.png" alt="Track log visualisation">
        <br>
        <em>Fig. 60: Track log visualisation (flight 67)</em>
    </td>
    <td>
        <img src="/docs/research/images/tracks/altitude/20240222_SJf_track-log-visualisation_altitude-26_nicolas-huber.png" alt="Altitude variation">
        <br>
        <em>Fig. 61: Altitude variation (flight 67)</em>
    </td>
</tr>
<tr>
    <td>
        <img src="/docs/research/images/tracks/map/20240222_SJf_track-log-visualisation_map-27_nicolas-huber.png" alt="Track log visualisation">
        <br>
        <em>Fig. 62: Track log visualisation (flight 68)</em>
    </td>
    <td>
        <img src="/docs/research/images/tracks/altitude/20240222_SJf_track-log-visualisation_altitude-27_nicolas-huber.png" alt="Altitude variation">
        <br>
        <em>Fig. 63: Altitude variation (flight 68)</em>
    </td>
</tr>
<tr>
    <td>
        <img src="/docs/research/images/tracks/map/20240222_SJf_track-log-visualisation_map-28_nicolas-huber.png" alt="Track log visualisation">
        <br>
        <em>Fig. 64: Track log visualisation (flight 71)</em>
    </td>
    <td>
        <img src="/docs/research/images/tracks/altitude/20240222_SJf_track-log-visualisation_altitude-28_nicolas-huber.png" alt="Altitude variation">
        <br>
        <em>Fig. 65: Altitude variation (flight 71)</em>
    </td>
</tr>
<tr>
    <td>
        <img src="/docs/research/images/tracks/map/20240222_SJf_track-log-visualisation_map-29_nicolas-huber.png" alt="Track log visualisation">
        <br>
        <em>Fig. 66: Track log visualisation (flight 72)</em>
    </td>
    <td>
        <img src="/docs/research/images/tracks/altitude/20240222_SJf_track-log-visualisation_altitude-29_nicolas-huber.png" alt="Altitude variation">
        <br>
        <em>Fig. 67: Altitude variation (flight 72)</em>
    </td>
</tr>
<tr>
    <td>
        <img src="/docs/research/images/tracks/map/20240222_SJf_track-log-visualisation_map-30_nicolas-huber.png" alt="Track log visualisation">
        <br>
        <em>Fig. 68: Track log visualisation (flight 73)</em>
    </td>
    <td>
        <img src="/docs/research/images/tracks/altitude/20240222_SJf_track-log-visualisation_altitude-30_nicolas-huber.png" alt="Altitude variation">
        <br>
        <em>Fig. 69: Altitude variation (flight 73)</em>
    </td>
</tr>
</table>

If you're looking for a specific track log, go to `docs/datasets/empiric-study/` and then either `1_raw` or `2_csv`. The files are named `20240216_SJf_skytraxx-2.1-export_flight-nr-n`, so just search for the `flight-nr-n` tag you're looking for.

### Speed Data Analysis

A detailed report for the speed data analysis can be found [here](/docs/research/reports/20240224_SJf_data-analysis_nicolas-huber.html). Please find listed below some further documentation on the individual processing steps.

#### Speed Data Processing

The speed data analysis is based on the raw input data, which is read in from the `.igc` files. This data must first be filtered and cleaned so that it can be processed.

The system filters out all horizontal speeds that are not available for comparison in the theoretical reference data set. In addition, data points that lie on a curve or have been flagged as unusable for other reasons are filtered out. The system also ensures that only negative vertical velocities are included in the data set. In this way, disruptive factors such as thermals are excluded as far as possible. 

The automatically generated report of this process can be found below:

<details>
<summary>Show Report</summary>

```txt
Filtered data:
--> Data points for filtered theoretical reference: 6 (lost 0)
--> Data points for filtered original reference: 27 (lost 8)
--> Data points for filtered tracklogs: 2335 (lost 17591)

Please note:
--> Why are so many raw data points lost? This is due to the fact that the system filters out all data point that are not on a straight line. This is done to ensure that the data is as accurate as possible.

Data smoothing:
--> During smoothing, the raw data points were reduced from 2335 to 2335 (lost 0).
--> During grouping, the smoothed data points were reduced from 2335 to 52 (lost 2283).
```

</details>

As described in the report, many data points are lost during pre-processing of the raw data. However, this ensures that the data set is as clean as possible and disruptive factors are removed. In addition, the data is converted into a form that is useful for further modeling. The data is smoothed and grouped according to the horizontal velocity. This is the basis for all further analysis.

#### Speed Data Visualisation

Below is a matrix with the visualized results of this analysis.

<table>
<tr>
  <th>Experimental Speed Data</th>
  <th>Deviation of Speed Data</th>
</tr>
<tr>
    <td>
        <img src="/docs/research/images/speed/20240224_SJf_experimentelle-geschwindigkeitsdaten-original_nicolas-huber.png" alt="Experimental Speed Data">
        <br>
        <em>Fig. 70: Experimental Speed Data, original (10/24/2022)</em>
    </td>
    <td>
        <img src="/docs/research/images/speed/20240224_SJf_abweichung-experimentelle-geschwindigkeitsdaten-original_nicolas-huber.png" alt="Deviation of Speed Data">
        <br>
        <em>Fig 71: Deviation of Speed Data, original (10/24/2022)</em>
    </td>
</tr>
<tr>
    <td>
        <img src="/docs/research/images/speed/20240224_SJf_experimentelle-geschwindigkeitsdaten-optimiert_nicolas-huber.png" alt="Experimental Speed Data">
        <br>
        <em>Fig 72: Experimental Speed Data, optimized (03/31/2024)</em>
    </td>
    <td>
        <img src="/docs/research/images/speed/20240224_SJf_abweichung-experimentelle-geschwindigkeitsdaten-optimiert_nicolas-huber.png" alt="Deviation of Speed Data">
        <br>
        <em>Fig 73: Deviation of Speed Data, optimized (03/31/2024)</em>
    </td>
</tr>
</table>

#### Speed Data Analysis Report

The final report of the data analysis step can be seen below.

<details>
<summary>Show Report</summary>


```txt
Filtered data:
Report:
--> Optimized dataset is closer to the theoretical curve.
----> The precision (deviation of theoretical polar) of this dataset improved by 30.78% compared to the original dataset.
----> The area between the graphs within the limits 8 to 16 is smaller (better) by 42.84% compared to the original dataset.

--> Number of processed datapoints: 
----> Original dataset (before processing): 35 & after processing: 27
----> Optimized dataset (before processing): 19926 & after processing: 52
```

</details>

The initial 20,000 data points were filtered and grouped to create an optimized data set of 52 points. The summarized data set represents the approximation of the theoretical speed data.

According to the median of the distances between the theoretical and experimental velocity polars, the optimized data set is 30% more accurate than the data set from the original version of this paper.

According to the deviation area, however, the increase in quality of the velocity data is as much as 40%. This is particularly relevant for the reason that this data can be used for applied models.

#### Speed Data Analysis Conclusion

Thanks to the filtering and grouping of the raw data, the quality of the speed data improved by 30% or 40% compared to the original paper **Fliegen am Limit**, depending on the criterion. This increase in quality is welcome because all models based on it benefit from it.

However, the speed data is not perfect. Although the experimentally determined polar curve is much closer to the theoretical one than the original one thanks to the optimized pre-processing, the inaccuracies are twofold:

- Firstly, it is noticeable that the experimental polar curve for low horizontal velocities is significantly lower than the theoretical one. This is due to the fact that, despite careful filtering of the raw data, flights with significant wind influences were probably included in this analysis. Wind primarily changes the speed relative to the ground, i.e. the horizontal speed. The airspeed at the wing (True Airspeed, TAS) changed by the wind also has an effect on the vertical speed according to the theoretical polar curve; in the case of headwinds (as in this analysis, for example), the vertical speed drops drastically. This phenomenon can be prevented in future analyses by collecting an empirical data set in which even greater attention is paid to the wind conditions.
- Secondly, it is noticeable that the raw data in the high speed range shows a greater scatter than for lower speeds. This is due to the fact that these speeds are reached much less frequently and therefore the number of data points for this speed range is low. The certainty of the approximation of the theoretical polar curve decreases in this range, but this has no significant effect in this specific case when comparing the theoretical and experimental polar curve.

In summary, although there are two aspects that limit the accuracy of this analysis in this specific case, the approximated polar curve based on the optimized pre-processing is significantly more accurate and reliable, especially as the scatter of the data is greatly reduced compared to the original data set. The clear advantages of the new analysis are therefore the reduced area between the two curves and the reduced standard error.

### C Value Modeling

This analysis is based on the data set generated by the speed data analysis. A detailed report for the c value modeling step can be found [here](/docs/research/reports/20240224_SJf_data-analysis_nicolas-huber.html). Please find listed below some further documentation on the individual processing steps.

#### C Model Data Processing

In this step, the c-values for modeling the stationary glide are calculated for the entire optimized data set. This was concluded with the following report: 

<details>
<summary>Show Report</summary>


```txt
Manipulating datasets:
--> The datasets are being extended:
----> The original reference dataset is being extended with the airspeed, that's calculated based on horizontal and vertical speed.
----> The theoretical reference dataset is being extended with the airspeed, that's calculated based on horizontal and vertical speed.
----> The experimental dataset is being extended with the airspeed, that's calculated based on horizontal and vertical speed.
--> Vertical speeds are converted to be positive:
----> The vertical speeds of the original reference dataset are being converted to be positive.
----> The vertical speeds of the theoretical reference dataset are being converted to be positive.
----> The vertical speeds of the experimental dataset are being converted to be positive.
--> The datasets have been extended and manipulated.

C values:
--> Calculating the c values for the following conditions:
----> Altitude: 2000 m
----> Air density: 1.0065 kg/m^3
----> Gravity: 9.81 m/s^2
----> Wing area: 23.1 m^2
----> Takeoff mass: 90 kg
--> Calculating the c values for the following datasets:
----> The c values are being calculated for the original reference dataset (simplified & optimized algorithm).
----> The c values are being calculated for the theoretical reference dataset (simplified & optimized algorithm).
----> The c values are being calculated for the experimental dataset (simplified & optimized algorithm).
--> The c values have been calculated.
```

</details>

The environmental conditions assumed for this model are of particular importance here:

- Altitude: 2000m AMSL
- Air density: 1.0065 kg/m^2 according to ICAO standard atmosphere at 2000m AMSL altitude
- Gravitational acceleration: 9.81 m/s^2 at Zurich (CH)
- Wing area: 23.1 m^2 (Ozone Alpina 4, size MS)
- Takeoff mass: 90kg (mean value)

The following visualisation is based on the model ran for these conditions.

#### C Model Data Visualisation

For reference the theoretical plots for both the original and optimized c-algorithm can be found below.

<table>
<tr>
  <th>Theoretical Ca coefficients</th>
  <th>Theoretical Cw coefficients</th>
</tr>
<tr>
    <td>
        <img src="/docs/research/images/coefficients/20240224_SJf_theoretische-ca-werte-vereinfacht_nicolas-huber.png" alt="Theoretical Ca coefficients">
        <br>
        <em>Fig 74: Theoretical Ca coefficients (original c-algorithm)</em>
    </td>
    <td>
        <img src="/docs/research/images/coefficients/20240224_SJf_theoretische-cw-werte-vereinfacht_nicolas-huber.png" alt="Theoretical Cw coefficients">
        <br>
        <em>Fig 75: Theoretical Cw coefficients (original c-algorithm)</em>
    </td>
</tr>
<tr>
    <td>
        <img src="/docs/research/images/coefficients/20240224_SJf_theoretische-ca-werte-optimiert_nicolas-huber.png" alt="Theoretical Ca coefficients">
        <br>
        <em>Fig 76: Theoretical Ca coefficients (optimized c-algorithm)</em>
    </td>
    <td>
        <img src="/docs/research/images/coefficients/20240224_SJf_theoretische-cw-werte-optimiert_nicolas-huber.png" alt="Theoretical Cw coefficients">
        <br>
        <em>Fig 77: Theoretical Cw coefficients (optimized c-algorithm)</em>
    </td>
</tr>
</table>


Below is a matrix with the visualized results of this analysis, plotted against the theoretical curve of the optimized c-algorithm.

<table>
<tr>
  <th>Experimental Ca Approximation</th>
  <th>Experimental Cw Approximation</th>
</tr>
<tr>
    <td>
        <img src="/docs/research/images/coefficients/20240224_SJf_experimentelle-ca-werte-vereinfacht-original_nicolas-huber.png" alt="Experimental Ca coefficients">
        <br>
        <em>Fig 78: Experimental Ca coefficients (original c-algorithm, original data)</em>
    </td>
    <td>
        <img src="/docs/research/images/coefficients/20240224_SJf_experimentelle-cw-werte-vereinfacht-original_nicolas-huber.png">
        <br>
        <em>Fig 79: Experimental Cw coefficients (original c-algorithm, original data)</em>
    </td>
</tr>
<tr>
    <td>
        <img src="/docs/research/images/coefficients/20240224_SJf_experimentelle-ca-werte-vereinfacht-optimiert_nicolas-huber.png" alt="Experimental Ca coefficients">
        <br>
        <em>Fig 80: Experimental Ca coefficients (original c-algorithm, optimized data)</em>
    </td>
    <td>
        <img src="/docs/research/images/coefficients/20240224_SJf_experimentelle-cw-werte-vereinfacht-optimiert_nicolas-huber.png" alt="Experimental Ca coefficients">
        <br>
        <em>Fig 81: Experimental Cw coefficients (original c-algorithm, optimized data)</em>
    </td>
</tr>
<tr>
    <td>
        <img src="/docs/research/images/coefficients/20240224_SJf_experimentelle-ca-werte-optimiert-original_nicolas-huber.png" alt="Experimental Ca coefficients">
        <br>
        <em>Fig 82: Experimental Ca coefficients (optimized c-algorithm, original data)</em>
    </td>
    <td>
        <img src="/docs/research/images/coefficients/20240224_SJf_experimentelle-cw-werte-optimiert-original_nicolas-huber.png" alt="Experimental Ca coefficients">
        <br>
        <em>Fig 83: Experimental Cw coefficients (optimized c-algorithm, original data)</em>
    </td>
</tr>
<tr>
    <td>
        <img src="/docs/research/images/coefficients/20240224_SJf_experimentelle-ca-werte-optimiert-optimiert_nicolas-huber.png" alt="Experimental Ca coefficients">
        <br>
        <em>Fig 84: Experimental Ca coefficients (optimized c-algorithm, optimized data)</em>
    </td>
    <td>
        <img src="/docs/research/images/coefficients/20240224_SJf_experimentelle-cw-werte-optimiert-optimiert_nicolas-huber.png" alt="Experimental Ca coefficients">
        <br>
        <em>Fig 85: Experimental Cw coefficients (optimized c-algorithm, optimized data)</em>
    </td>
</tr>
</table>

Additionally, below is a matrix of plots that visualize the deviation of the experimental curves.

<table>
<tr>
  <th>Ca Deviation</th>
  <th>Cw Deviation</th>
</tr>
<tr>
    <td>
        <img src="/docs/research/images/coefficients/20240224_SJf_abweichung-ca-werte-vereinfacht-original_nicolas-huber.png" alt="Experimental Ca coefficients">
        <br>
        <em>Fig 86: Deviation of Ca approximation (original c-algorithm, original data)</em>
    </td>
    <td>
        <img src="/docs/research/images/coefficients/20240224_SJf_abweichung-cw-werte-vereinfacht-original_nicolas-huber.png" alt="Experimental Cw coefficients">
        <br>
        <em>Fig 87: Deviation of Cw approximation (original c-algorithm, original data)</em>
    </td>
</tr>
<tr>
    <td>
        <img src="/docs/research/images/coefficients/20240224_SJf_abweichung-ca-werte-vereinfacht-optimiert_nicolas-huber.png" alt="Experimental Ca coefficients">
        <br>
        <em>Fig 88: Deviation of Ca approximation (original c-algorithm, optimized data)</em>
    </td>
    <td>
        <img src="/docs/research/images/coefficients/20240224_SJf_abweichung-cw-werte-vereinfacht-optimiert_nicolas-huber.png" alt="Experimental Cw coefficients">
        <br>
        <em>Fig 89: Deviation of Cw approximation (original c-algorithm, optimized data)</em>
    </td>
</tr>
<tr>
    <td>
        <img src="/docs/research/images/coefficients/20240224_SJf_abweichung-ca-werte-optimiert-original_nicolas-huber.png" alt="Experimental Ca coefficients">
        <br>
        <em>Fig 90: Deviation of Ca approximation (optimized c-algorithm, original data)</em>
    </td>
    <td>
        <img src="/docs/research/images/coefficients/20240224_SJf_abweichung-cw-werte-optimiert-original_nicolas-huber.png" alt="Experimental Cw coefficients">
        <br>
        <em>Fig 91: Deviation of Cw approximation (optimized c-algorithm, original data)</em>
    </td>
</tr>
<tr>
    <td>
        <img src="/docs/research/images/coefficients/20240224_SJf_abweichung-ca-werte-optimiert-optimiert_nicolas-huber.png" alt="Experimental Ca coefficients">
        <br>
        <em>Fig 92: Deviation of Ca approximation (optimized c-algorithm, optimized data)</em>
    </td>
    <td>
        <img src="/docs/research/images/coefficients/20240224_SJf_abweichung-cw-werte-optimiert-optimiert_nicolas-huber.png" alt="Experimental Cw coefficients">
        <br>
        <em>Fig 93: Deviation of Cw approximation (optimized c-algorithm, optimized data)</em>
    </td>
</tr>
</table>

#### C Model Report

This analysis was completed with the following report:

<details>
<summary>Show Report</summary>

```txt
Scores:
--> The scores for the original reference dataset (simplified algorithm) are as follows:
----> Ca: 0.011526744113621777
----> Cw: 0.011244766543086862
--> The scores for the experimental dataset (simplified algorithm) are as follows:
----> Ca: 0.007462068907088727
----> Cw: 0.00826139444516371
--> The scores for the original reference dataset (optimized algorithm) are as follows:
----> Ca: 0.011526744113621777
----> Cw: 0.011244766543086862
--> The scores for the experimental dataset (optimized algorithm) are as follows:
----> Ca: 0.007462068907088727
----> Cw: 0.00826139444516371

Evaluation:
--> The lower the score, the better the algorithm.
--> The evaluation of the scores is as follows:
----> Relative to the original reference dataset (simplified algorithm), the experimental dataset (simplified algorithm) has a score of 0.0040646752065330504 for Ca and 0.002983372097923152 for Cw, which translates to a quality increase of 35.26299505277994% for Ca and 26.53120530774639% for Cw.
----> Relative to the original reference dataset (optimized algorithm), the experimental dataset (optimized algorithm) has a score of 0.0040646752065330504 for Ca and 0.002983372097923152 for Cw, which translates to a quality increase of 35.26299505277994% for Ca and 26.53120530774639% for Cw.

Final Score:
--> Relative to the original reference dataset (simplified algorithm), the experimental dataset (optimized algorithm) has a score of 0.0040646752065330504 for Ca and 0.002983372097923152 for Cw, which translates to a quality increase of 35.26299505277994% for Ca and 26.53120530774639% for Cw.
--> The final quality increase of the experimental dataset (optimized algorithm) relative to the original reference dataset (simplified algorithm) is 67.81054632037929%.
```

</details>

The modeling of the c-values shows a pleasing result: Compared to the original model in the paper of 10/24/2022, there has been an increase in quality of 20%+, which benefits models based on it, such as the modeling of the dynamic pressure. The difference between the simplified and the optimized c-algorithm is minimal, but the difference between the original and optimized data is very noticeable. The more accurate these models are, especially the modeling of these coefficients, the better algorithms based on them will work. For example, the simulation of the pressure situation on the wing offers great potential. Ultimately, the aim is to prevent dangerous states in flight, especially collapses, through accurate numerical prediction and these models bring this goal within reach. 

### Stagnation Pressure Modeling

One example of this is the simulation of the dynamic pressure at the wing. One of the decisive factors for the pressure situation inside the paraglider, which is relevant for predicting dangerous flight situations such as collapses, is the stagnation pressure. This is modeled below to demonstrate the potential of this tool. 

Please find listed below some graphs that visualize the stagnation pressure at the wing of an Ozone Alpina 4 paraglider.

<table>
<tr>
    <th>Stagnation Pressure</th>
    <th>Deviation</th>
</tr>
<tr>
    <td>
        <img src="/docs/research/images/pressure/20240224_SJf_experimentelle-modellierung-des-staudrucks_nicolas-huber.png" alt="Experimentelle Modellierung des Staudrucks">
        <br>
        <em>Fig. 94: Experimental Model of Stagnation Pressure</em>
    </td>
    <td>
        <img src="/docs/research/images/pressure/20240224_SJf_abweichung-des-staudrucks_nicolas-huber.png" alt="Tracklog">
        <br>
        <em>Fig. 95: Deviation of Stagnation Pressure</em>
    </td>
</tr>
</table>

This exemplary visualization brings together the various concepts and algorithms of the `flight-analyzer` tool and shows where this idea could lead to. The ability to model a wing so accurately based on experimental data opens up many exciting possibilities for predicting dangerous flight situations such as collapses.

### Quality Analysis

The `flight-analyzer` tool introduces many different new concepts for modeling the stationary glide of a paraglider or for predicting dangerous flight situations. Nevertheless, it should be seen as a tool built on the concepts presented in the original paper **Fliegen am Limit** dated 10/24/2022. In order to create comparable results and evaluations, a quality analysis is appropriate at the end of this research report.

In the original paper, the quality of the modeling of the stationary glide was checked by comparing the force resultant of lift and drag forces calculated by the model, which contains all previously processed variables such as velocity data, approximation functions and coefficients, with the expected weight force. In stationary glide in an unaccelerated, stable state, the weight force and the force resultant must cancel each other out. More on this can be found in the paper, but this relationship is the basis for the quality test.

Please find below a visualisation of the quality check:

<table>
<tr>
    <th>Original Model</th>
    <th>Optimized Model</th>
</tr>
<tr>
    <td>
        <img src="/docs/research/images/quality/20240224_SJf_quality-original_nicolas-huber.png" alt="Quality Check">
        <br>
        <em>Fig. 96: Original Model Deviation</em>
    </td>
    <td>
        <img src="/docs/research/images/quality/20240224_SJf_quality-optimiert_nicolas-huber.png" alt="Quality Check">
        <br>
        <em>Fig. 97: Optimized Model Deviation</em>
    </td>
</tr>
</table>

The quality analysis resolved with the following report:

<details>
<summary>Show Report</summary>

```txt
Quality analysis:
--> The reference calculations are conducted for all datapoints of the experimental dataset.
----> The mean deviation of the expected resulting force is 3.89 N.
----> The mean deviation percentage of the expected resulting force is 0.4 %.
--> The reference calculations are conducted for all datapoints of the original reference dataset using the approximation model of the original paper (p. 40, fig. 56)
----> The mean deviation of the expected resulting force is 86.39 N.
----> The mean deviation percentage of the expected resulting force is 8.99 %.
```

</details>

This analysis leads to the result that the new model with a deviation of 0.4% on average is very close to reality and thus generates a realistic image of the stationary glide. It should be noted at this point that the original model in the original paper shows a deviation of around 1.5% (in an exemplary sample calculation at a specific point in the dataset). However, the original paper did not check the quality of the entire data set, which partly explains the deviation between the versions in this analysis. Above all, however, it should be mentioned that the data pre-processing has improved significantly between the two versions of this paper. An important part of the accuracy of the optimized models is the improved data processing. In order to create a realistic comparison between the versions, the old model with the old conditions was confronted with the new model and the adjusted conditions, leading to this result and a quality difference of 8% when looking at this exemplary quality analysis.

Not only have the individual components of this model improved, but the improvement can also be seen in applied applications.

## Summary

The `flight-analyzer` application led to a general improvement in the quality of the evaluations and analyses of the paper compared to the original version of this paper. First, the experimental velocity polars could be improved and thus the basis for applied models could be strengthened. This can be seen, for example, in the quality analysis for the calculation of lift and drag forces as well as c-coefficients. In addition, the new analyses offer great potential for new models and simulations thanks to the increase in quality. One example of this is the modeling of the stagnation pressure at the wing and the application of the concept for the prediction of collapses. Most importantly, however, this system automates the entire analysis process. The relevance of this point becomes particularly clear if you want to apply the concepts of the paper to a paraglider that does not correspond to the Ozone Alpina 4. The `flight-analyzer` application changes the challenge of modelling different gliders and makes it possible to calculate simulations and models for any glider in no time at all - based on an empiric set of flight data - and, after a few adjustments to the software, to output prediction models for collapses for any glider in the future. In summary, this tool increases the quality of the analyses compared to the original, fully automates them, creates a scope for new algorithms and thus ensures accessibility for all gliders and pilots, while automating the whole process.

Great news!

---

_© 2024, [Nicolas Huber](https://nicolas-huber.ch). All rights reserved._