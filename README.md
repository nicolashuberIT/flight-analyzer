# flight-analyzer
 
[![nicolashuberIT - flight-analyzer](https://img.shields.io/static/v1?label=nicolashuberIT&message=flight-analyzer&color=blue&logo=github)](https://github.com/nicolashuberIT/flight-analyzer "Go to GitHub repo")
![automated testing](https://github.com/nicolashuberIT/flight-analyzer/actions/workflows/ci.yaml/badge.svg)
[![License](https://img.shields.io/badge/License-INDIVIDUAL-blue)](#license)

## Abstract

Abstract

---

## License & Intellectual Property

The source code of this application is licensed under the license linked [here](LICENSE.md).

If not stated differently, the source code of this project is Nicolas Huber's intellectual property. External sources can be found in the code and are marked as such. Additionally, to improve code quality and speed up workflows, tools like GitHub Copilot and ChatGPT were used. AI generated content is flagged with the following note: 

- For documentation files: _This document { TITLE } has been written by { SOURCE } and verified by Nicolas Huber on { DATE }._
- For code snippets: _# AI content ({ SOURCE }, { DATE }), verified and adapted by Nicolas Huber._

AI tools are a powerful and valuable addition to improve the development workflow, as long as sources and contents are scientifically listed.

In consideration of the `LICENSE.md`, the licensee, who is considered as such at the point of downloading this application, agrees to respect the terms and conditions. The licensee undertakes to show respect for Nicolas Huber's intellectual property and to use it only in accordance with his instructions.

Thanks for noticing! 

---

## Technical documentation

### Introduction

Detailed descriptions can be found in docstrings and comments within the source code of this project. Please find listed below some important aspects to get started.

### Getting started

Make sure to install `Python 3.12.0` on your machine. The code has only been tested for this Python version and should properly work on MacOS, Linux distributions and Windows. It's recommended to use pyenv to manage local python environments as well as dependencies. To run this project make sure to activate an environment that supports Python 3.12.0 and then run `pip install -r requirements.txt`

#### Basic Usage

Basic usage

### Architecture

The application is structured as follows:

```txt
flight-analyzer
|-- .github/
|-- assets/
|-- docs/
|-- src/
|-- |-- helpers/
|-- tests/
|-- main.py
|-- LICENSE.md
|-- README.md
```

### Conventions

Please find naming conventions for this project linked here: [click](/docs/docs-conventions.md). In addition, static type indications are used in this project. Most of the codebase has been tested using the `pytest` module. The recent CI/CD status can be found at the top of this page. Click [here](https://github.com/nicolashuberIT/flight-analyzer/actions) for a detailed overview and unit testing logs. The code is formatted and linted in VS Code using the Black Formatter Extension and Pylint.

### Contributing

At this time, the `flight-analyzer` project is not open for community contributions. The development is currently handled exclusively by Nicolas Huber. Your interest is appreciated and this section will be updated if the policy changes in the future.

### Changelog

- **1.0.0** - Not released yet.

---

## Disclaimer

The author is not responsible for any damage caused by the use of the software.

---

_© 2024, [Nicolas Huber](https://nicolas-huber.ch). All rights reserved._