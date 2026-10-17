---
title: Algorithm release 0.8.5
date: 2025-10-24
categories:
- Algorithm
- Release
slug: 2025-10-24-algorithm-release
---

This release utilizes the [v.2025-02-07](https://github.com/vanallenlab/moalmanac-db/releases) version of the MOAlmanac database. Cancer Gene Census is also no longer required to run moalmanac. The interpreter version was increased to 0.8.5.

<!-- more -->

[View on GitHub](https://github.com/vanallenlab/moalmanac/releases/tag/0.8.5)

The repository history was also cleaned to remove COSMIC and Cancer Gene Census datasources. Users may need to refresh repository history by either recloning the repository or getting the current history. The following code should work instead of pulling the latest main branch, though we recommend creating a back up first.

```
git fetch --all --prune --prune-tags
git checkout main
git reset --hard origin/main
```

Additions:

- `datasources/cancergenecensus/cancer_gene_census_empty.genes.tsv` is now the default annotation source for the CGC. It is an empty file with our expected headers. To include CGC as part of the annotation process, users must download and manually generate their own version for use. Instructions for how to do this are located at `datasources/cancergenecensus/README.md`.

Revisions:

- `datasources/cosmic/CosmicMutantExport_empty.lite.txt` is now the default annotation datasource for COSMIC as specified within `moalmanac/annotation-datasources.ini`. Users can still compile COSMIC on their own using the script in `datasources/cosmic/` to re-enable COSMIC annotations.
- `datasources/exac/exac.expanded.r1.empty.txt` is set as the default annotation datasource for ExAC on GitHub, and this is changed to the compiled version `datasources/exac/exac.expanded.r1.txt` when the docker is building.
- Documentation was updated to reflect these changes.
- Applied Python Software Foundation's black formatting to the repository
- Removed COSMIC and Cancer Gene Census datasources from the repository history
