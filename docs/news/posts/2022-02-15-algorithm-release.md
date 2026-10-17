---
title: Algorithm release 0.4.2
date: 2022-02-15
categories:
- Algorithm
- Release
slug: 2022-02-15-algorithm-release
---

This release utilizes the [v.2021-02-04](https://github.com/vanallenlab/moalmanac-db/releases/tag/v.2021-02-04) release of the underlying MOAlmanac database.

<!-- more -->

[View on GitHub](https://github.com/vanallenlab/moalmanac/releases/tag/0.4.2)

Revisions:

- Added a README to the `moalmanac/datasources/` folder, specifying which datasources are available for use immediately from Github and which ones either need to be copied from Docker or processed from source.
- Added Oncotree code as an output columns for assertions in the `.actionable.txt` output.
- Revised documentation for COSMIC, `moalmanac/datasources/cosmic/`, and ExAC, `moalmanac/datasources/exac/`, by expanding upon how to generate the datasources from source.
- Revised documentation for preclinical data leveraged by MOAlmanac. Previously, `moalmanac/datasources/preclinical/` contained output tables from the [paper's repository](https://github.com/vanallenlab/moalmanac-paper) and referenced the repository for documentation. Now, all utilized tables can be generated within this repository from source.
- Revised README in the root directory to emphasis that not all datasources are immediately ready for use after pulling this repository from Github.
- Updated Dockerfile to compile moalmanac and preclinical datasources later, to hopefully reduce build time.
- Updated WDL to use the latest version of this method, increased default resource requirements for buffer, and preallocated additional matches json output.

Bug fixes:

- Annotation with ExAC now coerces integer columns from strings to floats and then integers, making the annotator resilient to some MAFs which have positions coded as floats instead of integers.
