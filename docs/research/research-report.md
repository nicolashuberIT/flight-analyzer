# Research Report

[README](/README.md) > Docs > Research Report

This report describes how the analyses presented in the scientific paper **Fliegen am Limit - Aktive Sicherheit im Gleitschirmsport** came about. This includes the preprocessing as well as the optimization of the algorithms and finally the evaluation of the data. 

Happy reading!

## Contents

- [Research Report](#research-report)
  - [Contents](#contents)
  - [Empiric Dataset](#empiric-dataset)
  - [Testing](#testing)
  - [Algorithm Optimization](#algorithm-optimization)
    - [Overview](#overview)
    - [Optimization Runs](#optimization-runs)
      - [Run 1 - Limit 100 \& Step 5](#run-1---limit-100--step-5)
      - [Run 2 - Limit 150 \& Step 5](#run-2---limit-150--step-5)
      - [Run 3 - Limit 200 \& Step 5](#run-3---limit-200--step-5)
    - [Summary](#summary)
  - [Flight Data Analysis](#flight-data-analysis)
    - [Conditions](#conditions)
    - [Track Log Matrix](#track-log-matrix)
    - [Speed Data Analysis](#speed-data-analysis)
      - [Speed Data Data pre-processing](#speed-data-data-pre-processing)
    - [C Value Modelling](#c-value-modelling)
    - [Dynamic Pressure Modelling](#dynamic-pressure-modelling)
    - [Quality Analysis](#quality-analysis)
  - [Summary](#summary-1)

## Empiric Dataset

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

When the optimization is performed for these parameters, the algorithm forms a cartesian product of all combinations for `ANGLE_PAST_THRESHOLD` and `ANGLE_FUTURE_THRESHOLD` within the specified range and calculates how well this combination performs in the analysis of the flight data.

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

Run wan as executed for the following conditions:

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

Run wan as executed for the following conditions:

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

### Summary

Three calculation runs were carried out with different parameters to optimize the thresholds. All runs produced the same result. The optimization algorithm recommends the following thresholds for further analyses:

- By score:
  - `OPTIMIZATION_LIMIT` = 95
  - `OPTIMIZATION_STEP` = 90
- By ratio:
  - `OPTIMIZATION_LIMIT` = 10
  - `OPTIMIZATION_STEP` = 50

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

#### Speed Data Data pre-processing

The speed data analysis is based on the raw input data, which is read in from the `.igc` files. This data must first be filtered and cleaned so that it can be processed.

The system filters out all horizontal speeds that are not available for comparison in the theoretical reference data set. In addition, data points that lie on a curve or have been flagged as unusable for other reasons are filtered out. The system also ensures that only negative vertical velocities are included in the data set. In this way, disruptive factors such as thermals are excluded as far as possible. 

The report of this process can be found below:

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

As described in the report, many data points are lost during pre-processing of the raw data. However, this ensures that the data set is as clean as possible and disruptive factors are removed. In addition, the data is converted into a form that is useful for further modeling. The data is smoothed and grouped according to horizontal velocity. This is the basis for all further analysis.

### C Value Modelling

_Coming soon._

### Dynamic Pressure Modelling

_Coming soon._

### Quality Analysis

_Coming soon._

## Summary

_Coming soon._

---

_© 2024, [Nicolas Huber](https://nicolas-huber.ch). All rights reserved._