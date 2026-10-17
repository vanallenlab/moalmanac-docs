---
title: Algorithm release 0.4.5
date: 2023-03-10
categories:
- Algorithm
- Release
slug: 2023-03-10-algorithm-release
---

This release utilizes the [v.2023-02-02](https://github.com/vanallenlab/moalmanac-db/releases) release of the underlying MOAlmanac database. It incorporates changes from three pull requests: [changing the underlying MOAlmanac database from TinyDB to JSON (#9)](https://github.com/vanallenlab/moalmanac/pull/9), [adding a simplified input option to run MOAlmanac (#10)](https://github.com/vanallenlab/moalmanac/pull/10), and [updating datasources (#11)](https://github.com/vanallenlab/moalmanac/pull/11).

<!-- more -->

[View on GitHub](https://github.com/vanallenlab/moalmanac/releases/tag/0.4.5)

Additions:

- A section called function_toggle has been added to `moalmanac/config.ini` to enable or disable several features of moalmanac, see [here](https://github.com/vanallenlab/moalmanac/pull/9) for more details.
- The script `moalmanac/simplified_input.py` has been added to allow users to input a tab delimited file of somatic variants, germline variants, copy number alterations, and rearrangements. Supporting functions have been added to `moalmanac/annotator.py` and `moalmanac/features.py` and example input data has been added to `example_data/` to support this change. See [here](https://github.com/vanallenlab/moalmanac/pull/10) for more details.

Revisions:

- The underlying moalmanac database is held in memory using the json python library, rather than TinyDB. See [here](https://github.com/vanallenlab/moalmanac/pull/9) for more details.
- `moalmanac/reporter.py` has been refactored to produce the report based on an object.
- Flask has been upgraded to 2.0.0 in requirements.txt.
- Documentation has been updated for description of inputs, example outputs, and method usage.
- Datasources COSMIC and Cancer Gene Census have been updated to version 97, ACMG secondary findings has been updated to version 3, and OncoTree has been updated.

Bug fixes:

- Warnings are no longer produced when generating the actionability report.
- Drugs not present in `almanac-gdsc-mappings.json` no longer cause errors with execution.
- The output folder is now properly handled by the R subprocesses.
- Therapies that have not been matched to preclinical drugs produced an error. moalmanac/investigator.py has been revised to only consider therapies that have already been mapped. This was identified in <https://github.com/vanallenlab/moalmanac/issues/11>.
