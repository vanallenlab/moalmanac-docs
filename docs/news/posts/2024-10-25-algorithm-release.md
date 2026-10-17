---
title: Algorithm release 0.7.2
date: 2024-10-25
categories:
- Algorithm
- Release
slug: 2024-10-25-algorithm-release
---

This release utilizes the [v.2024-10-03](https://github.com/vanallenlab/moalmanac-db/releases) release of the underlying [MOAlmanac database](https://moalmanac.org/) and otherwise fixes two bugs present in Release 0.7.1. This release incorporates pull requests <https://github.com/vanallenlab/moalmanac/pull/23> and <https://github.com/vanallenlab/moalmanac/pull/24>.

<!-- more -->

[View on GitHub](https://github.com/vanallenlab/moalmanac/releases/tag/0.7.2)

Additions:

- An example log output was added to the example_output/ folder in the root directory of this repository.

Revisions:

- `datasources/moalmanac/molecular-oncology-almanac.json` was updated to the 2024-10-03 release.
- `docs/template-pull-request.md` was renamed to `docs/pull_request_template.md`
- The section heads for both `moalmanac/annotation-databases.ini` and `moalmanac/preclinical-databases.ini` were renamed to paths.

Bug fixes:

- `moalmanac/moalmanac.py` would attempt to access the value "preclinical" in the preclinical_db_paths dictionary, even if no .ini file was provided using the --preclinical-dbs argument.
- Templates to generate tables within the Frozen Flask report were modified to include an if statement to only generate tables if the underlying dataframe is not empty.
