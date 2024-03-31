# Development

[README](/README.md) > Docs > Development

## Contents

- [Development](#development)
  - [Contents](#contents)
  - [Conventions](#conventions)
  - [Testing](#testing)
  - [Contributing](#contributing)
  - [Changelog](#changelog)
  - [Attributions](#attributions)

## Conventions

Please find naming conventions for this project linked here: [click](/docs/documentation/conventions.md). In addition, static type annotations are used in this project. The code is formatted and linted in VS Code using the Black Formatter Extension and Pylint.

## Testing

The codebase has been tested using the `pytest` module. The recent CI/CD status can be found below. Click [here](https://github.com/nicolashuberIT/flight-analyzer/actions) for a detailed overview and unit testing logs. 

![Testing](https://github.com/nicolashuberIT/flight-analyzer/actions/workflows/testing.yaml/badge.svg)

*Please note: An issue regarding some tests failing with a FileNotFoundError when running pytest without specifying test files explicitly has been resolved, but the option to run tests using the `testing.sh` script persists; this workaround involves explicitly listing test files with their relative paths in a shell script and executing it to ensure pytest can locate and run the tests without encountering errors. For more details, refer to [testing.sh](/testing.sh), [update_testing.sh](/update_testing.sh), and [testing.yaml](https://github.com/nicolashuberIT/flight-analyzer/blob/main/.github/workflows/testing.yaml).*

## Contributing

At this time, the `flight-analyzer` project is not open for community contributions. The development is currently handled exclusively by Nicolas Huber. Your interest is appreciated and this section will be updated if the policy changes in the future.

## Changelog

- **[1.0.0]** - `flight-analyzer` published as of 03/31/2024 as part of Nicolas Huber's contribution the the "Schweizer Jugend forscht 2024" initiative

## Attributions

I would like to give credit and express my gratitude to the following individuals and organizations for their contributions:

- **[OverlaudUT](https://github.com/OverloadUT/IGC2CSV)**: Author of [IGC2CSV](https://github.com/nicolashuberIT/IGC2CSV), which was forked and extended by Nicolas Huber
- **Daniela Arslan**: Photographer of the cover image in `README.md`

---

_© 2024, [Nicolas Huber](https://nicolas-huber.ch). All rights reserved._
