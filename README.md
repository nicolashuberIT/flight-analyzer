# flight-analyzer
 
[![nicolashuberIT - flight-analyzer](https://img.shields.io/static/v1?label=nicolashuberIT&message=flight-analyzer&color=blue&logo=github)](https://github.com/nicolashuberIT/flight-analyzer "Go to GitHub repo")
![Testing](https://github.com/nicolashuberIT/flight-analyzer/actions/workflows/testing.yaml/badge.svg)
![Python 3.12](https://img.shields.io/badge/Python-3.12.0-blue)
![Formatting](https://img.shields.io/badge/formatting-Black-black)
![Linting](https://img.shields.io/badge/linting-Pylint-yellow)
[![License](https://img.shields.io/badge/License-INDIVIDUAL-blue)](#license--intellectual-property)

## Overview

The `flight-analyzer` program is part of the scientific paper "Fliegen am Limit - Aktive Sicherheit im Gleitschirmsport", that was first published on 10/24/2022 and is being further developped by 03/31/2024 as of the "Schweizer Jugend forscht 2024" initiative. The application is designed to analyze flight data that was recorded by devices such as variometers or other flight trackers commonly used by the paragliding community. The program provides tools to clean up the input data after it has manually been processed using the utilities [IGC2KML (.igc -> .kml)](https://igc2kml.com/) and [KML2CSV (.kml -> .csv)](https://products.aspose.app/gis/conversion/kml-to-csv) as well as Microsoft Excel. It also allows to combine, filter and sort multiple datasets. The main functionality of the tool is the application of a selection of algorithms to filter the flight data. As part of the scientific paper, this tool is designed to deliver a clean dataset that can be used to do optimized analyses and compare them to the first version of this paper, which was published in 2022. Please find a detailed description of the algorithms in the sections below, in the paper itself or in the code.

The original paper (10/24/2022) can be downloaded here: [nicolas-huber.ch/docs](https://nicolas-huber.ch/docs/20221220_maturitaetsarbeit_fliegen-am-limit_public-version_nicolas-huber.pdf).

As soon as the refined version of V1 has been published, the links will be listed here. Until then, please refer to the version linked above.

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

## Technical documentation

### Introduction

The goal of the `flight-analyzer` application is to automatically manipulate large datasets, which contain the track logs of paragliding flights. The program evaluates for each point of the flight if it is on a straight line or not. An executed example for an individual point can be found [here](https://github.com/nicolashuberIT/flight-analyzer/blob/main/src/executor/execute_angle_analyzer.ipynb). The program will output a new dataset containing an index for each point. This allows further analysis and the filtering by position of the point. In addition, the tool offers some helpers such as data visualizers or data animators. 

Detailed descriptions can be found in docstrings and comments within the source code of this project. Please find listed below some important aspects to get started. 

### Getting started

Make sure to install `Python 3.12.0` on your machine. The code has only been tested for this Python version and should properly work on MacOS, Linux distributions and Windows. It's recommended to use pyenv to manage local python environments as well as dependencies. To run this project make sure to activate an environment that supports Python 3.12.0 and then run `pip install -r requirements.txt`. The application should work fine with the dependencies (indicated version) listed in `requirements.txt`.

#### Basic Usage

This section will be added as soon as the development work is completed.

### Architecture

The application is structured as follows:

```txt
⎡ flight-analyzer
⎢⎬ .github/
⎢⎬ assets/
⎢⎬ docs/
⎢⎬ → datasets/
⎢⎬ → reports/
⎢⎬ src/
⎢⎬ → algorithms/
⎢⎬ → executor/
⎢⎬ → helpers/
⎢⎬ → constants.py
⎢⎬ tests/
⎢⎬ main.py
⎢⎬ main.ipynb
⎢⎬ LICENSE.md
⎢⎬ README.md
⎢⎬ requirements.txt
⎣
```

### Conventions

Please find naming conventions for this project linked here: [click](/docs/docs-conventions.md). In addition, static type annotations are used in this project. The codebase has been tested using the `pytest` module. The recent CI/CD status can be found at the top of this page. Click [here](https://github.com/nicolashuberIT/flight-analyzer/actions) for a detailed overview and unit testing logs. The code is formatted and linted in VS Code using the Black Formatter Extension and Pylint.

### Contributing

At this time, the `flight-analyzer` project is not open for community contributions. The development is currently handled exclusively by Nicolas Huber. Your interest is appreciated and this section will be updated if the policy changes in the future.

### Changelog

- **[1.0.0]** - Not released yet.

---

## Disclaimer

The author is not responsible for any damage caused by the use of the software.

---

_© 2024, [Nicolas Huber](https://nicolas-huber.ch). All rights reserved._