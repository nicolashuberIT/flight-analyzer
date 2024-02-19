# Basic usage

The main entry points of this application are the `main.py` and `main.ipynb` files. Both the Python file and the Jupyter Notebook output the same result - you can chose the script that fits you best. If you'd like to visualize data or run a specific analysis check out the `src/executors/` directory, which contains a collection of Jupyter Notebooks. Please find listed below some instructions for the Notebooks in `src/executors/`, the `main` scripts and some guidenines for preprocessing.

## Contents

- [Basic usage](#basic-usage)
  - [Contents](#contents)
  - [Preprocessing flight data](#preprocessing-flight-data)
  - [Running main.py / main.ipynb](#running-mainpy--mainipynb)
  - [Run individual analysis](#run-individual-analysis)


## Preprocessing flight data

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

## Running main.py / main.ipynb

In order to run the main script of the `flight-analyzer` application make sure to prepare all necessary files and properly preprocess them. Please find instructions on preprocessing [here](#preprocessing-flight-data).

_Further documentation will follow as soon as the `main` script have been developped and properly tested._

## Run individual analysis

To run a particular algorithm of the `flight-analyzer` application, e.g. to visualize data, please refer to the executor scripts that can be found in `src/executors/`. The algorithms and some examples can be found in the [Algorithms and helpers](#algorithms-and-helpers) section.

This application provides the following executor Notebooks:

- `execute_file_convertor.ipynb`: This Notebook allows you to normalize the manually preprocessed data. 
- `execute_angle_analyzer.ipynb`: This Notebook allows you to process a normalized dataset. The AngleAnalyzer algorithm is applied. 
- `execute_data_analyzer.ipynb`: This Notebook allows you to extract points on a straight line from a processed dataset based on the AngleAnalyzer algorithm.
- `execute_optimize_thresholds.ipynb`: This Notebook allows you to automatically determine the best thresholds and constants to process your dataset (run before data analysis).

Further documentation on the inputs and outputs of these executors can be found in the Notebooks.

---

_© 2024, [Nicolas Huber](https://nicolas-huber.ch). All rights reserved._