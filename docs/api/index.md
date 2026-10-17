# API

The MOAlmanac API serves the [dereferenced](../database/index.md#referenced-and-dereferenced-records) database records at [https://api.moalmanac.org](https://api.moalmanac.org). It is a read-only HTTP API: every request is a `GET`, and every response is JSON in the same [response envelope](reference/responses.md).

The API is built with FastAPI ([moalmanac-api](https://github.com/vanallenlab/moalmanac-api)). The live interactive documentation at [api.moalmanac.org](https://api.moalmanac.org) lets you try requests in your browser; the [endpoint reference](reference/index.md) on this site is generated from the same OpenAPI description.

## Try it

List the genes named BRAF:

```bash
curl "https://api.moalmanac.org/genes?gene_name=BRAF"
```

The response has three parts: `meta` describes the request and its result, `service` describes the database release that answered it, and `data` holds the records, here a list of [Gene](../database/schemas/dereferenced/genes.md) records.

## Filtering

Most endpoints accept filters as query parameters. Different filters combine with AND, and repeating a filter combines its values with OR:

```bash
curl "https://api.moalmanac.org/statements?gene=BRAF&gene=KRAS&disease=Melanoma"
```

See the [endpoint reference](reference/index.md) for each endpoint's filters, and the exception on `/search`.
