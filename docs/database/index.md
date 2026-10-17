# Database

The MOAlmanac database ([moalmanac-db](https://github.com/vanallenlab/moalmanac-db)) is an expert-curated catalog of how molecular alterations relate to clinical actionability in cancer. Each record states that one or more biomarkers predict a therapeutic response in a disease, and links that claim to the documents that support it, such as regulatory approvals from the FDA and EMA.

The database is being refactored to align with GA4GH's [Variant Annotation Specification (VA-Spec)](https://github.com/ga4gh/va-spec) and [Categorical Variant Representation Specification (Cat-VRS)](https://github.com/ga4gh/cat-vrs). Both specifications are still in development, so the current schema follows them where it can but does not yet comply with either.

## Referenced and dereferenced records

The database is stored as a relational schema: each record type (biomarkers, diseases, documents, statements and so on) has its own file in `referenced/`, and records point to one another by id. This keeps each fact in one place, lets each record type be tested on its own, and makes curation faster, since curators reference an existing record instead of retyping it.

A script in the repository, `utils/dereference.py`, replaces those ids with the records they point to and writes the result to `dereferenced/` and to a single combined JSON file. The dereferenced records are what the [API](../api/index.md) serves.

The [schema reference](schemas/index.md) documents both forms, field by field.

## Getting the data

- Search it in the [browser](https://moalmanac.org) or query it through the [API](../api/index.md).
- Download it from the [repository](https://github.com/vanallenlab/moalmanac-db), or a specific version from its [releases](https://github.com/vanallenlab/moalmanac-db/releases). See [Releases and versioning](../about/releases-and-versioning.md).

## Suggesting an entry

To suggest a relationship for the database, use the browser's [submission form](https://moalmanac.org/add) or open a pull request on [moalmanac-db](https://github.com/vanallenlab/moalmanac-db).
