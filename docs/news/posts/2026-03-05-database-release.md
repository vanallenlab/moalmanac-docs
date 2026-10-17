---
title: Database release
date: 2026-03-05
categories:
- Database
- Release
slug: 2026-03-05-database-release
---

This release contains updates to the draft version of the database with FDA precision oncology approvals from February 2026. Specifically, indications and derived relationships were updated for Braftovi (encorafenib), Hernexeos (zongertinib), and Keytruda (pembrolizumab).

<!-- more -->

[View on GitHub](https://github.com/vanallenlab/moalmanac-db/releases/tag/v.2026-03-05)

## Database content updates

Added entries:

- (FDA) _BRAF_ p.V600E and sensitivity to encorafenib in combination with cetuximab and FOLFIRI for patients with metastatic colorectal cancer.
- (FDA) PD-L1 (CPS >= 1) and sensitivity to pembrolizumab in combination with paclitaxel, with or without bevacizumab, for patients with epithelial ovarian, fallopian tube, or primary peritoneal carcinoma.

Revised entries:

- (FDA) _BRAF_ p.V600E and sensitivity to encorafenib in combination with cetuximab and mFOLFOX6 for patients with metastatic colorectal cancer received regular approval.
- (FDA) _ERBB2_ activating variants and sensitivity to zongertinib in patients with non-squamous non-small cell lung cancer was revised to expand treatment eligibility by removing the prior therapy restriction.

Removed entries:

- (EMA, HSE) _FGFR2_::_BICC1_ and _FGFR2_::_CASP7_ and sensitivity to erdafitinib in patients with bladder urothelial carcinoma.

## New features

- The Documents table was merged to align with VA-Spec.
- URLs associated with documents have been moved to their own table in the referenced/ folder
