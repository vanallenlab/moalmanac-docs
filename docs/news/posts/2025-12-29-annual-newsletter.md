---
title: 2025 newsletter
date: 2025-12-29
categories:
- Annual newsletters
slug: 2025-12-29-annual-newsletter
---

Happy holidays from the Molecular Oncology Almanac team! Thank you all for the support throughout the year. This was a _huge_ year for development. Here, we'll share a recap of what we have done and where we are going.

<!-- more -->

## In this newsletter

- Database updates
- Algorithm updates
- Changes to our web presence
- What's next for 2026?

## Database updates

We managed [9 database releases](../category/database/) throughout 2025, increasing the number of records within our underlying database from 1,001 to 1,015 entries. These primarily originate from US Food and Drug Administration (FDA) regulatory approvals.

However, most of our effort this year has been spent on developing a new version of MOAlmanac that [aligns with representation standards from Global Alliance for Genomics & Health (GA4GH)'s Genomic Knowledge Standards work stream](2025-03-06-gks-in-development.md). Doing so will increase interoperability of our database's content, making it easier for additional users to ingest and utilize moalmanac. Utilizing this schema has already provided several benefits, including:

- Associating multiple biomarkers with a single database record, or genomic knowledge statement.
- Decouple combination therapies associated with a single database record. For example, our current schema lists "Adagrasib + Cetuximab" as a single therapy instead of being queryable with either Adagrasib or Cetuximab.
- Provide explicit hyperlinks and mappings to other resources for cataloged concepts. For example, linking to the [OncoTree node for Astrocytoma](https://oncotree.mskcc.org/?version=oncotree_2021_11_02&field=CODE&search=ASTR) when using an OncoTree coding.

As part of this update, we have recurated and rederived statements originating from US FDA approvals, and also curated [additional biomarker types](https://dev.moalmanac.org/biomarkers), including: homologous recombination status, internal tandem duplication, mismatch repair status, protein expression, and wild type relationships. As a result, statements originating from FDA approvals have increased from 285 entries to 674. In addition, we also curated regulatory approvals from several other agencies, including: the European Medicines Agency (EMA, 507 statements currently), the Republic of Ireland's Health Products Regulatory Authority (HPRA, 22) and Health Service Executive (HSE, 349), and Health Canada (HC, 331). From just these organizations, our database currently hosts 1883 genomic knowledge statements.

![Molecular Oncology Almanac database size over 2025](../../assets/news/2025-12-29-newsletter/db-size.svg)

We will migrate our non-regulatory approval evidence in the first couple of months in 2026.

We also began minting [Zenodo DOIs](https://zenodo.org/records/18064228) for our database in September so that specific database versions can be cited.

## Algorithm updates

Our algorithm received [5 GitHub releases this year](../category/algorithm/). Some highlights include: our Docker container now supports multiple operating system architectures, supporting Python 3.13, complying code refactoring to resolve warnings, and minor bug fixes.

## Changes to our web presence

We rebuilt the web browser from scratch this year to support the updated database schema. As part of this refactor, we designed the codebase to launch region-specific instances of the web browser that will only display regulatory approvals from selected organizations. Each can be deployed to their own moalmanac.org subdomain and customized with their own color scheme, of course. There are currently 3 active instances of the database browser:

- [dev.moalmanac.org](https://dev.moalmanac.org), default browser: hosting approvals from the FDA and EMA.
- [ie.moalmanac.org](https://ie.moalmanac.org), instance for the Republic of Ireland: hosting approvals from the FDA, EMA, Health Products Regulatory Authority, and Health Service Executive.
- [ca.moalmanac.org](https://ca.moalmanac.org), instance for Canada: hosting approvals from the FDA and Health Canada.

All instances are backed by our new API, with endpoints viewable at [https://api.moalmanac.org](https://api.moalmanac.org).

![Molecular Oncology Almanac database size over 2025](../../assets/news/2025-12-29-newsletter/web-overview.svg)

We also launched a dedicated news website: [news.moalmanac.org](../index.md). Here, release notes for all software products within the MOAlmanac ecosystem are shared as a one-stop-shop, as well as Announcements. These are also posted on both [Bluesky](https://bsky.app/profile/moalmanac.org) and [LinkedIn](https://www.linkedin.com/company/molecular-oncology-almanac/), the latter of which we joined in the autumn.

Lastly, the web portal to interactively launch Molecular Oncology Almanac on Terra and Google Cloud Platform was decommissioned this autumn due to [Google Cloud deprecating their Life Sciences API](2025-09-03-deprecation.md). We may revisit it at a future date.

## What's next for 2026?

Our focus for Q1 2026 is to continue refining our updated schema to successfully validate against GA4GH representation standards. We will be migrating over our non-regulatory approval database records to this new schema in the first couple of months, too. We hope to **redirect dev.moalmanac.org to moalmanac.org on March 31st, 2026**, and **redirect the current moalmanac.org to old.moalmanac.org** with plans to decommission it at the end of the year. We will add a banner to moalmanac.org linking to this announcement. As part of this, we will update the algorithm to ingest this new version of the database as a holdover until we perform a major release.

In addition, we aim to launch a single documentation website to host all MOAlmanac related documentation, as we have done with [news.moalmanac.org](../index.md).

In the meantime, we hope that you have had a wonderful holiday season! Thank you for reading and follow us on [Bluesky](https://bsky.app/profile/moalmanac.org) and [LinkedIn](https://www.linkedin.com/company/molecular-oncology-almanac/?viewAsMember=true) to receive more updates from us.
