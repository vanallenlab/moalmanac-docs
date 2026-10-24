This repository hosts the [Documentation subdomain](https://vanallenlab.github.io/moalmanac-docs/) for [Molecular Oncology Almanac](https://moalmanac.org), built with [Zensical](https://zensical.org). It contains documentation for all of the Molecular Oncology Almanac services.

## Installation

### Download

This repository can be downloaded through GitHub by either using the website or terminal. To download on the website, navigate to the top of this page, click the green `Clone or download` button, and select `Download ZIP` to download this repository in a compressed format. To install using GitHub on terminal, type:

```bash
git clone --recurse-submodules https://github.com/vanallenlab/moalmanac-docs.git
cd moalmanac-docs
```

If you already cloned without `--recurse-submodules`, fetch the submodules with:

```bash
git submodule update --init
```

### Submodules

The documented repositories are included as [git submodules](https://github.blog/open-source/git/working-with-submodules/) under `external/`, each pinned to a specific commit so every build of this site is reproducible:

- `external/db` - [moalmanac-db](https://github.com/vanallenlab/moalmanac-db)
- `external/api` - [moalmanac-api](https://github.com/vanallenlab/moalmanac-api)
- `external/algorithm` - [moalmanac](https://github.com/vanallenlab/moalmanac)
- `external/browser` - [moalmanac-browser](https://github.com/vanallenlab/moalmanac-browser)

Treat these folders as read-only: make changes in each repository itself, then update the pinned commit here. To move a submodule to the latest commit on its default branch:

```bash
git submodule update --remote external/db
```

Then commit the updated submodule (e.g. `git add external/db`) in this repository.

### Python dependencies

This repository uses Python 3.14. We recommend managing your environment wih [Conda-forge](https://conda-forge.org)'s installer [Miniforge](https://conda-forge.org/download/). Run the following from this repository's directory to create a virtual environment and install dependencies with Miniforge:

```bash
conda create -y -n moalmanac-docs python=3.14
conda activate moalmanac-docs
pip install -r requirements.txt
```

Or, if using base Python:

```bash
virtualenv venv
source activate venv/bin/activate
pip install -r requirements.txt
```

## Development

The reference pages and the algorithm pages come from the submodules, so generate them before building or previewing the site:

```bash
python utils/generate_schema_pages.py
python utils/generate_api_pages.py
python utils/copy_algorithm_pages.py
```

- [utils/generate_schema_pages.py](utils/generate_schema_pages.py) reads moalmanac-db's JSON Schemas (`external/db/schemas/`) and writes a page per schema, plus an index page for each group, to `docs/database/schemas/referenced/` and `docs/database/schemas/dereferenced/`.
- [utils/generate_api_pages.py](utils/generate_api_pages.py) reads the API's OpenAPI description (`external/api/docs/openapi.json`) and writes a page per endpoint, an endpoints overview, and a Responses page to `docs/api/reference/`. Records link to the schema pages rather than being described again.
- [utils/copy_algorithm_pages.py](utils/copy_algorithm_pages.py) copies the algorithm's description of inputs and outputs (`external/algorithm/docs/description-of-{inputs,outputs}.md`) to `docs/algorithm/`, dropping their hand-written tables of contents and pointing their links to other files in the algorithm repository to GitHub at the pinned commit.

Those pages are regenerated in full on every run and ignored by git, so edit the scripts (or, for the algorithm pages, the algorithm repository) rather than the pages. Run them again after updating a submodule.

Each script also keeps its part of [mkdocs.yml](mkdocs.yml)'s `nav` up to date, rewriting the lines between its `# BEGIN generated ... nav` and `# END generated ... nav` comments so every generated page appears in the sidebar. Don't edit those lines by hand. If a submodule update adds, removes, or renames a schema or endpoint, the scripts change them; commit that change together with the submodule update. The deploy workflow runs all three scripts with `--check`, which fails the build if the committed `nav` is out of date:

```bash
python utils/generate_schema_pages.py --check
python utils/generate_api_pages.py --check
python utils/copy_algorithm_pages.py --check
```

To preview the site locally, run:

```bash
zensical serve
```

The website will be available at [http://localhost:8000](http://localhost:8000).

If the ports fail to close when shutting down the application, use [utils/listen.sh](utils/listen.sh) to obtain the PID value of the service and then use [utils/kill.sh](utils/kill.sh) to shut down the ports. For example:

```bash
(base) vanallenlab@computer:news$ bash utils/listen.sh 8000
COMMAND   PID    USER   FD   TYPE             DEVICE SIZE/OFF NODE NAME
ruby    19849 vanallenlab   12u  IPv4 0xea464cd74b3ffbe0      0t0  TCP 127.0.0.1:8000 (LISTEN)
(base) vanallenlab@computer:news$ bash utils/kill.sh 19849
```

## Deployment

This site is built and deployed using [GitHub Actions](https://github.com/features/actions). On every push to the `main` branch, the workflow builds the site and publishes it to [GitHub Pages](https://docs.github.com/en/pages).

## Repository structure

- [mkdocs.yml](mkdocs.yml) - site configuration and navigation, which Zensical reads directly
- [docs/](docs/) - the site's pages, assets, and stylesheets
- `external/` - the documented repositories, as submodules (see [Submodules](#submodules))
- [utils/](utils/) - helper scripts, including [generate_schema_pages.py](utils/generate_schema_pages.py) and [generate_api_pages.py](utils/generate_api_pages.py), which generate the database schema and API reference pages, and [copy_algorithm_pages.py](utils/copy_algorithm_pages.py), which copies in the algorithm's input and output descriptions
- [.github/workflows/deploy-docs.yml](.github/workflows/deploy-docs.yml) - generates the schema and API reference pages and copies the algorithm pages (checking their `nav` entries are current), builds the site with `zensical build --strict`, and deploys it to GitHub Pages

## License

This repository is distributed under the [GNU General Public License, Version 2](./LICENSE).
