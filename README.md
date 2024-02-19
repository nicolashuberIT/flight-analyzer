# flight-analyzer
 
![Python](https://img.shields.io/badge/Python-3.9,3.10,3.11,3.12-blue)
[![License](https://img.shields.io/badge/License-INDIVIDUAL-blue)](#license--intellectual-property)
![Testing](https://github.com/nicolashuberIT/flight-analyzer/actions/workflows/testing.yaml/badge.svg)
![Formatting](https://img.shields.io/badge/formatting-Black-black)
![Linting](https://img.shields.io/badge/linting-Pylint-yellow)

## Overview

The `flight-analyzer` program is part of the scientific paper "Fliegen am Limit - Aktive Sicherheit im Gleitschirmsport", that was first published on 10/24/2022 and is being further developped by 03/31/2024 as of the "Schweizer Jugend forscht 2024" initiative. The application automates the analysis of paragliding flights and contains a selection of algorithms to process tracklogs. As part of the paper, this tool is designed to deliver a clean dataset that can be used to conduct and optimize advanced analyses and simulate the stationary glide of a paraglider. Please find a detailed description of the algorithms as well as concepts and findings in the sections below, in the paper itself or in the code.

Both the original and updated paper are listed below: 

<table style="width:100%">
  <tr>
    <th>Date</th>
    <th>Description</th>
    <th>Author</th>
    <th>Supervisor</th>
    <th>Context</th>
    <th>Link</th>
  </tr>
  <tr>
    <td>10/24/2022</td>
    <td>Original paper</td>
    <td>Nicolas Huber</td>
    <td>Albert Kern</td>
    <td>Kantonsschule Zürcher Oberland (KZO)</td>
    <td><a href="https://nicolas-huber.ch/docs/20221220_maturitaetsarbeit_fliegen-am-limit_public-version_nicolas-huber.pdf" target="_blank">nicolas-huber.ch/docs/...</a></td>
  </tr>
  <tr>
    <td>03/31/2024</td>
    <td>Updated paper</td>
    <td>Nicolas Huber</td>
    <td>Albert Kern, Ronald Luijten</td>
    <td>Schweizer Jugend forscht (SJf)</td>
    <td>coming soon</td>
  </tr>
</table>

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
  - [License \& Intellectual Property](#license--intellectual-property)
  - [Disclaimer](#disclaimer)

---

## Technical documentation

### Introduction

The goal of the `flight-analyzer` application is to automatically manipulate large datasets, which contain the track logs of paragliding flights. The program evaluates for each point of the flight if it is on a straight line or not, which is relevant for modelling the stationary glide of a paraglider. This allows further analyses and the filtering by position of the point. After the input dataset has been filtered the tool can apply a selection of algorithms, which have been developped as of the "Fliegen am Limit" paper, to simulate the stationary flight of a paraglider. This serves as a foundation for the development of new algorithms, more advanced models and to conduct further analyses. In addition, the tool offers some helpers such as tools to visualize the manipulated data or preprocess raw input files. 

Detailed descriptions can be found in docstrings and comments within the source code of this project. 

### Getting started

Make sure to install Python 3.9 or higher on your machine. The code has only been tested for the Python versions 3.9, 3.10, 3.11 and 3.12-dev and should properly work on MacOS, Ubuntu Linux and Windows. It's recommended to use pyenv to manage local python environments as well as dependencies. To run this project make sure to activate an environment that supports Python 3.9 or higher and then run `pip install -r requirements.txt`. The application should work fine with the dependencies (indicated version) listed in `requirements.txt`.

### Architecture

The application is structured as follows:

```txt
⎡ flight-analyzer
⎢ ⟶ .github/
⎢ ⟶ docs/
⎢   ⟶ datasets/
⎢   ⟶ documentation/
⎢   ⟶ images/
⎢   ⟶ optimization/
⎢   ⟶ research/
⎢ ⟶ src/
⎢   ⟶ algorithms/
⎢   ⟶ analysis/
⎢   ⟶ executor/
⎢   ⟶ helpers/
⎢   ⟶ packages/
⎢   ⟶ constants.py
⎢ ⟶ tests/
⎢ ⟶ main.ipynb
⎢ ⟶ LICENSE.md
⎢ ⟶ README.md
⎢ ⟶ requirements.txt
⎢ ⟶ testing.sh
⎢ ⟶ update_testing.sh
⎣
```

### Basic Usage

Please click [here](/docs/documentation/basic-usage.md) to read the `Basic Usage` documentation.

### Algorithms and helpers

Please click [here](/docs/documentation/algorithms-and-helpers.md) to read the `Algorithms and Helpers` documentation.

--- 

## Development

Please click [here](/docs/documentation/development.md) to read the `Development` documentation.

---

## License & Intellectual Property

The source code of this application is licensed under [this](LICENSE.md) license. Please click [here](/docs/documentation/license-and-intellectual-property.md) to read the `License & Intellectual Property` documentation.

---

## Disclaimer

The author is not responsible for any damage caused by the use of the software.

---

_© 2024, [Nicolas Huber](https://nicolas-huber.ch). All rights reserved._