This repository hosts the [Documentation subdomain](https://vanallenlab.github.io/moalmanac-docs/) for [Molecular Oncology Almanac](https://moalmanac.org), built with [Zensical](https://zensical.org). It contains documentation for all of the Molecular Oncology Almanac services.

**This is in development**.

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

This repository uses Python 3.14. We recommend using a [virtual environment](https://docs.python.org/3/tutorial/venv.html) and running Python with either [Anaconda](https://www.anaconda.com/download/) or [Miniconda](https://conda.io/miniconda.html). 

Run the following from this repository's directory to create a virtual environment and install dependencies with Anaconda or Miniconda:

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

The database schema reference pages are generated from moalmanac-db's JSON Schemas (`external/db/schemas/`), so generate them before building or previewing the site:

```bash
python utils/generate_schema_pages.py
```

This writes a page per schema, plus an index page listing them, to `docs/database/schemas/referenced/` and `docs/database/schemas/dereferenced/`. Those folders are regenerated in full on every run and ignored by git, so edit [utils/generate_schema_pages.py](utils/generate_schema_pages.py) rather than the pages. Run it again after updating `external/db`.

The script also keeps the schema entries in [mkdocs.yml](mkdocs.yml)'s `nav` up to date, rewriting the lines between `# BEGIN generated schema nav` and `# END generated schema nav` so every schema page appears in the sidebar. Don't edit those lines by hand. If a moalmanac-db update adds, removes, or renames a schema, the script changes them; commit that change together with the submodule update. The deploy workflow runs the script with `--check`, which fails the build if the committed `nav` is out of date:

```bash
python utils/generate_schema_pages.py --check
```

To preview the site locally, run:

```bash
zensical serve
```

The website will be available at [http://127.0.0.1:8000](http://127.0.0.1:8000).

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
- [utils/](utils/) - helper scripts, including [generate_schema_pages.py](utils/generate_schema_pages.py), which generates the database schema reference pages
- [.github/workflows/deploy-docs.yml](.github/workflows/deploy-docs.yml) - generates the schema reference pages (checking the schema `nav` is current), builds the site with `zensical build --strict`, and deploys it to GitHub Pages

## License

This repository is distributed under the [GNU GENERAL PUBLIC LICENSE Version 2](./LICENSE).
