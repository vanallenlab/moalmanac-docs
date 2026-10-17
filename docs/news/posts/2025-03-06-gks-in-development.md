---
title: Re-developing our schema to align with GA4GH standards
date: 2025-03-06
categories:
- Announcement
- Database
slug: 2025-03-06-gks-in-development
---

We are in the process of refactoring and updating moalmanac db to align with [GA4GH's Variant Annotation Specification (va-spec)](https://github.com/ga4gh/va-spec) and [Categorical Variant Representation Specification (Cat-VRS)](https://github.com/ga4gh/cat-vrs). Both of these specifications are in development and are following the [GA4GH Genomic Knowledge Standards (GKS) Maturity Model](https://cat-vrs.readthedocs.io/en/latest/appendices/maturity_model.html). As components of each specification moves from draft to trial and to normative maturity we will update our schema to align with their recommendations. This version of the database is under active development and, if you have any thoughts, comments, concerns, or suggestions, please [contact us](https://dev.moalmanac.org/about#contact)!

<!-- more -->

# Why are we making this change?

Most importantly, we are making this change because our current schema is something that we "just made up" throughout our original development. There is now an increasing emphasis within the field on interoperability and data standards, and we want moalmanac to both communicate with other services as well as possible while providing the most value to our users. Representing our database content within a widely used specification will increase the utility of our service.

Pragmatically, there is also technical debt associated with the current format. While we use [a flat JSON schema](https://github.com/vanallenlab/moalmanac-db/blob/main/docs/sop.md), this is converted into a SQLite table for use with the [moalmanac-browser](https://github.com/vanallenlab/moalmanac-browser/tree/master/db_versions). The representation of genomic information is particularly troublesome within this format, with nested tables to store attribute definitions and attributes of each biomarker type. Code to generate the browser's sqlite table easily results in ids of assertions, sources, or features changing between the database content releases. Over the years this has caused some hiccups with adoption by some users. To complicate matters further, we store database metadata in the version of the database [used by the algorithm](https://github.com/vanallenlab/moalmanac/tree/main/datasources/moalmanac) and as a result there are three slightly different versions of our database published: our database repository, the one used by our browser and accessible through the API, and by the algorithm. We would like to simplify this. It has also made expanding our API endpoints difficult.

About a year ago in January 2024, we began curating knowledge for European precision oncology approvals (more on this soon!) in the format used by [GA4GH's genomic knowledge pilot](https://gk-pilot.readthedocs.io/en/stable/index.html). Afterwards, we went back and re-curated FDA approvals from scratch, additionally curating indications involving biomarkers that are of type protein expression, wild type, mismatch repair, and homologous recombination.

# Using a relational schema

We are using a relational schema that can be dereferenced to a single JSON file using [utils/dereference.py](https://github.com/vanallenlab/moalmanac-db/tree/main/utils#dereferencepy). The genomic knowledge pilot separated datasources into referenced and dereferenced sources, and so we are following their recommendations for this. We can thus have each element of the specification in its own referenced json file and these contents can be mirrored into the SQLite database that will be used by the API, or other database type chosen. There are two other additional benefits that we've noticed: testing the database content is much easier because each element can be independently evaluated and curation is _much_ faster by being able to reference the appropriate record within a data type, instead of typing or copying data. In short using a relational schema better follows [Don't repeat yourself (DRY)](https://en.wikipedia.org/wiki/Don%27t_repeat_yourself) principles.

# Our in progress interpretation of VA-Spec

VA-Spec supports a wide array of [proposition types](https://va-ga4gh.readthedocs.io/en/latest/base-profiles/statement-profiles.html) but at the moment we are only utilizing Variant Therapeutic Response Study Proposition. Our current draft schema does _not_ follow va-spec and we are continuing to work to align our specification to their framework.

More on this update to come!

We also want to give a special thank you to Daniel Puthawala and Kori Kuzama from the Wagner lab for their help and patience as we've badgered them with questions to understand the GKS ecosystem. Their expertise and the [Wagner Lab's normalizers](https://gk-pilot.readthedocs.io/en/stable/tools.html) are excellent.
