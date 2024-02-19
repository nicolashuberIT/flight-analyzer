# flight-analyzer
 
![Python](https://img.shields.io/badge/Python-3.9,3.10,3.11,3.12-blue)
[![License](https://img.shields.io/badge/License-INDIVIDUAL-blue)](#license--intellectual-property)
![Testing](https://github.com/nicolashuberIT/flight-analyzer/actions/workflows/testing.yaml/badge.svg)
![Formatting](https://img.shields.io/badge/formatting-Black-black)
![Linting](https://img.shields.io/badge/linting-Pylint-yellow)

## Overview

The `flight-analyzer` program is part of the scientific paper "Fliegen am Limit - Aktive Sicherheit im Gleitschirmsport", that was first published on 10/24/2022 and is being further developped by 03/31/2024 as of the "Schweizer Jugend forscht 2024" initiative. The application automates the analysis of paragliding flights and contains a selection of algorithms to process tracklogs. As part of the paper, this tool is designed to deliver a clean dataset that can be used to conduct and optimize advanced analyses and simulate the stationary glide of a paraglider. Please find a detailed description of the algorithms as well as concepts and findings in the sections below, in the paper itself or in the code.

The original paper (10/24/2022) can be downloaded here: [nicolas-huber.ch/docs](https://nicolas-huber.ch/docs/20221220_maturitaetsarbeit_fliegen-am-limit_public-version_nicolas-huber.pdf).

As soon as the refined version of the 2022 version has been published, the link will be listed here. Until then, please refer to the original paper.

---

## Contents

- [flight-analyzer](#flight-analyzer)
  - [Overview](#overview)
  - [Contents](#contents)
  - [Technical documentation](#technical-documentation)
    - [Introduction](#introduction)
    - [Getting started](#getting-started)
    - [Architecture](#architecture)
    - [Basic Usage](#basic-usage)
      - [Preprocessing flight data](#preprocessing-flight-data)
      - [Running main.py / main.ipynb](#running-mainpy--mainipynb)
      - [Run individual analysis](#run-individual-analysis)
    - [Algorithms and helpers](#algorithms-and-helpers)
      - [FileConvertor](#fileconvertor)
      - [AngleAnalyzer](#angleanalyzer)
      - [DataAnalyzer](#dataanalyzer)
      - [ThresholdOptimizer](#thresholdoptimizer)
  - [Development](#development)
    - [Conventions](#conventions)
    - [Testing](#testing)
    - [Contributing](#contributing)
    - [Changelog](#changelog)
  - [License \& Intellectual Property](#license--intellectual-property)
  - [Disclaimer](#disclaimer)

---

## Technical documentation

### Introduction

The goal of the `flight-analyzer` application is to automatically manipulate large datasets, which contain the track logs of paragliding flights. The program evaluates for each point of the flight if it is on a straight line or not, which is relevant for modelling the stationary glide of a paraglider. This allows further analyses and the filtering by position of the point. After the input dataset has been filtered the tool can apply a selection of algorithms, which have been developped as of the "Fliegen am Limit" paper, to simulate the stationary flight of a paraglider. This serves as a foundation for the development of new algorithms, more advanced models and to conduct further analyses. In addition, the tool offers some helpers such as tools to visualize the manipulated data or preprocess raw input files. 

Detailed descriptions can be found in docstrings and comments within the source code of this project. 

### Getting started

Make sure to install `Python 3.9` or higher on your machine. The code has only been tested for the Python versions 3.9, 3.10, 3.11 and 3.12-dev and should properly work on MacOS, Ubuntu Linux and Windows. It's recommended to use pyenv to manage local python environments as well as dependencies. To run this project make sure to activate an environment that supports Python 3.9 or higher and then run `pip install -r requirements.txt`. The application should work fine with the dependencies (indicated version) listed in `requirements.txt`.

### Architecture

The application is structured as follows:

```txt
⎡ flight-analyzer
⎢ ⟶ .github/
⎢ ⟶ assets/
⎢ ⟶ docs/
⎢   ⟶ datasets/
⎢   ⟶ reports/
⎢ ⟶ src/
⎢   ⟶ algorithms/
⎢   ⟶ executor/
⎢   ⟶ helpers/
⎢   ⟶ constants.py
⎢ ⟶ tests/
⎢ ⟶ main.py
⎢ ⟶ main.ipynb
⎢ ⟶ LICENSE.md
⎢ ⟶ README.md
⎢ ⟶ requirements.txt
⎣
```

### Basic Usage

The main entry points of this application are the `main.py` and `main.ipynb` files. Both the Python file and the Jupyter Notebook output the same result - you can chose the script that fits you best. If you'd like to visualize data or run a specific analysis check out the `src/executors/` directory, which contains a collection of Jupyter Notebooks. Please find listed below some instructions for the Notebooks in `src/executors/`, the `main` scripts and some guidenines for preprocessing.

#### Preprocessing flight data

The flight data consumed by this program is read from `.igc files`, which are written by flight computers such as variometers or similar. Reading these files is currently not fully supported in this program, which is why external applications are used. It's recommended to use [IGC2KML](https://igc2kml.com/) for `.igc` to `.kml` conversion and [KML2CSV](https://products.aspose.app/gis/conversion/kml-to-csv) for `.kml` to `.csv` conversion as well as Microsoft Excel to clean up the raw table data.

After processing the tracklog using the linked tools you're dealing with `.csv` data of the following format: 

<details>
<summary>Show Data</summary>

```txt
name,description,altitudeMode,visibility,tessellate,WKT
<<< SOME RANDOM HTML>>>
"12:25:30 0m 5kmh 0m/s 0km",,"clampToGround",,"true","LINESTRING Z (7.530683 46.213083 2612, 7.5307 46.213083 2612)"
"12:25:31 1m 0kmh +1m/s 0km",,"clampToGround",,"true","LINESTRING Z (7.5307 46.213083 2612, 7.5307 46.213083 2612)"
...
```
</details>

This data is to be processed using a tool like Microsoft Excel to remove the HTML content that's marked as `<<< SOME RANDOM HTML>>>` as well as clean up the data. After your final manual preprocessing steps the `.csv` data is supposed to look like this:

<details>
<summary>Show Data</summary>

```txt
name,description,altitudeMode,visibility,tessellate,WKT
12:25:30 0m 5kmh 0m/s 0km,,clampToGround,,TRUE,"LINESTRING Z (7.530683 46.213083 2612, 7.5307 46.213083 2612)"
12:25:31 1m 0kmh +1m/s 0km,,clampToGround,,TRUE,"LINESTRING Z (7.5307 46.213083 2612, 7.5307 46.213083 2612)"
```

</details>

Please check your input data before running any of the algorithms in this application to prevent unexpected errors. The preprocessed input is consumed by the `main` scripts in `.csv` or `.xlsx` format. It can also be manually fed into the `FileConvertor` helper class, on which further records can be found [here](#algorithms-and-helpers).

To quickly parse a big number of .igc files, e.g. to evaluate which flights are suited to be analyzed in the `flight-analyzer` application, you can also use the `IGC2CSV` package. The source code of this package can be found [here](/src/packages/IGC2CSV.py). This tool parses .igc files and either outputs a csv file or a DataFrame containing flight data in the same format as the `FileConvertor` does. However, in the current state, this tool reads data with the `altitudeMode` attribute set to `clampToGround`, which means the output only contains datapoints with a altitude relative to ground, rather than an altitude relative to takeoff as with `altitudeMode` set to `absolute`. Most trackers only record a datapoint with altitude relative to ground (sea level) every few seconds. Hence the data resolution can be very poor, which is why it is not recommended to use this package to preprocess data for further analyses using the `flight-converter` application. Still, this algorithm can be very useful in the process of preprocessing tracklogs for further analyses, as it can be used to quickly visualize a large number of flights to manually evaluate which one is suited for bein processed by the other algorithms of this application. An analysis tool that visualises all tracklogs from files in a indicated directory can be found [here](/src/analysis/analyze_tracklogs.ipynb). 

For now, it is not recommended to use the `IGC2CSV` package for preprocessing. This algorithm might be adapted to extracting data with `altitudeMode` set to `absolute`, but for now please stick with the manual preprocessing using the tools listed above for optimal data quality, which is critical.

#### Running main.py / main.ipynb

In order to run the main script of the `flight-analyzer` application make sure to prepare all necessary files and properly preprocess them. Please find instructions on preprocessing [here](#preprocessing-flight-data).

_Further documentation will follow as soon as the `main` script have been developped and properly tested._

#### Run individual analysis

To run a particular algorithm of the `flight-analyzer` application, e.g. to visualize data, please refer to the executor scripts that can be found in `src/executors/`. The algorithms and some examples can be found in the [Algorithms and helpers](#algorithms-and-helpers) section.

This application provides the following executor Notebooks:

- `execute_file_convertor.ipynb`: This Notebook allows you to normalize the manually preprocessed data. 
- `execute_angle_analyzer.ipynb`: This Notebook allows you to process a normalized dataset. The AngleAnalyzer algorithm is applied. 
- `execute_data_analyzer.ipynb`: This Notebook allows you to extract points on a straight line from a processed dataset based on the AngleAnalyzer algorithm.
- `execute_optimize_thresholds.ipynb`: This Notebook allows you to automatically determine the best thresholds and constants to process your dataset (run before data analysis).

Further documentation on the inputs and outputs of these executors can be found in the Notebooks.

### Algorithms and helpers

Some key aspects of the program's algorithms are described below. Note that the detailed documentation can be found in the docstrings and in comments in the code. Please note that the data and plots below are merely examples and the exact results can be found in the version of the paper dated 03/31/2024.

#### FileConvertor

The `FileConvertor` is a helper class that converts the manually preprocessed data, which is documented [here](#preprocessing-flight-data), to data that can be consumed by the algorithms of this application. Additionally, this class filters the raw data: It removes entries where the `altitudeMode` property is set to `clampToGround` and it removes entries of horizontal speed 0. The input data is in form of `.csv` or `.xlsx` and in the following structure:

```txt
name,description,altitudeMode,visibility,tessellate,WKT
12:25:30 0m 5kmh 0m/s 0km,,clampToGround,,TRUE,"LINESTRING Z (7.530683 46.213083 2612, 7.5307 46.213083 2612)"
...
```

After executing the `FileConvertor` for a manually preprocessed file the data looks like this:

```txt
timestamp [UTC],relative altitude [m],horizontal velocity [m/s],vertical velocity [m/s],distance to takeoff [km],longitude,latitude
12:25:30,0.0,1.39,0.0,0.0,7.530683,46.213083
...
```

You can manually execute the `FileConvertor` using [this](/src/executor/execute_file_convertor.ipynb) executor notebook. The source code of this class can be seen [here](/src/helpers/file_convertor.py).

#### AngleAnalyzer

The `AngleAnalyzer` class is designed to analyze flight trajectories at a specific point by examining the angles between successive points. It reads flight data from a CSV file and calculates angles between points, determining if they form a straight line or a curve. Using provided thresholds, it extracts past and future coordinates, filters out zero angles, and performs both angle-based and linear regression analyses. These analyses help classify flight segments as either straight lines or curves. 

The input for the following examples was [this](/docs/datasets/tracklogs/1_examples/2_normalized/20211016_tracklog-normalized_nicolas-huber.csv) file.
The examples used the conditions in the box below:

<details>
<summary>Conditions</summary>

```Python
INDEX: int = 1400 # point to be analyzed

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
      <img src="/docs/images/20240215_flight-analyzer_punktvariation-mit-relativer-hoehe_nicolas-huber.png" alt="Punktvariation mit relativer Höhe">
      <br>
      <em>Fig. 1: Point variation with relative height</em>
    </td>
    <td style="width: 50%; text-align: center;">
      <img src="/docs/images/20240215_flight-analyzer_winkelvariation_nicolas-huber.png" alt="Winkelvariation">
      <br>
      <em>Fig. 2: Angle variation</em>
    </td>
  </tr>
  <tr>
    <td style="width: 50%; text-align: center;">
      <img src="/docs/images/20240215_flight-analyzer_punktvariation-mit-linearer-regression-vergangenheit_nicolas-huber.png" alt="Lineare Regression (Vergangenheit)">
      <br>
      <em>Fig. 3: Linear regression (past)</em>
    </td>
    <td style="width: 50%; text-align: center;">
      <img src="/docs/images/20240215_flight-analyzer_punktvariation-mit-linearer-regression-zukunft_nicolas-huber.png" alt="Lineare Regression (Zukunft)">
      <br>
      <em>Fig. 4: Linear regression (future)</em>
    </td>
  </tr>
</table>

As you can easily tell by eye the analysed point lies on a straight line. This can be seen in figure 1. Figure 2 is a visualization of the angle variaton of the analysed points, the blue line representing the analysed point. The data behind this plot is calculated by comparing the angle between the datapoint and other trackpoints of the series within the thresholds. More precisely, the slope of the straight line between the analyzed point and the current point is compared with the slope of the first line between the analyzed point and the subsequent point. Additionally, as shown in figures 3 and 4, the program also runs a linear regression analysis that is validated against the angle analysis for both the past and future values. These analyses result in a categorization of that specific datapoint, which in this case is:

<details>
<summary>Output</summary>

```txt
Angle Analysis
--> Past: True
--> Future: True

Past Linear Regression
--> Status: True
--> Slope: 0.24496415928278734
--> Intercept: 44.41611343989336
--> R-Value: 0.9970350725539303
--> P-Value: 1.2004630598704919e-88
--> Standard Error: 0.0021406452009797685

Future Linear Regression
--> Status: True
--> Slope: 0.11306255384150318
--> Intercept: 45.41304614404877
--> R-Value: 0.9736381906284354
--> P-Value: 9.2965712930775e-23
--> Standard Error: 0.004610898882940768

Data Analysis
--> Status: (True, 'Straight Line', 0)
```
</details>

You can manually execute the `AngleAnalyzer` using [this](/src/executor/execute_angle_analyzer.ipynb) executor. The source code of this algorithm can be found [here](/src/algorithms/angle_analyzer.py).

#### DataAnalyzer

The `DataAnalyzer` class conducts thorough analysis of flight trajectory data by systematically applying the `AngleAnalyzer` class to every single trackpoint. This process enables the determination of whether each point lies on a straight line or a curve. It reads flight data from a CSV file, processes it by extracting past and future coordinates for each point, and performs angle-based and linear regression analyses. The analysis results, including the classification of each point as belonging to a straight-line segment or a curved segment, are appended to the dataset. Finally, the processed data, enriched with analysis outcomes, is exported to a new CSV file. This systematic approach empowers the identification of different trajectory characteristics throughout the flight path.

The input for the following examples was [this](/docs/datasets/tracklogs/1_examples/2_normalized/20211016_tracklog-normalized_nicolas-huber.csv) file.
The examples used the conditions in the box below:

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
      <img src="/docs/images/20240215_flight-analyzer_punktvariation-mit-position-und-kategorisierung_nicolas-huber.png" alt="Kategorisierung der Punkte">
      <br>
      <em>Fig. 5: Point position and categorization</em>
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

#### ThresholdOptimizer

The `ThresholdOptimizer` class optimizes thresholds for the `AngleAnalyzer` algorithm by systematically testing different combinations and scoring them based on specified criteria. It iteratively evaluates threshold combinations using a `DataAnalyzer` object, calculating scores derived from linear regression values and weighted metrics. The class then selects the best-scoring threshold combinations and exports the tested combinations to a CSV file. By providing insights into the trade-offs between different threshold settings, this class enables the fine-tuning of the `AngleAnalyzer` to achieve optimal performance.

The input for the following examples was [this](/docs/datasets/tracklogs/1_examples/2_normalized/20211016_tracklog-normalized_nicolas-huber.csv) file.
The examples used the conditions in the box below:

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
      <em>Fig. 6: Optimization score and data loss</em>
    </td>
    <td style="width: 50%; text-align: center;">
      <img src="/docs/images/20240215_flight-analyzer_optimierung-der-thresholds_nicolas-huber.png" alt="Optimierung der Thresholds">
      <br>
      <em>Fig. 7: Threshold optimization</em>
    </td>
  </tr>
</table>

Figure 6 plots both the optimization score and the data loss for this threshold combination on a normalized scale. Figure 7 shows how the 3 relevant linear regression values are weighted for the analysis. This specific run led to the following results:

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

--- 

## Development

### Conventions

Please find naming conventions for this project linked here: [click](/docs/docs-conventions.md). In addition, static type annotations are used in this project. The code is formatted and linted in VS Code using the Black Formatter Extension and Pylint.

### Testing

The codebase has been tested using the `pytest` module. The recent CI/CD status can be found at the top of this page. Click [here](https://github.com/nicolashuberIT/flight-analyzer/actions) for a detailed overview and unit testing logs. 

When running tests using pytest without specifying the test files explicitly, some tests fail with a FileNotFoundError. Interestingly, this issue did not occur with previous versions of the codebase. The reason for this error is unknown, and it appeared unexpectedly. Due to time constraints, the error wasn't further debugged, and the following workaround was implemented to ensure testing could proceed efficiently. 

To address this issue, a workaround involves explicitly specifying the test files to be executed in a shell script. By creating a shell script that lists all test files with their relative paths and then executing this script, pytest can properly locate the test files and run them without encountering FileNotFoundError. This ensures that pytest operates from the correct working directory and resolves file paths accurately.

For reference, check [testing.sh](/testing.sh), [update_testing.sh](/update_testing.sh) and [testing.yaml](https://github.com/nicolashuberIT/flight-analyzer/blob/main/.github/workflows/testing.yaml).

To run unit tests locally, run `./update_testing.sh` from the base directory of this project and then initialize pytest by running `./testing.sh`.

### Contributing

At this time, the `flight-analyzer` project is not open for community contributions. The development is currently handled exclusively by Nicolas Huber. Your interest is appreciated and this section will be updated if the policy changes in the future.

### Changelog

- **[1.0.0]** - Not released yet.

---

## License & Intellectual Property

The source code of this application is licensed under the license linked [here](LICENSE.md).

If not stated differently, the source code of this project is Nicolas Huber's intellectual property. External sources can be found in the code and are marked as such. Additionally, to improve code quality and speed up workflows, tools like GitHub Copilot and ChatGPT were used. AI generated content is flagged with the following notes: 

- For documentation files: _This document { TITLE } has been written by { SOURCE } and verified by Nicolas Huber on { DATE }._
- For code snippets: _# AI content ({ SOURCE }, { DATE }), verified and adapted by Nicolas Huber._

AI tools are a powerful and valuable addition to improve the development workflow, as long as sources and contents are scientifically listed. Thus, it's valued a lot to provide proper listings. The following utilities have been used: [GitHub Copilot](https://github.com/features/copilot), [ChatGPT](https://chat.openai.com/).

In consideration of the `LICENSE.md`, the licensee, who is considered as such at the point of downloading this application, agrees to respect the terms and conditions. The licensee undertakes to show respect for Nicolas Huber's intellectual property and to use it only in accordance with his instructions.

Thanks for noticing! 

---

## Disclaimer

The author is not responsible for any damage caused by the use of the software.

---

_© 2024, [Nicolas Huber](https://nicolas-huber.ch). All rights reserved._