# Document

Dereferenced schema · [Source](https://github.com/vanallenlab/moalmanac-db/blob/e8179c4641a1f5c3345e5ec6c6ca6239548605ed/schemas/dereferenced/documents.schema.json) · [Referenced version](../referenced/documents.md)

A source document. Publisher, company, drug names, dates, and status are extensions; urls are plain strings.

## Fields

| Field | Type | Required | Description |
| --- | --- | --- | --- |
| <code>id</code> | string matching <code>^doc:(fda&#124;ema&#124;hse&#124;hc&#124;hpra):.+$</code> | yes |  |
| <code>type</code> | always <code>Document</code> | yes |  |
| <code>documentType</code> | one of <code>Regulatory approval</code> | yes |  |
| <code>name</code> | string | yes |  |
| <code>title</code> | string or null | yes |  |
| <code>aliases</code> | array of string | yes |  |
| <code>description</code> | string | yes |  |
| <code>urls</code> | array of string format <code>uri</code> | yes |  |
| <code>doi</code> | string or null | yes |  |
| <code>pmid</code> | string or null | yes |  |
| <code>extensions</code> | array of extensions (see [Extensions](#extensions)) | yes |  |

## Extensions

Each extension is an object with a `name`, a `value`, and an optional `description` (see [Extension](extension.md)).

| Name | Value | Required |
| --- | --- | --- |
| <code>agent</code> | [Agent](agents.md) without <code>extensions</code> | yes |
| <code>company</code> | string | yes |
| <code>drug_name_brand</code> | string or null | yes |
| <code>drug_name_generic</code> | string or null | yes |
| <code>first_publication_date</code> | [iso_date_or_null](#iso_date_or_null) | yes |
| <code>publication_date</code> | [iso_date_or_null](#iso_date_or_null) | yes |
| <code>regulatory_identifier</code> | string or null | yes |
| <code>status</code> | one of <code>Active</code>, <code>Deprecated</code> | yes |

## Definitions

### iso_date_or_null

An ISO 8601 date (YYYY-MM-DD) or null.

Type: null or string format <code>date</code>

## Additional rules

These rules also apply to every record:

- When <code>id</code> matches <code>^doc:fda:</code>: <code>extensions</code> must contain <code>regulatory_identifier</code> extension with value string matching <code>^(BLA&#124;NDA)[0-9]{6}$</code>.

## JSON Schema

??? note "Full JSON Schema"

    ```json
    {
      "$schema": "https://json-schema.org/draft/2020-12/schema",
      "$id": "https://moalmanac.org/schemas/dereferenced/documents.schema.json",
      "title": "Document",
      "description": "A source document. Publisher, company, drug names, dates, and status are extensions; urls are plain strings.",
      "type": "object",
      "properties": {
        "id": {
          "type": "string",
          "pattern": "^doc:(fda|ema|hse|hc|hpra):.+$"
        },
        "type": {
          "const": "Document"
        },
        "documentType": {
          "enum": [
            "Regulatory approval"
          ]
        },
        "name": {
          "type": "string"
        },
        "title": {
          "type": [
            "string",
            "null"
          ]
        },
        "aliases": {
          "type": "array",
          "items": {
            "type": "string"
          }
        },
        "description": {
          "type": "string"
        },
        "urls": {
          "type": "array",
          "items": {
            "type": "string",
            "format": "uri"
          }
        },
        "doi": {
          "type": [
            "string",
            "null"
          ]
        },
        "pmid": {
          "type": [
            "string",
            "null"
          ]
        },
        "extensions": {
          "type": "array",
          "items": {
            "anyOf": [
              {
                "$ref": "extension.schema.json",
                "properties": {
                  "name": {
                    "const": "agent"
                  },
                  "value": {
                    "$ref": "agents.schema.json",
                    "not": {
                      "required": [
                        "extensions"
                      ]
                    }
                  }
                }
              },
              {
                "$ref": "extension.schema.json",
                "properties": {
                  "name": {
                    "const": "company"
                  },
                  "value": {
                    "type": "string"
                  }
                }
              },
              {
                "$ref": "extension.schema.json",
                "properties": {
                  "name": {
                    "const": "drug_name_brand"
                  },
                  "value": {
                    "type": [
                      "string",
                      "null"
                    ]
                  }
                }
              },
              {
                "$ref": "extension.schema.json",
                "properties": {
                  "name": {
                    "const": "drug_name_generic"
                  },
                  "value": {
                    "type": [
                      "string",
                      "null"
                    ]
                  }
                }
              },
              {
                "$ref": "extension.schema.json",
                "properties": {
                  "name": {
                    "const": "first_publication_date"
                  },
                  "value": {
                    "$ref": "#/$defs/iso_date_or_null"
                  }
                }
              },
              {
                "$ref": "extension.schema.json",
                "properties": {
                  "name": {
                    "const": "publication_date"
                  },
                  "value": {
                    "$ref": "#/$defs/iso_date_or_null"
                  }
                }
              },
              {
                "$ref": "extension.schema.json",
                "properties": {
                  "name": {
                    "const": "regulatory_identifier"
                  },
                  "value": {
                    "type": [
                      "string",
                      "null"
                    ]
                  }
                }
              },
              {
                "$ref": "extension.schema.json",
                "properties": {
                  "name": {
                    "const": "status"
                  },
                  "value": {
                    "enum": [
                      "Active",
                      "Deprecated"
                    ]
                  }
                }
              }
            ]
          },
          "allOf": [
            {
              "contains": {
                "$ref": "extension.schema.json",
                "properties": {
                  "name": {
                    "const": "agent"
                  },
                  "value": {
                    "$ref": "agents.schema.json",
                    "not": {
                      "required": [
                        "extensions"
                      ]
                    }
                  }
                }
              }
            },
            {
              "contains": {
                "$ref": "extension.schema.json",
                "properties": {
                  "name": {
                    "const": "company"
                  },
                  "value": {
                    "type": "string"
                  }
                }
              }
            },
            {
              "contains": {
                "$ref": "extension.schema.json",
                "properties": {
                  "name": {
                    "const": "drug_name_brand"
                  },
                  "value": {
                    "type": [
                      "string",
                      "null"
                    ]
                  }
                }
              }
            },
            {
              "contains": {
                "$ref": "extension.schema.json",
                "properties": {
                  "name": {
                    "const": "drug_name_generic"
                  },
                  "value": {
                    "type": [
                      "string",
                      "null"
                    ]
                  }
                }
              }
            },
            {
              "contains": {
                "$ref": "extension.schema.json",
                "properties": {
                  "name": {
                    "const": "first_publication_date"
                  },
                  "value": {
                    "$ref": "#/$defs/iso_date_or_null"
                  }
                }
              }
            },
            {
              "contains": {
                "$ref": "extension.schema.json",
                "properties": {
                  "name": {
                    "const": "publication_date"
                  },
                  "value": {
                    "$ref": "#/$defs/iso_date_or_null"
                  }
                }
              }
            },
            {
              "contains": {
                "$ref": "extension.schema.json",
                "properties": {
                  "name": {
                    "const": "regulatory_identifier"
                  },
                  "value": {
                    "type": [
                      "string",
                      "null"
                    ]
                  }
                }
              }
            },
            {
              "contains": {
                "$ref": "extension.schema.json",
                "properties": {
                  "name": {
                    "const": "status"
                  },
                  "value": {
                    "enum": [
                      "Active",
                      "Deprecated"
                    ]
                  }
                }
              }
            }
          ]
        }
      },
      "required": [
        "id",
        "type",
        "documentType",
        "name",
        "title",
        "aliases",
        "description",
        "urls",
        "doi",
        "pmid",
        "extensions"
      ],
      "additionalProperties": false,
      "allOf": [
        {
          "if": {
            "required": [
              "id"
            ],
            "properties": {
              "id": {
                "pattern": "^doc:fda:"
              }
            }
          },
          "then": {
            "properties": {
              "extensions": {
                "contains": {
                  "$ref": "extension.schema.json",
                  "properties": {
                    "name": {
                      "const": "regulatory_identifier"
                    },
                    "value": {
                      "type": "string",
                      "pattern": "^(BLA|NDA)[0-9]{6}$"
                    }
                  }
                }
              }
            }
          }
        }
      ],
      "$defs": {
        "iso_date_or_null": {
          "description": "An ISO 8601 date (YYYY-MM-DD) or null.",
          "oneOf": [
            {
              "type": "null"
            },
            {
              "type": "string",
              "format": "date"
            }
          ]
        }
      }
    }
    ```
