# Agent

Dereferenced schema · [Source](https://github.com/vanallenlab/moalmanac-db/blob/e8179c4641a1f5c3345e5ec6c6ca6239548605ed/schemas/dereferenced/agents.schema.json) · [Referenced version](../referenced/agents.md)

An organization or person that publishes documents or contributes to records.

## Fields

| Field | Type | Required | Description |
| --- | --- | --- | --- |
| <code>id</code> | string matching <code>^agent:(org&#124;user):[a-z0-9]+$</code> | yes |  |
| <code>type</code> | always <code>Agent</code> | yes |  |
| <code>agentType</code> | one of <code>organization</code>, <code>contributor</code> | yes |  |
| <code>name</code> | string | yes |  |
| <code>description</code> | string | yes |  |
| <code>extensions</code> | array of extensions (see [Extensions](#extensions)) |  |  |

## Extensions

Each extension is an object with a `name`, a `value`, and an optional `description` (see [Extension](extension.md)).

| Name | Value | Required |
| --- | --- | --- |
| <code>last_updated</code> | string |  |
| <code>url</code> | string |  |

## JSON Schema

??? note "Full JSON Schema"

    ```json
    {
      "$schema": "https://json-schema.org/draft/2020-12/schema",
      "$id": "https://moalmanac.org/schemas/dereferenced/agents.schema.json",
      "title": "Agent",
      "description": "An organization or person that publishes documents or contributes to records.",
      "type": "object",
      "properties": {
        "id": {
          "type": "string",
          "pattern": "^agent:(org|user):[a-z0-9]+$"
        },
        "type": {
          "const": "Agent"
        },
        "agentType": {
          "enum": [
            "organization",
            "contributor"
          ]
        },
        "name": {
          "type": "string"
        },
        "description": {
          "type": "string"
        },
        "extensions": {
          "type": "array",
          "items": {
            "anyOf": [
              {
                "$ref": "extension.schema.json",
                "properties": {
                  "name": {
                    "const": "last_updated"
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
                    "const": "url"
                  },
                  "value": {
                    "type": "string"
                  }
                }
              }
            ]
          }
        }
      },
      "required": [
        "id",
        "type",
        "agentType",
        "name",
        "description"
      ],
      "additionalProperties": false
    }
    ```
