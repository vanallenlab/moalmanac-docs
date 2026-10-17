---
title: Algorithm release 0.8.0
date: 2024-12-10
categories:
- Algorithm
- Release
slug: 2024-12-10-algorithm-release
---

This release utilizes the [v.2024-12-05 version of the underlying database](https://github.com/vanallenlab/moalmanac-db/releases/tag/v.2024-12-05) and contains changes from several pull requests: [#27](https://github.com/vanallenlab/moalmanac/pull/27), [#28](https://github.com/vanallenlab/moalmanac/pull/28), [#29](https://github.com/vanallenlab/moalmanac/pull/29), [#30](https://github.com/vanallenlab/moalmanac/pull/30), [#31](https://github.com/vanallenlab/moalmanac/pull/31).

<!-- more -->

[View on GitHub](https://github.com/vanallenlab/moalmanac/releases/tag/0.8.0)

Additions:

- A new output of the suffix .input-metadata.txt. This converts the patients dictionary, which contains input details such as string label, tumor purity, ploidy, and msi status, into a dataframe and outputs it as a table. From [#30](https://github.com/vanallenlab/moalmanac/pull/30) .
- A new output of the suffix .moalmanac-execution.json. This compiles all config settings set in config.ini, execution runtime, input file paths, input datasource paths, input metadata, as well as each tabular output into a single json file. From [#30](https://github.com/vanallenlab/moalmanac/pull/30) .
- A new script `moalmanac/run_4x_for_output_regression_test.py` to run the `moalmanac/run_example.py` four times using different config settings and with and without input files. From [#29](https://github.com/vanallenlab/moalmanac/pull/29).

Revisions:

- `moalmanac/logger.py` was revised to shut down at the end of moalmanac's main function, allowing for multiple processes to be executed in series within a single Python process. From [#29](https://github.com/vanallenlab/moalmanac/pull/29).
- Annotating with ExAC, ExACExtended, and ClinVar will now skip rows that have missing data in any of the required columns. From [#28](https://github.com/vanallenlab/moalmanac/pull/28).
- Docker now uses Python 3.12 and also pushes to the `latest` tag. From [#27](https://github.com/vanallenlab/moalmanac/pull/27).

Bug fixes:

- Columns with empty values within read count columns would cause the process to fail. From [#28](https://github.com/vanallenlab/moalmanac/pull/28).
