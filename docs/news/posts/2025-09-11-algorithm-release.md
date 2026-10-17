---
title: Algorithm release 0.8.3
date: 2025-09-11
categories:
- Algorithm
- Release
slug: 2025-09-11-algorithm-release
---

This release utilizes the [v.2025-02-07](https://github.com/vanallenlab/moalmanac-db/releases) version of the MOAlmanac database. It includes a fix to a bug that prevented HTML report generation. Specifically, in rare circumstances, the columns `sensitive_score_bin_map`, `resistance_score_bin_map`, and `prognostic_score_bin_map` were not added to the data object for actionable variants, which are used to sort report tables.

<!-- more -->

[View on GitHub](https://github.com/vanallenlab/moalmanac/releases/tag/0.8.3)

Revisions:

- Changes were made to `evaluator.py`, `illustrator.py`, and `writer.py` to resolve occasionally occurring warnings regarding upcoming changes on interacting with a copy of a slice from a DataFrame and downcasting object dtype arrays.

Bug fixes:

- Explicitly define `sensitive_score_bin_map`, `resistance_score_bin_map`, or `prognostic_score_bin_map` within the `bin_names` section of `colnames.ini`.
