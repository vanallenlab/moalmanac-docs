# Overview

The Molecular Oncology Almanac (MOAlmanac) is a clinical and biological interpretation algorithm and paired knowledge base for precision oncology. The primary objective of MOAlmanac is to identify and associate molecular alterations with therapeutic sensitivity and resistance as well as disease prognosis. This is done for “first-order” genomic alterations -- individual events such as somatic variants, copy number alterations, fusions, and germline -- as well as “second-order” events -- those that are not associated with one single mutation, and may be descriptive of global processes in the tumor such as tumor mutational burden, microsatellite instability, mutational signatures, and whole-genome doubling.

The underlying database of this method is dependent on expert curation of the current body of knowledge on how molecular alterations affect clinical actionability. As the field of precision oncology grows, the quantity of research on how specific alterations affect therapeutic response and patient prognosis expands at an increasing rate. Curating the latest literature and presenting it in an accessible manner increases the abilities of clinicians and researchers alike to rapidly assess the importance of a molecular feature.

The database has been refactored to align with representation standards developed by the [Global Alliance for Genomics & Health](https://www.ga4gh.org) [Genomic Knowledge Standards Work Stream](https://www.ga4gh.org/work_stream/genomic-knowledge-standards/). You can access our our version of the database and browser at [https://old.moalmanac.org](https://old.moalmanac.org), **which will be deprecated on March 31st, 2027**.

## Molecular Oncology Almanac resources

- [Molecular Oncology Almanac Algorithm](../algorithm/index.md) - clinical interpretation of individual patient samples ([GitHub](https://github.com/vanallenlab/moalmanac)).
- [Molecular Oncology Almanac API](https://api.moalmanac.org) - programmatic access to the knowledge base ([GitHub](https://github.com/vanallenlab/moalmanac-api)).
- [Molecular Oncology Almanac Browser](https://moalmanac.org) - browse the underlying knowledge base ([GitHub](https://github.com/vanallenlab/moalmanac-browser)).
- Molecular Oncology Almanac Database - the knowledge base content and release notes ([GitHub](https://github.com/vanallenlab/moalmanac-db)).
- All related GitHub repositories can be accessed through the ["molecular-oncology-almanac" GitHub Topic](https://github.com/topics/molecular-oncology-almanac).

!!! note

    We have not yet adapted the [interpretation algorithm](https://github.com/vanallenlab/moalmanac) to this new schema.

## Region-specific instances

Region-specific instances of the Molecular Oncology Almanac are developed with local collaborators and include regulatory and/or health system access content for their region.

### Canada

[https://ca.moalmanac.org](https://ca.moalmanac.org)

This instance contains marketing authorization approvals from [Health Canada](https://www.canada.ca/en.html). We note that Health Canada's content is [**not approved for commercial use**](https://www.canada.ca/en/transparency/terms.html#:~:text=Ownership%20and%20usage,relevant%20page(s).).

### Ireland

[https://ie.moalmanac.org](https://ie.moalmanac.org)

This instance of the Molecular Oncology Almanac was developed with the [Culhane lab](https://www.ul.ie/ehs/medicine/prof-aedin-culhane) at the [University of Limerick](https://www.ul.ie) in collaboration with the [Health Service Executive's National Cancer Control Programme](https://www.hse.ie/eng/services/list/5/cancer/). It contains marketing authorization approvals from the [European Commission](https://www.ema.europa.eu/en/homepage) and [Health Products Regulatory Agency](https://www.hpra.ie), as well as approvals for reimbursement within the public health system from the [Health Service Executive](https://www.hse.ie).

## Citation

If you use the Molecular Oncology Almanac, please cite our publication. See [Citation](citation.md) for the reference and for citing a specific database release.

## Data access

The contents of this knowledge base can be downloaded through [the database's GitHub releases](https://github.com/vanallenlab/moalmanac-db/releases) or the [API](https://api.moalmanac.org), particularly the [statements endpoint](https://api.moalmanac.org/#/Entities/get_statements_statements_get).
