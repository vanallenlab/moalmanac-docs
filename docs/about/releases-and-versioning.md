# Releases and versioning

## Database releases

Database content changes are made on a branch of [moalmanac-db](https://github.com/vanallenlab/moalmanac-db) and reviewed by other members of the curation team in a pull request before they are merged.

Releases are labeled by date, in the format `v.YYYY-MM-DD`. Each release is published on the repository's [releases page](https://github.com/vanallenlab/moalmanac-db/releases) with release notes, and every content change is summarized in the [content changelog](https://news.moalmanac.org/category/database).

Since the [2025-09-04 release](../news/posts/2025-09-04-database-release.md), each database release also has its own Zenodo DOI, so a specific version can be cited. See [Citation](citation.md).

## API

The API serves one database release at a time. Every response includes a `service` object with the `release` and `last_updated` date of the database that answered it, so you can tell which version your results came from. See [Responses](../api/reference/responses.md).

The API repository pins moalmanac-db as a submodule, so each API deployment corresponds to a specific database commit.

## This site

This site pins each repository it documents (moalmanac-db, moalmanac-api, moalmanac and moalmanac-browser) as a submodule. Generated pages say which commit they were built from.
