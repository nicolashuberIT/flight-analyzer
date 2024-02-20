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

- `OPTIMIZATION_LIMIT` - defines the highest threshold that's to be tested
- `OPTIMIZATION_STEPS` - defines the step size between the tested thresholds

When the optimization is performed for these parameters, the algorithm forms a cartesian product of all combinations for `ANGLE_PAST_THRESHOLD` and `ANGLE_FUTURE_THRESHOLD` and calculates how well this combination performs in the analysis of the flight data.

The basis for this optimization is the track log visualized below. The raw file can be found [here](/docs/datasets/empiric-study/1_raw/20240216_SJf_skytraxx-2.1-export_flight-nr-22.igc), the corresponding `.csv` file can be found [here](/docs/datasets/empiric-study/2_csv/20240216_SJf_skytraxx-2.1-export_flight-nr-22.csv).

<table>
<tr>
  <th>Analyzed track log</th>
</tr>
<tr>
  <td>
    <img src="/docs/optimization/input/20240220_SJf_threshold-optimization_flight-visualisation_nicolas-huber.png" alt="Tracklog">
      <br>
      <em>Fig. 1: Track log visualisation</em>
    </td>
</tr>
</table>

---

_© 2024, [Nicolas Huber](https://nicolas-huber.ch). All rights reserved._