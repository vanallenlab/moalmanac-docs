# Database schemas

Every record type in moalmanac-db is described by a JSON Schema in the repository's `schemas/` folder. The pages in this section are generated from those schemas, so they always match the pinned version of the database.

There are two sets:

- [Referenced schemas](referenced/index.md) describe records as stored in `referenced/`, where foreign keys are ids that point to records in other tables.
- [Dereferenced schemas](dereferenced/index.md) describe records as written to `dereferenced/` and served by the API, with those ids replaced by the records they point to.

## How the records fit together

- A **statement** is a single knowledge claim. It points to a **proposition**, to the **strength** of the evidence, to the **indication** it was derived from, and to the **documents** it was reported in.
- A **proposition** says that one or more **biomarkers** predict a therapeutic response to a **therapy** (or a **therapy group** given together) in a **disease**. Each biomarker is attached through a **biomarker criterion**, which says whether that biomarker must be present or absent.
- A **biomarker** is a categorical variant, with one subtype per biomarker type. Depending on the type it refers to **genes**, **alleles**, **copy changes**, **function consequences** and **sequence locations**.
- An **indication** holds the regulatory approval text a statement was curated from, with one subtype per regulatory agency.
- **Documents** are the sources: at present, every document is a regulatory approval.
- **Contributions** record which **agent** created or changed a record, and when.
- **Codings** and **mappings** link concepts such as diseases, genes and therapies to the same concept in other vocabularies.

Two shared structures appear on many records: **extensions**, which carry information VA-Spec does not model directly (always with `name`, `value` and `description`), and **mappings**, which pair a coding in another system with a relation such as `exactMatch`.
