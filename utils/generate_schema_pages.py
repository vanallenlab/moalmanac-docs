"""
Generates the database schema reference pages from moalmanac-db's JSON Schemas.

Reads external/db/schemas/{referenced,dereferenced}/*.schema.json and writes one
page per schema, plus an index page per category listing every schema, to
docs/database/schemas/{referenced,dereferenced}/. Those two folders are generated
in full and ignored by git, so run this before `zensical build` or
`zensical serve`:

    python utils/generate_schema_pages.py

It also rewrites the schema entries in mkdocs.yml's `nav`, between the
"# BEGIN generated schema nav" and "# END generated schema nav" comments, so every
schema page appears in the sidebar. Commit that change with the submodule update
that caused it. With `--check`, mkdocs.yml is left unchanged and the script exits
with status 1 if its schema entries are out of date; CI runs it this way.
"""

import argparse
import html
import json
import pathlib
import re
import shutil
import subprocess
import sys
import typing
import unicodedata

REPOSITORY_ROOT = pathlib.Path(__file__).resolve().parents[1]
DB_DIRECTORY = REPOSITORY_ROOT / "external" / "db"
OUTPUT_DIRECTORY = REPOSITORY_ROOT / "docs" / "database" / "schemas"
CONFIG_PATH = REPOSITORY_ROOT / "mkdocs.yml"
NAV_BEGIN = "# BEGIN generated schema nav"
NAV_END = "# END generated schema nav"
DB_REPOSITORY_URL = "https://github.com/vanallenlab/moalmanac-db"

# Title and introduction for each category's index page, keyed by folder name.
CATEGORIES = {
    "referenced": (
        "Referenced schemas",
        "Records as stored in moalmanac-db's `referenced/` files. Foreign keys are "
        "ids that point to records in other tables.",
    ),
    "dereferenced": (
        "Dereferenced schemas",
        "Records as written to moalmanac-db's `dereferenced/` files and served by "
        "the API, with foreign keys replaced by the records they point to.",
    ),
}


class Context(typing.NamedTuple):
    """
    What a page needs to link to other schemas in the same category.

    Attributes:
        filename (str): The schema being rendered, e.g. "indications.schema.json".
        titles (dict[str, str]): Schema titles keyed by filename.
        roots (dict[str, str | None]): Each schema's root `$defs` entry (the one
            its top-level `$ref` points to), keyed by filename, or None.
    """

    filename: str
    titles: dict[str, str]
    roots: dict[str, str | None]


def anchor(name: str) -> str:
    """
    Converts a heading to the anchor id the site generates for it.

    Args:
        name (str): The heading text, e.g. "Copy Number (arm level)".

    Returns:
        str: The anchor id, e.g. "copy-number-arm-level".
    """
    value = unicodedata.normalize("NFKD", name).encode("ascii", "ignore").decode()
    value = re.sub(r"[^\w\s-]", "", value).strip().lower()
    return re.sub(r"[-\s]+", "-", value)


def cell(text: str) -> str:
    """
    Makes plain text safe for a Markdown table cell.

    Args:
        text (str): The text, which may contain newlines or pipes.

    Returns:
        str: The text on one line, with pipes escaped.
    """
    return " ".join(text.split()).replace("|", "\\|")


def code(text: str) -> str:
    """
    Formats text as inline code that is safe inside a Markdown table cell.

    A backslash-escaped pipe inside backticks renders with the backslash, so this
    writes a `<code>` element with the pipe as an HTML entity instead.

    Args:
        text (str): The code text, e.g. a regex pattern.

    Returns:
        str: An HTML `<code>` element.
    """
    escaped = html.escape(text, quote=False).replace("|", "&#124;")
    return f"<code>{escaped}</code>"


def constraints(node: dict, context: Context | None) -> str | None:
    """
    Describes the property constraints in a rule's `then`, `else`, or `oneOf`
    branch, e.g. "`state_length` is integer".

    Args:
        node (dict): A schema with only `properties` (and optionally `required`).
        context (Context | None): Used to link `$ref`s.

    Returns:
        str | None: The constraints joined with "and", or None if the schema has
            anything other than properties to describe.
    """
    if set(node) - {"properties", "required"} or not node.get("properties"):
        return None
    clauses = []
    for key, value in node["properties"].items():
        description = describe(value, context)
        if description.startswith("containing "):
            description = "must contain " + description.removeprefix("containing ")
        elif not description.startswith(("matching", "with", "without", "not")):
            description = "is " + description
        clauses.append(f"{code(key)} {description}")
    return " and ".join(clauses)


def condition(rule: dict) -> str:
    """
    Describes the `if` of a subtype rule, e.g. which id prefix selects it.

    Args:
        rule (dict): The `if` schema, e.g. `{"properties": {"id": {"pattern": ...}}}`.

    Returns:
        str: A description such as "`id` matches `^ind:fda:`".
    """
    clauses = []
    for key, constraint in rule.get("properties", {}).items():
        contained = constraint.get("contains", {})
        name = extension_name(contained)
        if key == "extensions" and name is not None:
            value = contained["properties"].get("value", {})
            shown = code(literal(value["const"])) if "const" in value else describe(value, None)
            clauses.append(f"{code(name)} extension is {shown}")
        elif "pattern" in constraint:
            clauses.append(f"{code(key)} matches {code(constraint['pattern'])}")
        elif "const" in constraint:
            clauses.append(f"{code(key)} is {code(literal(constraint['const']))}")
        else:
            clauses.append(f"{code(key)} is {describe(constraint, None)}")
    return " and ".join(clauses) or code(json.dumps(rule))


def describe(node: typing.Any, context: Context | None) -> str:
    """
    Describes a schema in a short phrase for a table cell.

    Args:
        node (typing.Any): A schema, e.g. `{"type": ["string", "null"]}`.
        context (Context | None): Used to link `$ref`s; None leaves them as code.

    Returns:
        str: A description such as "string or null".
    """
    if not isinstance(node, dict):
        return "any"

    name = extension_name(node)
    if name is not None and "value" in node.get("properties", {}):
        return f"{code(name)} extension with value {describe(node['properties']['value'], context)}"

    parts = []
    if "$ref" in node:
        parts.append(reference_link(node["$ref"], context))
    if "const" in node:
        parts.append(f"always {code(literal(node['const']))}")
    if "enum" in node:
        parts.append("one of " + ", ".join(code(literal(v)) for v in node["enum"]))
    if "$ref" not in node and ("type" in node or "items" in node or "properties" in node):
        parts.append(describe_type(node, context))
    for key in ("anyOf", "oneOf"):
        if key in node:
            parts.append(" or ".join(describe(option, context) for option in node[key]))
    if "allOf" in node:
        parts.append(" and ".join(describe(part, context) for part in node["allOf"]))

    qualifiers = []
    if "$ref" in node and "properties" in node:
        overlays = [f"{code(key)} {describe(value, context)}" for key, value in node["properties"].items()]
        qualifiers.append("with " + ", ".join(overlays))
    if "pattern" in node:
        qualifiers.append(f"matching {code(node['pattern'])}")
    if "format" in node:
        qualifiers.append(f"format {code(node['format'])}")
    if "minimum" in node:
        qualifiers.append(f"at least {node['minimum']}")
    if "contains" in node:
        qualifiers.append(f"containing {describe(node['contains'], context)}")
    if "not" in node:
        excluded = node["not"]
        if set(excluded) == {"required"}:
            qualifiers.append("without " + ", ".join(code(k) for k in excluded["required"]))
        else:
            qualifiers.append(f"not {describe(excluded, context)}")

    if not parts:
        return ", ".join(qualifiers) or "any"
    return ", ".join(parts) + (" " + ", ".join(qualifiers) if qualifiers else "")


def describe_type(node: dict, context: Context | None) -> str:
    """
    Describes a schema's `type`, including what an array holds.

    Args:
        node (dict): A schema with `type`, `items`, or `properties`.
        context (Context | None): Used to link `$ref`s in array items.

    Returns:
        str: A description such as "array of string (exactly 2 items)".
    """
    types = node.get("type")
    if types is None:
        types = "array" if "items" in node else "object"
    if isinstance(types, str):
        types = [types]

    descriptions = []
    for kind in types:
        if kind != "array":
            descriptions.append(kind)
            continue
        if "prefixItems" in node:
            items = ", ".join(describe(item, context) for item in node["prefixItems"])
            descriptions.append(f"array of ({items})")
        elif "items" in node:
            items = node["items"]
            if isinstance(items, dict) and "properties" in items and "$ref" not in items:
                descriptions.append("array of objects")
            else:
                descriptions.append(f"array of {describe(items, context)}")
        else:
            descriptions.append("array")
        count = item_count(node)
        if count:
            descriptions[-1] += f" ({count})"
    return " or ".join(descriptions)


def extension_note(value: dict, required: bool, context: Context) -> str:
    """
    Describes an extension's value and whether it is required, in parentheses.

    Args:
        value (dict): The extension's value schema; empty if unconstrained.
        required (bool): Whether the extension is required.
        context (Context): Used to link `$ref`s.

    Returns:
        str: A note such as " (string, required)", or "" if there is nothing to add.
    """
    notes = [describe(value, context)] if value else []
    if required:
        notes.append("required")
    return f" ({', '.join(notes)})" if notes else ""


def extension_rules(extensions: dict) -> list[tuple[str, dict, bool]]:
    """
    Finds the named extensions an `extensions` array allows or requires.

    Allowed extensions are listed in `items.anyOf`; required ones are `contains`
    rules, directly or in `allOf`. A required extension need not also be listed
    as allowed, e.g. when `items` accepts any extension.

    Args:
        extensions (dict): The `extensions` property schema.

    Returns:
        list[tuple[str, dict, bool]]: The name, value schema, and whether it is
            required, for each named extension; empty if none are named.
    """
    rules: dict[str, tuple[dict, bool]] = {}
    for option in extensions.get("items", {}).get("anyOf", []):
        name = extension_name(option)
        if name is not None:
            rules[name] = (option["properties"].get("value", {}), False)
    for rule in [*extensions.get("allOf", []), extensions]:
        contains = rule.get("contains", {})
        name = extension_name(contains)
        if name is not None:
            value = rules[name][0] if name in rules else contains["properties"].get("value", {})
            rules[name] = (value, True)
    return [(name, value, required) for name, (value, required) in rules.items()]


def extension_name(node: typing.Any) -> str | None:
    """
    Returns the name an extension schema fixes with `properties.name.const`.

    Args:
        node (typing.Any): A schema, e.g. an item of an `extensions` array.

    Returns:
        str | None: The extension's name, or None if it is not fixed.
    """
    if not isinstance(node, dict):
        return None
    name = node.get("properties", {}).get("name", {})
    return name.get("const") if isinstance(name, dict) else None


def extension_rows(extensions: dict, context: Context) -> list[str]:
    """
    Builds the Extensions table for an `extensions` array.

    Args:
        extensions (dict): The `extensions` property schema.
        context (Context): Used to link `$ref`s in extension values.

    Returns:
        list[str]: Markdown lines, or an empty list if the extensions are not
            constrained by name.
    """
    rules = extension_rules(extensions)
    if not rules:
        return []

    lines = [
        "## Extensions",
        "",
        "Each extension is an object with a `name`, a `value`, and an optional "
        "`description` (see [Extension](extension.md)).",
        "",
        "| Name | Value | Required |",
        "| --- | --- | --- |",
    ]
    for name, value, required in rules:
        lines.append(
            f"| {code(name)} | {describe(value, context)} | {'yes' if required else ''} |",
        )
    return [*lines, ""]


def field_rows(
    node: dict,
    context: Context,
    prefix: str = "",
    link_extensions: bool = False,
) -> list[str]:
    """
    Builds table rows for an object's properties, including nested objects.

    Nested fields are listed with dotted names (`parent.child`), and fields of
    objects inside arrays with brackets (`parent[].child`).

    Args:
        node (dict): An object schema with `properties` and `required`.
        context (Context): Used to link `$ref`s.
        prefix (str): The parent field's path, for nested fields (default: "").
        link_extensions (bool): If True, a top-level `extensions` field links to
            the page's Extensions section; otherwise its allowed extensions are
            listed inline (default: False).

    Returns:
        list[str]: Markdown table rows.
    """
    rows = []
    required = set(node.get("required", []))
    for name, field in node.get("properties", {}).items():
        path = f"{prefix}{name}"
        rules = extension_rules(field) if name == "extensions" else []
        if rules and link_extensions and not prefix:
            kind = "array of extensions (see [Extensions](#extensions))"
        elif rules:
            kind = "array of extensions: " + ", ".join(
                code(rule_name) + extension_note(value, required, context)
                for rule_name, value, required in rules
            )
        else:
            kind = describe(field, context)
        description = cell(field.get("description", "")) if isinstance(field, dict) else ""
        rows.append(
            f"| {code(path)} | {kind} | {'yes' if name in required else ''} | {description} |",
        )
        if not isinstance(field, dict) or "$ref" in field:
            continue
        if "properties" in field:
            rows.extend(field_rows(field, context, prefix=f"{path}."))
        items = field.get("items")
        if isinstance(items, dict) and "properties" in items and "$ref" not in items:
            rows.extend(field_rows(items, context, prefix=f"{path}[]."))
    return rows


def fields_table(node: dict, context: Context, link_extensions: bool = False) -> list[str]:
    """
    Builds a fields table for an object schema.

    Args:
        node (dict): An object schema with `properties`.
        context (Context): Used to link `$ref`s.
        link_extensions (bool): If True, the `extensions` field links to the
            page's Extensions section (default: False).

    Returns:
        list[str]: Markdown lines for the table.
    """
    return [
        "| Field | Type | Required | Description |",
        "| --- | --- | --- | --- |",
        *field_rows(node, context, link_extensions=link_extensions),
        "",
    ]


def item_count(node: dict) -> str:
    """
    Describes an array's `minItems` and `maxItems`.

    Args:
        node (dict): An array schema.

    Returns:
        str: A description such as "exactly 2 items", or "" if unconstrained.
    """
    minimum, maximum = node.get("minItems"), node.get("maxItems")
    if minimum is not None and minimum == maximum:
        return f"exactly {minimum} item{'s' if minimum != 1 else ''}"
    if minimum is not None and maximum is not None:
        return f"{minimum} to {maximum} items"
    if minimum:
        return f"at least {minimum} item{'s' if minimum != 1 else ''}"
    if maximum is not None:
        return f"at most {maximum} item{'s' if maximum != 1 else ''}"
    return ""


def json_block(value: typing.Any, indent: str = "") -> list[str]:
    """
    Formats a value as a fenced JSON code block.

    Args:
        value (typing.Any): The value to show.
        indent (str): A prefix for every line, e.g. to nest in a collapsible
            block (default: "").

    Returns:
        list[str]: Markdown lines.
    """
    body = json.dumps(value, indent=2, ensure_ascii=False).splitlines()
    return [f"{indent}```json", *(f"{indent}{line}" for line in body), f"{indent}```", ""]


def literal(value: typing.Any) -> str:
    """
    Formats a JSON value for display.

    Args:
        value (typing.Any): A `const` or `enum` value.

    Returns:
        str: The value as text; strings unquoted, None as "null".
    """
    return value if isinstance(value, str) else json.dumps(value)


def main() -> int:
    """
    Generates every schema page and index page, and updates or checks the
    schema entries in mkdocs.yml's `nav`.

    Returns:
        int: The exit status: 0 on success; 1 if the schemas or nav markers are
            missing, or if `--check` found the nav out of date.
    """
    parser = argparse.ArgumentParser(description=__doc__.strip().splitlines()[0])
    parser.add_argument(
        "--db-directory",
        type=pathlib.Path,
        default=DB_DIRECTORY,
        help="The moalmanac-db checkout (default: external/db).",
    )
    parser.add_argument(
        "--output-directory",
        type=pathlib.Path,
        default=OUTPUT_DIRECTORY,
        help="Where to write pages (default: docs/database/schemas).",
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
        help="Do not change the config; exit with status 1 if its schema nav is out of date.",
    )
    arguments = parser.parse_args()

    schemas_directory = arguments.db_directory / "schemas"
    if not schemas_directory.is_dir():
        print(
            f"{schemas_directory} not found. Fetch the submodules with "
            "`git submodule update --init`.",
            file=sys.stderr,
        )
        return 1

    commit = db_commit(db_directory=arguments.db_directory)
    loaded = {
        category: {
            path.name: json.loads(path.read_text())
            for path in sorted((schemas_directory / category).glob("*.schema.json"))
        }
        for category in CATEGORIES
    }
    total = 0
    for category, schemas in loaded.items():
        other = next(name for name in CATEGORIES if name != category)
        pages = render_category(
            category=category,
            schemas=schemas,
            other_files=set(loaded[other]),
            commit=commit,
        )

        output = arguments.output_directory / category
        if output.exists():
            shutil.rmtree(output)
        output.mkdir(parents=True)
        for name, lines in pages.items():
            (output / name).write_text("\n".join(lines).rstrip() + "\n")
        total += len(pages)
    print(f"Wrote {total} pages for moalmanac-db {commit[:7] if commit else '(unknown commit)'}.")

    config = arguments.config.read_text()
    try:
        updated = update_nav(config=config, loaded=loaded)
    except ValueError as error:
        print(error, file=sys.stderr)
        return 1
    if updated == config:
        print(f"{arguments.config.name} schema nav is up to date.")
    elif arguments.check:
        print(
            f"{arguments.config.name} schema nav is out of date. Run "
            "`python utils/generate_schema_pages.py` and commit the result.",
            file=sys.stderr,
        )
        return 1
    else:
        arguments.config.write_text(updated)
        print(f"Updated the schema nav in {arguments.config.name}.")
    return 0


def db_commit(db_directory: pathlib.Path) -> str | None:
    """
    Looks up the moalmanac-db commit the pages are generated from.

    Args:
        db_directory (pathlib.Path): The moalmanac-db checkout.

    Returns:
        str | None: The full commit hash, or None if it is not a git checkout.
    """
    result = subprocess.run(
        ["git", "-C", str(db_directory), "rev-parse", "HEAD"],
        capture_output=True,
        text=True,
        check=False,
    )
    return result.stdout.strip() if result.returncode == 0 else None


def nav_entries(loaded: dict[str, dict[str, dict]], indent: str) -> list[str]:
    """
    Renders the schema entries for mkdocs.yml's `nav`.

    Args:
        loaded (dict[str, dict[str, dict]]): Every schema, keyed by category and
            then filename.
        indent (str): The indentation of the entries, matching the markers.

    Returns:
        list[str]: YAML lines: per category, an Overview entry for its index
            page, then one entry per schema in the same order as the index.
    """
    lines = []
    for category, schemas in loaded.items():
        directory = f"database/schemas/{category}"
        lines += [
            f"{indent}- {category.capitalize()}:",
            f"{indent}    - Overview: {directory}/index.md",
        ]
        for filename in sorted(schemas, key=lambda name: schemas[name]["title"]):
            page = filename.removesuffix(".schema.json") + ".md"
            lines.append(f"{indent}    - {yaml_key(schemas[filename]['title'])}: {directory}/{page}")
    return lines


def reference_link(reference: str, context: Context | None) -> str:
    """
    Links a `$ref` to the page and section that documents it.

    Args:
        reference (str): The `$ref`, e.g. "agents.schema.json",
            "genes.schema.json#/$defs/Gene", or "#/$defs/FDA Indication".
        context (Context | None): The page being rendered; None returns code.

    Returns:
        str: A Markdown link, or the reference as code without a context.
    """
    if context is None:
        return code(reference)

    target, _, fragment = reference.partition("#")
    filename = target or context.filename
    page = f"{filename.removesuffix('.schema.json')}.md" if target else ""
    if not fragment.startswith("/$defs/"):
        return f"[{context.titles.get(filename, filename)}]({page})"

    name = fragment.removeprefix("/$defs/")
    section = "fields" if context.roots.get(filename) == name else anchor(name)
    return f"[{name}]({page}#{section})"


def rule_sentence(rule: dict, context: Context) -> str | None:
    """
    Describes a top-level conditional rule in a sentence, when it is simple.

    Handles `if`/`then`/`else` with a property condition, and `oneOf` between
    sets of property constraints.

    Args:
        rule (dict): The rule, e.g. `{"if": ..., "then": ..., "else": ...}`.
        context (Context): Used to link `$ref`s.

    Returns:
        str | None: The sentence, or None if the rule is too complex to describe.
    """
    if set(rule) == {"oneOf"}:
        options = [constraints(option, context) for option in rule["oneOf"]]
        if None in options:
            return None
        return "Exactly one of: " + "; or ".join(options) + "."
    if "if" in rule and set(rule) <= {"if", "then", "else"}:
        then = constraints(rule.get("then", {}), context)
        otherwise = constraints(rule["else"], context) if "else" in rule else ""
        if then is None or otherwise is None or set(rule["if"]) - {"properties", "required"}:
            return None
        sentence = f"When {condition(rule['if'])}: {then}."
        return f"{sentence} Otherwise: {otherwise}." if otherwise else sentence
    return None


def render_category(
    category: str,
    schemas: dict[str, dict],
    other_files: set[str],
    commit: str | None,
) -> dict[str, list[str]]:
    """
    Renders every page for one category, plus its index page.

    Args:
        category (str): "referenced" or "dereferenced".
        schemas (dict[str, dict]): The category's schemas, keyed by filename.
        other_files (set[str]): Schema filenames in the other category, for
            links between the two versions of a schema.
        commit (str | None): The moalmanac-db commit, for source links.

    Returns:
        dict[str, list[str]]: Markdown lines keyed by output filename.
    """
    titles = {filename: schema["title"] for filename, schema in schemas.items()}
    roots = {filename: root_definition(schema) for filename, schema in schemas.items()}
    other = next(name for name in CATEGORIES if name != category)

    pages = {}
    for filename, schema in schemas.items():
        context = Context(filename=filename, titles=titles, roots=roots)
        pages[filename.removesuffix(".schema.json") + ".md"] = render_schema(
            schema=schema,
            category=category,
            context=context,
            source=source_url(category=category, filename=filename, commit=commit),
            counterpart=filename in other_files and other,
        )

    title, introduction = CATEGORIES[category]
    lines = [f"# {title}", "", introduction, ""]
    if commit:
        lines += [
            f"Generated from moalmanac-db at commit [`{commit[:7]}`]"
            f"({DB_REPOSITORY_URL}/tree/{commit}/schemas/{category}).",
            "",
        ]
    lines += ["| Schema | Description |", "| --- | --- |"]
    for filename in sorted(schemas, key=lambda name: titles[name]):
        page = filename.removesuffix(".schema.json") + ".md"
        description = cell(schemas[filename].get("description", ""))
        lines.append(f"| [{titles[filename]}]({page}) | {description} |")
    pages["index.md"] = lines
    return pages


def render_definition(node: dict, context: Context) -> list[str]:
    """
    Renders a `$defs` entry: its description, what it builds on, and its fields.

    Args:
        node (dict): The definition schema.
        context (Context): Used to link `$ref`s.

    Returns:
        list[str]: Markdown lines.
    """
    lines = [cell(node["description"]), ""] if node.get("description") else []
    for part in node.get("allOf", []):
        if set(part) == {"$ref"}:
            lines += [f"Builds on {reference_link(part['$ref'], context)}.", ""]
        elif "properties" in part:
            lines += fields_table(part, context)
        else:
            lines += ["With this additional rule:", "", *json_block(part)]
    if "properties" in node:
        lines += fields_table(node, context)
    elif "allOf" not in node:
        lines += [f"Type: {describe(node, context)}", ""]
    return lines


def render_schema(
    schema: dict,
    category: str,
    context: Context,
    source: str,
    counterpart: str | typing.Literal[False],
) -> list[str]:
    """
    Renders one schema's page.

    Args:
        schema (dict): The JSON Schema.
        category (str): "referenced" or "dereferenced".
        context (Context): Used to link `$ref`s.
        source (str): The schema file's URL on GitHub.
        counterpart (str | typing.Literal[False]): The other category, if it has
            a schema with the same filename, or False.

    Returns:
        list[str]: Markdown lines.
    """
    stem = context.filename.removesuffix(".schema.json")
    links = [f"{category.capitalize()} schema", f"[Source]({source})"]
    if counterpart:
        links.append(f"[{counterpart.capitalize()} version](../{counterpart}/{stem}.md)")
    lines = [f"# {schema['title']}", "", " · ".join(links), ""]
    if schema.get("description"):
        lines += [schema["description"], ""]

    definitions = dict(schema.get("$defs", {}))
    root = context.roots[context.filename]
    main_object = dict(definitions.pop(root)) if root else {}
    if root and main_object.get("description"):
        lines += [main_object["description"], ""]
    if "properties" in schema:
        main_object["properties"] = {**main_object.get("properties", {}), **schema["properties"]}
        main_object["required"] = [*main_object.get("required", []), *schema.get("required", [])]

    if main_object.get("properties"):
        extensions = extension_rows(main_object["properties"].get("extensions", {}), context)
        lines += [
            "## Fields",
            "",
            *fields_table(main_object, context, link_extensions=bool(extensions)),
            *extensions,
        ]

    subtypes, rules = [], []
    for part in schema.get("allOf", []):
        target = part.get("then", {}).get("$ref", "")
        if "if" in part and target.startswith("#/$defs/") and set(part["then"]) == {"$ref"}:
            subtypes.append((target.removeprefix("#/$defs/"), part["if"]))
        else:
            rules.append(part)
    if "if" in schema:
        rules.append({key: schema[key] for key in ("if", "then", "else") if key in schema})
    for key in ("oneOf", "anyOf", "not"):
        if key in schema:
            rules.append({key: schema[key]})

    if subtypes:
        lines += [
            "## Subtypes",
            "",
            "Every record matches exactly one subtype, which adds to the "
            "[fields](#fields) above.",
            "",
            "| Subtype | Applies when | Description |",
            "| --- | --- | --- |",
        ]
        for name, rule in subtypes:
            description = cell(definitions.get(name, {}).get("description", ""))
            lines.append(f"| [{name}](#{anchor(name)}) | {condition(rule)} | {description} |")
        lines.append("")
        for name, _ in subtypes:
            lines += [f"### {name}", "", *render_definition(definitions.pop(name, {}), context)]

    if definitions:
        lines += ["## Definitions", ""]
        for name, definition in definitions.items():
            lines += [f"### {name}", "", *render_definition(definition, context)]

    if rules:
        lines += ["## Additional rules", "", "These rules also apply to every record:", ""]
        for rule in rules:
            sentence = rule_sentence(rule, context)
            lines += [f"- {sentence}", ""] if sentence else json_block(rule)

    lines += ["## JSON Schema", "", '??? note "Full JSON Schema"', ""]
    lines += json_block(schema, indent="    ")
    return lines


def update_nav(config: str, loaded: dict[str, dict[str, dict]]) -> str:
    """
    Replaces the schema entries between the nav markers in the site config.

    Args:
        config (str): The contents of mkdocs.yml.
        loaded (dict[str, dict[str, dict]]): Every schema, keyed by category and
            then filename.

    Raises:
        ValueError: If the begin and end markers are not each found exactly once,
            in order.

    Returns:
        str: The config with the entries between the markers regenerated.
    """
    lines = config.splitlines()
    begins = [i for i, line in enumerate(lines) if line.strip().startswith(NAV_BEGIN)]
    ends = [i for i, line in enumerate(lines) if line.strip().startswith(NAV_END)]
    if len(begins) != 1 or len(ends) != 1 or begins[0] > ends[0]:
        raise ValueError(
            f"Expected one '{NAV_BEGIN}' line followed by one '{NAV_END}' line in "
            "the nav of mkdocs.yml.",
        )
    begin, end = begins[0], ends[0]
    indent = lines[begin][: len(lines[begin]) - len(lines[begin].lstrip())]
    entries = nav_entries(loaded=loaded, indent=indent)
    return "\n".join([*lines[: begin + 1], *entries, *lines[end:]]) + "\n"


def root_definition(schema: dict) -> str | None:
    """
    Finds the `$defs` entry a schema's top-level `$ref` points to.

    Args:
        schema (dict): The JSON Schema.

    Returns:
        str | None: The definition's name, e.g. "Indication", or None.
    """
    reference = schema.get("$ref", "")
    return reference.removeprefix("#/$defs/") if reference.startswith("#/$defs/") else None


def source_url(category: str, filename: str, commit: str | None) -> str:
    """
    Builds the URL of a schema file on GitHub.

    Args:
        category (str): "referenced" or "dereferenced".
        filename (str): The schema's filename.
        commit (str | None): The moalmanac-db commit, or None to link `main`.

    Returns:
        str: The URL.
    """
    return f"{DB_REPOSITORY_URL}/blob/{commit or 'main'}/schemas/{category}/{filename}"


def yaml_key(text: str) -> str:
    """
    Formats a nav title as a YAML key, quoting it only when YAML requires it.

    Args:
        text (str): The title, e.g. "Agent".

    Returns:
        str: The title as is if it is plain words, otherwise double-quoted.
    """
    return text if re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9 ()-]*", text) else json.dumps(text)


if __name__ == "__main__":
    sys.exit(main())
