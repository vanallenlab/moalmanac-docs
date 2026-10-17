---
title: Database release
date: 2026-02-05
categories:
- Database
- Release
slug: 2026-02-05-database-release
---

This release contains updates to the draft version of the database with FDA precision oncology approvals for Akeega. Additionally, the Organizations table was merged into the Agents table.

<!-- more -->

[View on GitHub](https://github.com/vanallenlab/moalmanac-db/releases/tag/v.2026-02-05)

## Database content updates

Added entries:

- (FDA) BRCA2 oncogenic and pathogenic variants and sensitivity to niraparib and abiraterone acetate in combination with prednisone for the treatment of patients with metastatic castration-sensitive prostate cancer.

Revised entries:

- (FDA) BRCA1/2 oncogenic and pathogenic variants and sensitivity to niraparib and abiraterone acetate in combination with prednisone for the treatment of patients with metastatic castration-resistant prostate cancer was incorrectly listed as initially published in 2018 instead of 2023.

## New features

- The `description` written for each statement associated with an indication from the indications table will now populate the `description` field when dereferencing the database.
- The Agents and Organizations table were merged to align with VA-Spec.
