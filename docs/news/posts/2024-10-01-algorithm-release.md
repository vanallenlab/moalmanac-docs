---
title: Algorithm release 0.7.1
date: 2024-10-01
categories:
- Algorithm
- Release
slug: 2024-10-01-algorithm-release
---

This release utilizes the [v.2024-04-11](https://github.com/vanallenlab/moalmanac-db/releases) release of the underlying MOAlmanac database and primarily focuses on adding logging to MOAlmanac and refactoring the codebase to remove the `datasources/` directory from the application folder. It incorporates changes from two pull requests: <https://github.com/vanallenlab/moalmanac/pull/21> and <https://github.com/vanallenlab/moalmanac/pull/22>.

<!-- more -->

[View on GitHub](https://github.com/vanallenlab/moalmanac/releases/tag/0.7.1)

Additions:

- A new output with the suffix `.log` is generated which details inputs provided, configuration settings, output locations, and MOAlmanac processes as they happen. This is detailed in [pull request 22](https://github.com/vanallenlab/moalmanac/pull/22).
- Two new configuration files: `annotation-databases.ini` and `preclinical-databases.ini` have been added to the application folder to detail datasource locations for both required datasources and datasources for the cancer cell line modules, respectively. These sections have been removed from `config.ini`. `annotation-databases.ini` and `config.ini` are now required arguments of `moalmanac/moalmanac.py` and `preclinical-databases.ini` is an optional argument.

Revisions:

- The datasources folder, `moalmanac/datasources/`, was moved to the root directory of this repository.
- Input, output, and runtime README files have been updated to reflect the changes of these two pull requests.
- `run_example.py` was revised to add the date in ISO format to the default output directory
- Several unit tests were updated to accommodate the datasources location and aforementioned changes to configuration files.
- The files `moalmanac/run_deconstructSigs.R` and `moalmanac/wrapper_deconstructSigs.sh` have been removed from the repository.
