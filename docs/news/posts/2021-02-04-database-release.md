---
title: Database release
date: 2021-02-04
categories:
- Database
- Release
slug: 2021-02-04-database-release
---

In addition to the content changes listed below, this release added a therapeutic strategy (`therapy_strategy`) for all sensitive and resistance relationships.

<!-- more -->

[View on GitHub](https://github.com/vanallenlab/moalmanac-db/releases/tag/v.2021-02-04)

Added entries:

- (FDA) _EGFR_ p.L858R and sensitivity to osimertinib in non-small cell lung cancer.
- (FDA) _EGFR_ exon 19 deletions and sensitivity to osimertinib in non-small cell lung cancer.
- (FDA) HER2-positive breast cancer and sensitivity to margetuximab-cmkb + chemotherapy.

Edited entries:

- (Guideline) _ABL1_ p.T315I suggesting sensitivity to Omacetaxine in CML has been recategorized from a targeted therapy to chemotherapy.
- (Guideline) MSI-High associated with resistance to 5-Fluorouracil in colorectal adenocarcinoma. 5-Fluorouracil was reclassified as a chemotherapy therapy type instead of targeted therapy.
- (Guideline) _TET2_ somatic variants suggesting sensitivity to azacitidine was changed from a targeted therapy to chemotherapy.
- (Clinical evidence) _PAK1_ amplifications associated with poor prognosis in breast cancer. Removed Tamoxifen from this association as it is not asserting therapeutic sensitivity or resistance.
- (Preclinical) _KRAS_ somatic variants associated with sensitivity to trametinib + fgfr1 inhibition. Recorded therapy name to be alphabetical and changed inhibitor to be lowercase.
- (Preclinical) _RUNX1_--_RUNX1T1_ fusions and sensitivity to azacitidine + panobinostat has been reclassified as a combination therapy from targeted therapy.

Mutational signature version has been added as a feature definition for mutational signatures. All catalogued assertions of this feature type are currently using Mutational Signatures (v2).

Several assertions from clinical guideline sources for multiple myeloma and myelodysplasia were incorrectly reported as clinical evidence. These have been updated to be guidelines.
