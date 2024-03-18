# Basic usage

[README](/README.md) > Docs > Basic Usage

The main entry point of this application is the `main.ipynb` file. If you'd like to visualize data or run a specific analysis check out the `src/executors/` or `src/analysis` directories, which contain a collection of Jupyter Notebooks. Please find listed below some instructions for the Notebooks in `src/executors/`, the `main` script and some guidelines for preprocessing.

## Contents

- [Basic usage](#basic-usage)
  - [Contents](#contents)
  - [Preprocessing flight data](#preprocessing-flight-data)
  - [Running main.ipynb](#running-mainipynb)
  - [Run individual analysis](#run-individual-analysis)


## Preprocessing flight data

The flight data consumed by this program is read from `.igc files`, which are written by flight computers such as variometers or similar. This application offers the `IGC2CSV` package, that extracts tracklogs from `.igc` files and preprocesses the data to a format that is supported by the `flight-analyzer` algorithms. You can find further documentation on this tool linked [here](/docs/documentation/algorithms-and-helpers.md#igc2csv).

Alternatively, you can use [IGC2KML](https://igc2kml.com/) for `.igc` to `.kml` conversion and [KML2CSV](https://products.aspose.app/gis/conversion/kml-to-csv) for `.kml` to `.csv` conversion as well as Microsoft Excel to manually clean up the raw table data. Please find listed below some instructions for manual preprocessing.

After manually processing the tracklog using the linked tools you're dealing with `.csv` data of the following format: 

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

This data can then be preprocessed using the `FileConvertor` tool, which is linked [here](/src/helpers/file_convertor.py).

## Running main.ipynb

In order to run the main script of the `flight-analyzer` application make sure to prepare all necessary files and properly preprocess them. Please find instructions on preprocessing [here](#preprocessing-flight-data).

Documentation on using this notebook can be found at the top of the Jupyter Notebook, which can be found [here](/main.ipynb).

## Run individual analysis

To run a particular algorithm of the `flight-analyzer` application, e.g. to visualize data, please refer to the executor scripts that can be found in `src/executors/`. The algorithms and some examples can be found in the [Algorithms and Helpers](/docs/documentation/algorithms-and-helpers.md) documentation.

Check out the [src/executor](/src/executor/) or [src/analysis](/src/analysis/) directories to find a selection of data processing tools. 

---

_© 2024, [Nicolas Huber](https://nicolas-huber.ch). All rights reserved._