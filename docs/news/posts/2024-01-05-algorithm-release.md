---
title: Algorithm release 0.5.0
date: 2024-01-05
categories:
- Algorithm
- Release
slug: 2024-01-05-algorithm-release
---

This release utilizes the [v.2023-11-09](https://github.com/vanallenlab/moalmanac-db/releases/tag/v.2023-11-09) release of the underlying MOAlmanac database and incorporates changes from three pull requests: [#15: Added AIP to hereditary cancers gene list](https://github.com/vanallenlab/moalmanac/pull/15), [#16: Update db nov 2023](https://github.com/vanallenlab/moalmanac/pull/16), and [#17: Revise handling of COSMIC mutational signatures](https://github.com/vanallenlab/moalmanac/pull/17).

<!-- more -->

[View on GitHub](https://github.com/vanallenlab/moalmanac/releases/tag/0.5.0)

Additions:

- Added _AIP_ to genes related to hereditary cancers gene list.
- All entries within the MOAlmanac database now have filled fields for `publication_date` of the source and when the record was `last_updated`.
- `moalmanac/moalmanac.py` now accepts `--mutational_signatures` as an input argument and an example input as been added.  

Revisions:

- MOAlmanac no longer runs deconstructSigs as a subprocess and, as a result, R dependencies have been removed.
- The annotation to the MOAlmanac database was updated to sort by the evidence type, publication date of the source, and then when the database record was last updated.
