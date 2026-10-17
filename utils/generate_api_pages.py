"""
Generates the API reference pages from moalmanac-api's OpenAPI description.

Reads external/api/docs/openapi.json and writes one page per endpoint, an
Endpoints overview, and a Responses page to docs/api/reference/. That folder is
generated in full and ignored by git, so run this before `zensical build` or
`zensical serve`:

    python utils/generate_api_pages.py

Records are not described again here: each endpoint links to the database schema
pages written by utils/generate_schema_pages.py.

It also rewrites the API reference entries in mkdocs.yml's `nav`, between the
"# BEGIN generated API nav" and "# END generated API nav" comments. Commit that
change with the submodule update that caused it. With `--check`, mkdocs.yml is
left unchanged and the script exits with status 1 if those entries are out of
date; CI runs it this way.
"""

import argparse
import json
import pathlib
import shutil
import sys
import urllib.parse

import generate_schema_pages

REPOSITORY_ROOT = pathlib.Path(__file__).resolve().parents[1]
API_DIRECTORY = REPOSITORY_ROOT / "external" / "api"
OUTPUT_DIRECTORY = REPOSITORY_ROOT / "docs" / "api" / "reference"
CONFIG_PATH = REPOSITORY_ROOT / "mkdocs.yml"
API_REPOSITORY_URL = "https://github.com/vanallenlab/moalmanac-api"
BASE_URL = "https://api.moalmanac.org"
NAV_BEGIN = "# BEGIN generated API nav"
NAV_END = "# END generated API nav"
COMPONENTS_PREFIX = "#/components/schemas/"

# From docs/api/reference/ to the generated database schema pages.
SCHEMA_PAGES = "../../database/schemas"


def component_name(schema: dict) -> str | None:
    """
    Returns the component a `$ref` points to.

    Args:
        schema (dict): A schema, e.g. `{"$ref": "#/components/schemas/Gene"}`.

    Returns:
        str | None: The component name, e.g. "Gene", or None if not a component
            reference.
    """
    reference = schema.get("$ref", "")
    return reference.removeprefix(COMPONENTS_PREFIX) if reference.startswith(COMPONENTS_PREFIX) else None


def endpoint_page(path: str) -> str:
    """
    Names the page for an endpoint.

    Args:
        path (str): The endpoint's path, e.g. "/biomarker_criteria".

    Returns:
        str: The page's filename, e.g. "biomarker_criteria.md".
    """
    return f"{path.strip('/')}.md"


def endpoint_title(path: str) -> str:
    """
    Names an endpoint for the sidebar.

    Args:
        path (str): The endpoint's path, e.g. "/biomarker_criteria".

    Returns:
        str: The title, e.g. "Biomarker criteria".
    """
    return path.strip("/").replace("_", " ").capitalize()


def example_request(path: str, operation: dict) -> str:
    """
    Builds an example `curl` command, using one parameter's documented example.

    Prefers a name filter (e.g. `gene_name`), since those read most naturally.

    Args:
        path (str): The endpoint's path.
        operation (dict): The OpenAPI operation.

    Returns:
        str: The command.
    """
    candidates = [
        parameter
        for parameter in operation.get("parameters", [])
        if parameter.get("schema", {}).get("examples")
    ]
    candidates.sort(key=lambda parameter: not parameter["name"].endswith("_name"))
    query = ""
    if candidates:
        parameter = candidates[0]
        example = parameter["schema"]["examples"][0]
        value = example[0] if isinstance(example, list) else example
        query = "?" + urllib.parse.urlencode({parameter["name"]: value})
    return f'curl "{BASE_URL}{path}{query}"'


def main() -> int:
    """
    Generates every API reference page, and updates or checks the API reference
    entries in mkdocs.yml's `nav`.

    Returns:
        int: The exit status: 0 on success; 1 if the OpenAPI description or nav
            markers are missing, or if `--check` found the nav out of date.
    """
    parser = argparse.ArgumentParser(description=__doc__.strip().splitlines()[0])
    parser.add_argument(
        "--api-directory",
        type=pathlib.Path,
        default=API_DIRECTORY,
        help="The moalmanac-api checkout (default: external/api).",
    )
    parser.add_argument(
        "--output-directory",
        type=pathlib.Path,
        default=OUTPUT_DIRECTORY,
        help="Where to write pages (default: docs/api/reference).",
    )
    parser.add_argument(
        "--config",
        type=pathlib.Path,
        default=CONFIG_PATH,
        help="The site configuration whose nav to update (default: mkdocs.yml).",
    )
    parser.add_argument(
        "--check",
        action="store_true",
        help="Do not change the config; exit with status 1 if its API nav is out of date.",
    )
    arguments = parser.parse_args()

    specification_path = arguments.api_directory / "docs" / "openapi.json"
    if not specification_path.is_file():
        print(
            f"{specification_path} not found. Fetch the submodules with "
            "`git submodule update --init`, and make sure external/api is pinned "
            "to a commit that has docs/openapi.json.",
            file=sys.stderr,
        )
        return 1

    specification = json.loads(specification_path.read_text())
    commit = generate_schema_pages.db_commit(db_directory=arguments.api_directory)
    record_pages = schema_page_links()
    pages = render_pages(specification=specification, record_pages=record_pages, commit=commit)

    output = arguments.output_directory
    if output.exists():
        shutil.rmtree(output)
    output.mkdir(parents=True)
    for name, lines in pages.items():
        (output / name).write_text("\n".join(lines).rstrip() + "\n")
    print(f"Wrote {len(pages)} pages for moalmanac-api {commit[:7] if commit else '(unknown commit)'}.")

    config = arguments.config.read_text()
    try:
        updated = generate_schema_pages.replace_between_markers(
            config=config,
            begin_marker=NAV_BEGIN,
            end_marker=NAV_END,
            render=lambda indent: nav_entries(paths=ordered_paths(specification), indent=indent),
        )
    except ValueError as error:
        print(error, file=sys.stderr)
        return 1
    if updated == config:
        print(f"{arguments.config.name} API nav is up to date.")
    elif arguments.check:
        print(
            f"{arguments.config.name} API nav is out of date. Run "
            "`python utils/generate_api_pages.py` and commit the result.",
            file=sys.stderr,
        )
        return 1
    else:
        arguments.config.write_text(updated)
        print(f"Updated the API nav in {arguments.config.name}.")
    return 0


def nav_entries(paths: list[str], indent: str) -> list[str]:
    """
    Renders the API reference entries for mkdocs.yml's `nav`.

    Args:
        paths (list[str]): Every endpoint's path, in display order.
        indent (str): The indentation of the entries, matching the markers.

    Returns:
        list[str]: YAML lines: an Endpoints section (overview, then one entry
            per endpoint) and the Responses page.
    """
    lines = [f"{indent}- Endpoints:", f"{indent}    - Overview: api/reference/index.md"]
    for path in paths:
        title = generate_schema_pages.yaml_key(endpoint_title(path))
        lines.append(f"{indent}    - {title}: api/reference/{endpoint_page(path)}")
    return [*lines, f"{indent}- Responses: api/reference/responses.md"]


def ordered_paths(specification: dict) -> list[str]:
    """
    Orders endpoints by their tag (in the order tags are declared), then path.

    Args:
        specification (dict): The OpenAPI description.

    Returns:
        list[str]: Every endpoint's path.
    """
    tags = [tag["name"] for tag in specification.get("tags", [])]

    def key(path: str) -> tuple[int, str]:
        tag = specification["paths"][path]["get"].get("tags", [""])[0]
        return (tags.index(tag) if tag in tags else len(tags), path)

    return sorted(specification["paths"], key=key)


def paragraphs(text: str) -> list[str]:
    """
    Joins a docstring's wrapped lines into paragraphs.

    Args:
        text (str): The text, with single newlines inside paragraphs and blank
            lines between them.

    Returns:
        list[str]: Markdown lines, one per paragraph, each followed by a blank line.
    """
    lines = []
    for paragraph in text.strip().split("\n\n"):
        lines += [" ".join(paragraph.split()), ""]
    return lines


def parameter_rows(operation: dict) -> list[str]:
    """
    Builds the Parameters table for an endpoint.

    Args:
        operation (dict): The OpenAPI operation.

    Returns:
        list[str]: Markdown lines, or a sentence if there are no parameters.
    """
    parameters = operation.get("parameters", [])
    if not parameters:
        return ["This endpoint takes no parameters.", ""]

    lines = ["| Name | Type | Description | Example |", "| --- | --- | --- | --- |"]
    for parameter in parameters:
        schema = parameter.get("schema", {})
        if schema.get("type") == "array":
            kind = f"{generate_schema_pages.describe(schema.get('items', {}), None)} (repeatable)"
        else:
            kind = generate_schema_pages.describe(schema, None)
        if "default" in schema:
            kind += f", default {generate_schema_pages.code(generate_schema_pages.literal(schema['default']))}"
        example = ""
        if schema.get("examples"):
            value = schema["examples"][0]
            value = value[0] if isinstance(value, list) else value
            example = generate_schema_pages.code(generate_schema_pages.literal(value))
        description = generate_schema_pages.cell(parameter.get("description", ""))
        name = generate_schema_pages.code(parameter["name"])
        lines.append(f"| {name} | {kind} | {description} | {example} |")
    return [*lines, ""]


def render_endpoint(
    path: str,
    operation: dict,
    specification: dict,
    record_pages: dict[str, str],
) -> list[str]:
    """
    Renders one endpoint's page.

    Args:
        path (str): The endpoint's path.
        operation (dict): The OpenAPI operation.
        specification (dict): The OpenAPI description, for component examples.
        record_pages (dict[str, str]): Links to record schema pages, keyed by
            component name.

    Returns:
        list[str]: Markdown lines.
    """
    components = specification["components"]["schemas"]
    lines = [f"# {operation.get('summary', path)}", "", f"`GET {BASE_URL}{path}`", ""]
    lines += paragraphs(operation.get("description", ""))
    lines += ["## Parameters", "", *parameter_rows(operation)]
    lines += ["## Example request", "", "```bash", example_request(path, operation), "```", ""]

    response = operation["responses"]["200"]["content"]["application/json"]["schema"]
    data = response["properties"]["data"]
    is_list = data.get("type") == "array"
    record = component_name(data.get("items", {}) if is_list else data)
    lines += ["## Response", "", f"Returns the [standard response envelope](responses.md), with `data` set to {returns(record, is_list, record_pages)}.", ""]

    meta = response["properties"]["meta"].get("examples", [{}])[0]
    example_record = components.get(record, {}).get("examples", [None])[0]
    if example_record is not None:
        example = {
            "meta": meta,
            "service": components["About"]["examples"][0],
            "data": [example_record] if is_list else example_record,
        }
        lines += ['??? example "Example response"', ""]
        lines += generate_schema_pages.json_block(example, indent="    ")
    return lines


def render_index(specification: dict, record_pages: dict[str, str], commit: str | None) -> list[str]:
    """
    Renders the Endpoints overview: how to call the API, and a table of every
    endpoint by tag.

    Args:
        specification (dict): The OpenAPI description.
        record_pages (dict[str, str]): Links to record schema pages, keyed by
            component name.
        commit (str | None): The moalmanac-api commit, for the source link.

    Returns:
        list[str]: Markdown lines.
    """
    lines = [
        "# Endpoints",
        "",
        f"Every endpoint is a `GET` request to `{BASE_URL}` and returns JSON in the "
        "[standard response envelope](responses.md). You can also try requests "
        f"in your browser with the interactive documentation at [{BASE_URL}]({BASE_URL}).",
        "",
    ]
    if commit:
        lines += [
            f"Generated from moalmanac-api at commit [`{commit[:7]}`]"
            f"({API_REPOSITORY_URL}/tree/{commit}/docs/openapi.json).",
            "",
        ]
    description = specification["info"].get("description", "")
    if "**Filtering**" in description:
        filtering = description.split("**Filtering**", 1)[1]
        lines += ["## Filtering", "", filtering.strip(), ""]

    tags = {tag["name"]: tag.get("description", "") for tag in specification.get("tags", [])}
    paths = ordered_paths(specification)
    for tag, tag_description in tags.items():
        tagged = [path for path in paths if specification["paths"][path]["get"].get("tags", [""])[0] == tag]
        if not tagged:
            continue
        lines += [f"## {tag}", "", tag_description, "", "| Endpoint | Summary | Returns |", "| --- | --- | --- |"]
        for path in tagged:
            operation = specification["paths"][path]["get"]
            data = operation["responses"]["200"]["content"]["application/json"]["schema"]["properties"]["data"]
            is_list = data.get("type") == "array"
            record = component_name(data.get("items", {}) if is_list else data)
            lines.append(
                f"| [`{path}`]({endpoint_page(path)}) | {operation.get('summary', '')} | "
                f"{returns(record, is_list, record_pages, short=True)} |",
            )
        lines.append("")
    return lines


def render_pages(
    specification: dict,
    record_pages: dict[str, str],
    commit: str | None,
) -> dict[str, list[str]]:
    """
    Renders every API reference page.

    Args:
        specification (dict): The OpenAPI description.
        record_pages (dict[str, str]): Links to record schema pages, keyed by
            component name.
        commit (str | None): The moalmanac-api commit, for the source link.

    Returns:
        dict[str, list[str]]: Markdown lines keyed by output filename.
    """
    pages = {
        "index.md": render_index(specification, record_pages, commit),
        "responses.md": render_responses(specification, record_pages),
    }
    for path in ordered_paths(specification):
        pages[endpoint_page(path)] = render_endpoint(
            path=path,
            operation=specification["paths"][path]["get"],
            specification=specification,
            record_pages=record_pages,
        )
    return pages


def render_responses(specification: dict, record_pages: dict[str, str]) -> list[str]:
    """
    Renders the Responses page: the envelope every endpoint returns, the fields
    the API adds to records, and errors.

    Args:
        specification (dict): The OpenAPI description.
        record_pages (dict[str, str]): Links to record schema pages, keyed by
            component name.

    Returns:
        list[str]: Markdown lines.
    """
    components = specification["components"]["schemas"]
    search = components["SearchResult"]
    contribution = components["ContributionResult"]
    records = contribution["properties"]["extensions"]["items"]
    return [
        "# Responses",
        "",
        "Every endpoint returns a JSON object with the same three keys:",
        "",
        "| Key | Contents |",
        "| --- | --- |",
        "| `meta` | Information about the request and response (see [below](#meta)). |",
        f"| `service` | The [About]({record_pages['About']}) record: which moalmanac-db release the API is serving. |",
        "| `data` | The results. For `/about`, a single object; for every other endpoint, a list of records. Each endpoint's page links to the schema of its records. |",
        "",
        "## meta",
        "",
        *generate_schema_pages.fields_table(components["Meta"], None),
        "## Search results",
        "",
        f"`/search` returns [Proposition]({record_pages['Proposition']}) records, each with an added `aggregates` object summarizing the statements made about it:",
        "",
        *generate_schema_pages.fields_table(search["properties"]["aggregates"], None),
        "## Contribution records",
        "",
        f"With `include_records=true`, each [Contribution]({record_pages['Contribution']}) from `/contributions` gains an extension named `records` listing what it contributed:",
        "",
        *generate_schema_pages.fields_table(records, None),
        "## Empty results and errors",
        "",
        "- A request whose filters match nothing returns status 200 with an empty `data` list.",
        "- Parameters an endpoint doesn't accept are ignored.",
        "- A parameter value of the wrong type (for example `include_deprecated=maybe`) returns status 422, with a `detail` list describing each problem.",
    ]


def returns(record: str | None, is_list: bool, record_pages: dict[str, str], short: bool = False) -> str:
    """
    Describes what an endpoint's `data` holds, linking to the record's schema.

    Args:
        record (str | None): The record's component name, e.g. "Gene".
        is_list (bool): Whether `data` is a list of records.
        record_pages (dict[str, str]): Links to record schema pages, keyed by
            component name.
        short (bool): If True, a short form for tables (default: False).

    Returns:
        str: A description such as "a list of [Gene](...) records".
    """
    special = {
        "SearchResult": ("[Proposition]({Proposition}) records with [aggregates](responses.md#search-results)"),
        "ContributionResult": ("[Contribution]({Contribution}) records, optionally with [their records](responses.md#contribution-records)"),
    }
    if record in special:
        noun = special[record].format(**record_pages)
    elif record in record_pages:
        noun = f"[{record}]({record_pages[record]})"
        noun = noun if not is_list else f"{noun} records"
    else:
        noun = generate_schema_pages.code(record or "any")
    if short:
        return noun if is_list or record in special else f"{noun} record"
    if record in special:
        return f"a list of {noun}"
    return f"a list of {noun}" if is_list else f"the {noun} record"


def schema_page_links() -> dict[str, str]:
    """
    Maps each record component to its page from utils/generate_schema_pages.py.

    The API returns dereferenced records, so components link to the dereferenced
    schema pages, except `About`, which only has a referenced schema.

    Returns:
        dict[str, str]: Relative links from docs/api/reference/, keyed by
            component name (the schema's title), e.g. "Gene".
    """
    links = {}
    schemas = generate_schema_pages.DB_DIRECTORY / "schemas"
    for category in ("referenced", "dereferenced"):
        for path in sorted((schemas / category).glob("*.schema.json")):
            title = json.loads(path.read_text())["title"]
            links[title] = f"{SCHEMA_PAGES}/{category}/{path.name.removesuffix('.schema.json')}.md"
    return links


if __name__ == "__main__":
    sys.exit(main())
