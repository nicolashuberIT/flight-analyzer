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
    - [Algorithms and helpers](#algorithms-and-helpers)
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

Please click [here](/docs/documentation/basic-usage.md) to read the `Basic Usage` documentation

### Algorithms and helpers

Please click [here](/docs/documentation/algorithms-and-helpers.md) to read the `Algorithms and Helpers` documentation.

--- 

## Development

### Conventions

Please find naming conventions for this project linked here: [click](/docs/documentation/docs-conventions.md). In addition, static type annotations are used in this project. The code is formatted and linted in VS Code using the Black Formatter Extension and Pylint.

### Testing

The codebase has been tested using the `pytest` module. The recent CI/CD status can be found at the top of this page. Click [here](https://github.com/nicolashuberIT/flight-analyzer/actions) for a detailed overview and unit testing logs. 

When running tests using pytest without specifying the test files explicitly, some tests fail with a FileNotFoundError. Interestingly, this issue did not occur with previous versions of the codebase. The reason for this error is unknown, and it appeared unexpectedly. Due to time constraints, the error wasn't further debugged, and the following workaround was implemented to ensure testing could proceed efficiently. 

To address this issue, the workaround involves explicitly specifying the test files to be executed in a shell script. By creating a shell script that lists all test files with their relative paths and then executing this script, pytest can properly locate the test files and run them without encountering FileNotFoundError. This ensures that pytest operates from the correct working directory and resolves file paths accurately.

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