"""
Copies the algorithm's description of inputs and outputs into the site.

Reads external/algorithm/docs/description-of-{inputs,outputs}.md and writes them
to docs/algorithm/, adapted for the site: their hand-written tables of contents
are dropped (the site builds its own), headings are adjusted so each page has a
single title, and links to other files in the algorithm repository point to
those files on GitHub at the pinned commit. The copies are ignored by git, so run
this before `zensical build` or `zensical serve`:

    python utils/copy_algorithm_pages.py

It also rewrites the algorithm entries in mkdocs.yml's `nav`, between the
"# BEGIN generated algorithm nav" and "# END generated algorithm nav" comments.
With `--check`, mkdocs.yml is left unchanged and the script exits with status 1
if its algorithm entries are out of date; CI runs it this way.
"""

import argparse
import pathlib
import posixpath
import re
import sys

import generate_schema_pages

REPOSITORY_ROOT = pathlib.Path(__file__).resolve().parents[1]
ALGORITHM_DIRECTORY = REPOSITORY_ROOT / "external" / "algorithm"
OUTPUT_DIRECTORY = REPOSITORY_ROOT / "docs" / "algorithm"
CONFIG_PATH = REPOSITORY_ROOT / "mkdocs.yml"
NAV_BEGIN = "# BEGIN generated algorithm nav"
NAV_END = "# END generated algorithm nav"
ALGORITHM_REPOSITORY_URL = "https://github.com/vanallenlab/moalmanac"

# Pages to copy, as (file in the algorithm's docs/ folder, nav title).
PAGES = [
    ("description-of-inputs.md", "Description of inputs"),
    ("description-of-outputs.md", "Description of outputs"),
]

FENCE = re.compile(r"^\s*(```|~~~)")
HEADING = re.compile(r"^(#{1,6})\s+(.*?)\s*$")
LINK = re.compile(r"\]\(([^)\s]+)\)")
TABLE_OF_CONTENTS_ENTRY = re.compile(r"^\s*[*-]\s+\[[^\]]*\]\(#[^)]*\)\s*$")


def adapt(text: str, commit: str | None, algorithm_directory: pathlib.Path) -> tuple[str, list[str]]:
    """
    Adapts one of the algorithm's docs pages for the site.

    Args:
        text (str): The page as written in the algorithm repository.
        commit (str | None): The algorithm commit to link files at, or None to
            link to `main`.
        algorithm_directory (pathlib.Path): The algorithm checkout, used to check
            that linked files exist.

    Returns:
        tuple[str, list[str]]: The adapted page, and the repository paths it links
            to that do not exist in the checkout.
    """
    lines = text.splitlines()
    demote = sum(1 for line in outside_fences(lines) if line.startswith("# ")) > 1

    output = []
    missing = []
    in_fence = False
    in_contents = False
    title_seen = False
    for line in lines:
        if FENCE.match(line):
            in_fence = not in_fence
            in_contents = False
            output.append(line)
            continue
        heading = None if in_fence else HEADING.match(line)
        if heading:
            in_contents = heading.group(2).lower() == "table of contents"
            if in_contents:
                continue
            if not title_seen:
                title_seen = True
            elif demote:
                line = f"#{heading.group(1)} {heading.group(2)}"
        elif in_contents and TABLE_OF_CONTENTS_ENTRY.match(line):
            continue
        if not in_fence:
            line = LINK.sub(
                lambda match: f"]({rewrite_link(match.group(1), commit, algorithm_directory, missing)})",
                line,
            )
        output.append(line)

    adapted = re.sub(r"\n{3,}", "\n\n", "\n".join(output)).strip() + "\n"
    return adapted, missing


def main() -> int:
    """
    Copies every algorithm page, and updates or checks the algorithm entries in
    mkdocs.yml's `nav`.

    Returns:
        int: The exit status: 0 on success; 1 if the algorithm docs or nav
            markers are missing, or if `--check` found the nav out of date.
    """
    parser = argparse.ArgumentParser(description=__doc__.strip().splitlines()[0])
    parser.add_argument(
        "--algorithm-directory",
        type=pathlib.Path,
        default=ALGORITHM_DIRECTORY,
        help="The moalmanac (algorithm) checkout (default: external/algorithm).",
    )
    parser.add_argument(
        "--output-directory",
        type=pathlib.Path,
        default=OUTPUT_DIRECTORY,
        help="Where to write pages (default: docs/algorithm).",
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
        help="Do not change the config; exit with status 1 if its algorithm nav is out of date.",
    )
    arguments = parser.parse_args()

    docs_directory = arguments.algorithm_directory / "docs"
    sources = [docs_directory / filename for filename, _ in PAGES]
    absent = [source for source in sources if not source.is_file()]
    if absent:
        print(
            f"{', '.join(str(source) for source in absent)} not found. Fetch the "
            "submodules with `git submodule update --init`.",
            file=sys.stderr,
        )
        return 1

    commit = generate_schema_pages.db_commit(db_directory=arguments.algorithm_directory)
    arguments.output_directory.mkdir(parents=True, exist_ok=True)
    for source in sources:
        adapted, missing = adapt(
            text=source.read_text(),
            commit=commit,
            algorithm_directory=arguments.algorithm_directory,
        )
        (arguments.output_directory / source.name).write_text(
            with_source_note(text=adapted, filename=source.name, commit=commit),
        )
        for path in sorted(set(missing)):
            print(f"Warning: {source.name} links to {path}, which is not in the algorithm repository.", file=sys.stderr)
    print(f"Wrote {len(sources)} pages for moalmanac {commit[:7] if commit else '(unknown commit)'}.")

    config = arguments.config.read_text()
    try:
        updated = generate_schema_pages.replace_between_markers(
            config=config,
            begin_marker=NAV_BEGIN,
            end_marker=NAV_END,
            render=nav_entries,
        )
    except ValueError as error:
        print(error, file=sys.stderr)
        return 1
    if updated == config:
        print(f"{arguments.config.name} algorithm nav is up to date.")
    elif arguments.check:
        print(
            f"{arguments.config.name} algorithm nav is out of date. Run "
            "`python utils/copy_algorithm_pages.py` and commit the result.",
            file=sys.stderr,
        )
        return 1
    else:
        arguments.config.write_text(updated)
        print(f"Updated the algorithm nav in {arguments.config.name}.")
    return 0


def nav_entries(indent: str) -> list[str]:
    """
    Renders the algorithm entries for mkdocs.yml's `nav`.

    Args:
        indent (str): The indentation of the marker comments.

    Returns:
        list[str]: One nav line per copied page.
    """
    return [f"{indent}- {title}: algorithm/{filename}" for filename, title in PAGES]


def outside_fences(lines: list[str]) -> list[str]:
    """
    Lists the lines of a Markdown page that are not inside a fenced code block.

    Args:
        lines (list[str]): The page's lines.

    Returns:
        list[str]: The lines outside code fences, fence lines excluded.
    """
    kept = []
    in_fence = False
    for line in lines:
        if FENCE.match(line):
            in_fence = not in_fence
        elif not in_fence:
            kept.append(line)
    return kept


def rewrite_link(
    target: str,
    commit: str | None,
    algorithm_directory: pathlib.Path,
    missing: list[str],
) -> str:
    """
    Points a link in an algorithm docs page somewhere that works on the site.

    Links to the other copied pages stay relative; links to other files in the
    algorithm repository go to that file on GitHub. Absolute URLs and in-page
    anchors are left as they are.

    Args:
        target (str): The link target as written, relative to the algorithm's
            docs/ folder, or starting with "/" for the repository root.
        commit (str | None): The algorithm commit to link files at, or None to
            link to `main`.
        algorithm_directory (pathlib.Path): The algorithm checkout.
        missing (list[str]): Collects repository paths that do not exist.

    Returns:
        str: The new link target.
    """
    if re.match(r"^[a-z][a-z0-9+.-]*:", target) or target.startswith("#"):
        return target
    path, _, fragment = target.partition("#")
    if path.startswith("/"):
        resolved = posixpath.normpath(path.lstrip("/") or ".")
    else:
        resolved = posixpath.normpath(posixpath.join("docs", path))
    suffix = f"#{fragment}" if fragment else ""

    copied = {f"docs/{filename}" for filename, _ in PAGES}
    if resolved in copied:
        return posixpath.basename(resolved) + suffix

    local = algorithm_directory / resolved
    if not local.exists():
        missing.append(resolved)
    kind = "tree" if local.is_dir() or resolved == "." else "blob"
    reference = commit or "main"
    location = "" if resolved == "." else f"/{resolved}"
    return f"{ALGORITHM_REPOSITORY_URL}/{kind}/{reference}{location}{suffix}"


def with_source_note(text: str, filename: str, commit: str | None) -> str:
    """
    Adds a line under the page title saying where the page was copied from.

    Args:
        text (str): The adapted page.
        filename (str): The page's file name in the algorithm's docs/ folder.
        commit (str | None): The algorithm commit the page was copied from.

    Returns:
        str: The page with the note after its first line.
    """
    if not commit:
        return text
    title, _, rest = text.partition("\n")
    note = (
        f"Copied from moalmanac at commit [`{commit[:7]}`]"
        f"({ALGORITHM_REPOSITORY_URL}/blob/{commit}/docs/{filename})."
    )
    return f"{title}\n\n{note}\n\n{rest.lstrip()}"


if __name__ == "__main__":
    sys.exit(main())
