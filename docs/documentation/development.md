# Development

[README](/README.md) > Docs > Development

## Contents

- [Development](#development)
  - [Contents](#contents)
  - [Conventions](#conventions)
  - [Testing](#testing)
    - [Issues and Workaround](#issues-and-workaround)
  - [Contributing](#contributing)
  - [Changelog](#changelog)

## Conventions

Please find naming conventions for this project linked here: [click](/docs/documentation/docs-conventions.md). In addition, static type annotations are used in this project. The code is formatted and linted in VS Code using the Black Formatter Extension and Pylint.

## Testing

The codebase has been tested using the `pytest` module. The recent CI/CD status can be found at the top of this page. Click [here](https://github.com/nicolashuberIT/flight-analyzer/actions) for a detailed overview and unit testing logs. 

### Issues and Workaround

When running tests using pytest without specifying the test files explicitly, some tests fail with a FileNotFoundError. Interestingly, this issue did not occur with previous versions of the codebase. The reason for this error is unknown, and it appeared unexpectedly. Due to time constraints, the error wasn't further debugged, and the following workaround was implemented to ensure testing could proceed efficiently. 

To address this issue, the workaround involves explicitly specifying the test files to be executed in a shell script. By creating a shell script that lists all test files with their relative paths and then executing this script, pytest can properly locate the test files and run them without encountering FileNotFoundError. This ensures that pytest operates from the correct working directory and resolves file paths accurately.

For reference, check [testing.sh](/testing.sh), [update_testing.sh](/update_testing.sh) and [testing.yaml](https://github.com/nicolashuberIT/flight-analyzer/blob/main/.github/workflows/testing.yaml).

To run unit tests locally, run `./update_testing.sh` from the base directory of this project and then initialize pytest by running `./testing.sh`.

## Contributing

At this time, the `flight-analyzer` project is not open for community contributions. The development is currently handled exclusively by Nicolas Huber. Your interest is appreciated and this section will be updated if the policy changes in the future.

## Changelog

- **[1.0.0]** - Not released yet.

---

_© 2024, [Nicolas Huber](https://nicolas-huber.ch). All rights reserved._
