---
title: Algorithm release 0.6.0
date: 2024-05-31
categories:
- Algorithm
- Release
slug: 2024-05-31-algorithm-release
---

This release utilizes the [v.2024-04-11](https://github.com/vanallenlab/moalmanac-db/releases) release of the underlying MOAlmanac database and primarily focuses on supporting Python 3.12. It incorporates changes from two pull requests: <https://github.com/vanallenlab/moalmanac/pull/18> and <https://github.com/vanallenlab/moalmanac/pull/19>.

<!-- more -->

[View on GitHub](https://github.com/vanallenlab/moalmanac/releases/tag/0.6.0)

Additions:

- A new output regression test to hash and compare output text files from two folders, `run_output_regression_test.py`. This test is intended to be run on outputs generated from the `main` branch and a branch intending to be merged.
- The minimum coverage value is now taken for ONP variants when multiple coverage values are provided on a single row. This change was made to comply with pandas' [change in behavior of object type downcasting](https://pandas.pydata.org/docs/whatsnew/v2.2.0.html).

Revisions:

- All dependencies in `requirements.txt` have been updated to their latest versions, and also alphabetized.
- `moalmanac/datasources/moalmanac/create_almanac_db.py` was revised to (i) take the config.ini file as an input argument and (ii) skip a record if the `_deprecated` field is set to `False`.

Bug fixes:

- `investigator.py`'s `populate_feature_dictionary` function will no longer will include samples with an NA sample name. Some samples have an NA for sample name because not all samples have an alias across all three naming conventions: Broad Institute, CCLE, and Sanger labels.
