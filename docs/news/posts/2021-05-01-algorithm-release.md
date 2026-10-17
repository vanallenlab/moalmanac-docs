---
title: Algorithm release 0.4.1
date: 2021-05-01
categories:
- Algorithm
- Release
slug: 2021-05-01-algorithm-release
---

This release utilizes the [v.2021-02-04](https://github.com/vanallenlab/moalmanac-db/releases/tag/v.2021-02-04) release of the underlying MOAlmanac database.

<!-- more -->

[View on GitHub](https://github.com/vanallenlab/moalmanac/releases/tag/0.4.1)

New features:

- Pass called copy number alterations rather than segmentation files with the `--called_cna` input argument.
- A new output lists all therapeutic strategies highlighted by MOAlmanac and associated therapies, categorized by if the therapy was highlighted for sensitivity or resistance relationships. This is reported in the output of the suffix `.therapeutic_strategies.txt`.
- Added the `docs/` folder, which includes detailed descriptions of inputs and outputs.

Revisions:

- Updated WDL to use the latest version of this method.
- Updated READMEs.
- Updated how mutational signatures are displayed, version number of COSMIC signatures are now shown.
- Removed requirement for segment valued copy number alterations to be of at least |1| in value to be reported as Putatively Actionable.
- Reports now show "Prognosis and rationale" for assertions related to prognosis.
- Updated datasources modal in report.
- Fusion inputs now are appropriate for the latest output of STAR fusion.
- The y-axis for preclinical efficacy figures are now dynamically set based on values plotted rather than a static range.
- The actionability categories "Investigate Actionability - High" and "Investigate Actionability - Low" have been collapsed to a single label, "Investigate Actionability". Molecular features will still sort as before.
- The sort order of dataframes based on datasource match are now explicitly set in the Writer, for if each datasource column should be ascending or descending.
- Added a function to annotate somatic variants without ExAC, which can be imported for custom annotation.
- Updated unit tests to reflect code changes.
- Updated license to GPL 2.0.
- Updated preclinical datasources to reflect the recent revisions to the [paper repository](https://vanallenlab/moalmanac-paper).

Bug fixes:

- Extended ExAC annotations (annotating with subpopulation information) now properly annotates as expected.
- The second gene as part of fusions were not properly being ranked in the somatic output.
