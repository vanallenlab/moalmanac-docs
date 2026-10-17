---
title: Algorithm release 0.8.4
date: 2025-10-17
categories:
- Algorithm
- Release
slug: 2025-10-17-algorithm-release
---

This release utilizes the [v.2025-02-07](https://github.com/vanallenlab/moalmanac-db/releases) version of the MOAlmanac database. Both COSMIC and ExAC are now no longer required to run moalmanac. The interpreter version was increased to 0.8.4.

<!-- more -->

[View on GitHub](https://github.com/vanallenlab/moalmanac/releases/tag/0.8.4)

Revisions:

- A file `datasources/cosmic/CosmicMutantExport_empty.lite.txt` was added. This is an empty file other than the columns expected for COSMIC as a datasource, and is now the default annotation datasource for COSMIC as specified within `moalmanac/annotation-datasources.ini`. Users can still compile COSMIC on their own using the script in `datasources/cosmic/` to re-enable COSMIC annotations.
- A file `datasources/exac/exac.expanded.r1.empty.txt` was added. This is an empty file other than the columns expected for ExAC as a datasource. This was **not** set to be the default annotation datasource for ExAC. Users can change `moalmanac/annotation-datasources.ini` to point to this file if they do not want to annotate with ExAC. Alternatively, they can either generate the datasource using the script in `datasources/exac/` or copy the datasource from the Docker to annotate with ExAC.
- Documentation was updated to reflect these changes.
