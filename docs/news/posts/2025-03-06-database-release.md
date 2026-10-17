---
title: Database release
date: 2025-03-06
categories:
- Database
- Release
slug: 2025-03-06-database-release
---

In this release, we have normalized `therapy_name` values to [NCI thesaurus](https://evsexplore.semantics.cancer.gov/evsexplore/welcome) ([#40](https://github.com/vanallenlab/moalmanac-db/pull/40)) and merged an initial version of the next version of our database ([#36](https://github.com/vanallenlab/moalmanac-db/pull/36)), that aims to follow with [GA4GH's Genomic Knowledge Standards](https://www.ga4gh.org/work_stream/genomic-knowledge-standards/) for the database schema ([Read more here](https://github.com/vanallenlab/moalmanac-db/blob/main/docs/referenced-schema-draft-about.md)).

<!-- more -->

[View on GitHub](https://github.com/vanallenlab/moalmanac-db/releases/tag/v.2025-03-06)

Revised entries:

- 31 `therapy_name` values were revised to align with the [NCI thesaurus](https://evsexplore.semantics.cancer.gov/evsexplore/welcome) preferred names, resulting in 106 database records being updated. For more details, see [the relevant pull request](https://github.com/vanallenlab/moalmanac-db/pull/40).

| old `therapy_name` | new `therapy_name` | NCIt code |
|---|---|---|
| 5-Fluorouracil | Fluorouracil | C505 |
| AT7519 | CDK Inhibitor AT7519 | C64761 |
| AZ4547 | Fexagratinib | C88272 |
| AZD3759 | Zorifertinib | C118289 |
| AZD8186 | PI3Kbeta Inhibitor AZD8186 | C107684 |
| Ado-Trastuzumab Emtansine | Trastuzumab Emtansine | C82492 |
| Alkylating chemotherapy | Antineoplastic Alkylating Agent | C1590 |
| Amivantamab-vmjw | Amivantamab | C124993 |
| BAY 1895344 | Elimusertib | C146807 |
| Carbogen and nicotinamide  | Carbogen | C1038 |
| Dostarlimab-gxly | Dostarlimab | C126799 |
| EGF816 | Nazartinib | C115109 |
| Interferon-alpha | Interferon Alpha | C20494 |
| LOXO-292 | Selpercatinib | C134987 |
| MK-2206 | Akt Inhibitor MK2206 | C90581 |
| Margetuximab-cmkb | Margetuximab | C91733 |
| Neoadjuvant chemoradiation | Chemoradiotherapy | C94626 |
| Neoadjuvant chemotherapy | Chemotherapy | C15632 |
| Oxaplatin | Oxaliplatin | C1181 |
| PF-06747775 | Mavelertinib | C120307 |
| PU-H71 | Zelavespib | C101227 |
| Platinum | Platinum Compound | C1450 |
| Proton-based SBRT | Proton Stereotactic Body Radiation Therapy | C175032 |
| Radiation therapy | Radiation Therapy | C15313 |
| Radical radiotherapy | Radiation Therapy | C15313 |
| Rapamycin | Sirolimus | C1212 |
| SBRT | Stereotactic Body Radiation Therapy | C118286 |
| VX-680 | Tozasertib Lactate | C61319 |
| Zenocutuzumab-zbco | Zenocutuzumab | C152948 |
| radiotherapy | Radiation Therapy | C15313 |
| surgery | Surgery | C17173 |
