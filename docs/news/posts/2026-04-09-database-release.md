---
title: Database release
date: 2026-04-09
categories:
- Database
- Release
slug: 2026-04-09-database-release
---

This release contains updates to the draft version of the database. _EGFR_ TKD activating variants was introduced as a biomarker and associated with regulatory approvals from the European Medicines Agency (EMA) and Health Canada (HC). No additional genomic knowledge statements were added with this release, though several were modified.

<!-- more -->

[View on GitHub](https://github.com/vanallenlab/moalmanac-db/releases/tag/v.2026-04-09)

## Database content updates

Added entries:

- (EMA, HC) _EGFR_ TKD activating variants and response to gefitinib for patients with non-small cell lung cancer.

Revised entries:

- (FDA) A description was previously not written for Statements associated with Indication ind:fda.kadcyla:0.
- (FDA) The text for ind:fda.augtyro:1 was revised to resolve typos.
- (HSE) The URLs were updated for all documents originating from Ireland's Health Service Executive (HSE) to reflect their new website.
- (HSE) `ids` associated with treatment regimen "P0567" from the HSE were updated to be "P00567".
- Biomarker names for _EGFR_, _ERBB2_, and _ESR1_ oncogenic variants were renamed to "activating variants" to align with the scope of the associated regulatory approvals.

## New features

- Badges in the moalmanac-db README are now hard coded and do not rely on an API request to render.
