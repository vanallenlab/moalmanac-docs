---
title: Database release
date: 2025-02-07
categories:
- Database
- Release
slug: 2025-02-07-database-release
---

Added entries:

<!-- more -->

[View on GitHub](https://github.com/vanallenlab/moalmanac-db/releases/tag/v.2025-02-07)

- (FDA) [_ALK_ rearrangements and sensitivity to ensartinib for the treatment of adult patients with non-small cell lung cancer](https://www.fda.gov/drugs/resources-information-approved-drugs/fda-approves-ensartinib-alk-positive-locally-advanced-or-metastatic-non-small-cell-lung-cancer).
- (FDA) [_BRAF_ p.V600E and sensitivity to encorafenib in combination with cetuximab and mFOLFOX6 for the treatment of patients with colorectal cancer](https://www.fda.gov/drugs/resources-information-approved-drugs/fda-grants-accelerated-approval-encorafenib-cetuximab-and-mfolfox6-metastatic-colorectal-cancer-braf).
- (FDA) [_KRAS_ p.G12C and sensitivity to panitumumab in combination with sotorasib for the treatment of adult patients with metastatic colorectal cancer](https://www.fda.gov/drugs/resources-information-approved-drugs/fda-approves-sotorasib-panitumumab-kras-g12c-mutated-colorectal-cancer).

Additionally, all records in the database now contain three additional keys: `assertion_id`, `feature_id`, and `source_id`, as they appear in the [https://www.moalmanac.org/api/assertions](https://www.moalmanac.org/api/assertions) endpoint. The assertion_id and feature_id values are simply the index value for each record in the database.

The [https://www.moalmanac.org/api/features](https://www.moalmanac.org/api/features) endpoint lists the unique features when _not_ considering the `feature_id` key, and thus it returns a list of dictionaries containing the first instance of each genomic feature. This will be added at a later date to each record in `molecular-oncology-almanac.json` under the key `features_endpoint_feature_id`.
