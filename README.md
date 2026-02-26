# Molecular Oncology Almanac Documentation
This repository hosts the [Documentation subdomain]() for [Molecular Oncology Almanac](https://dev.moalmanac.org), built with [MkDocs](https://www.mkdocs.org) and [Material for MkDocs](https://squidfunk.github.io/mkdocs-material/). It contains documentation for all of the Molecular Oncology Almanac services.

**This is in development**.

## Installation
### Download
This repository can be downloaded through GitHub by either using the website or terminal. To download on the website, navigate to the top of this page, click the green `Clone or download` button, and select `Download ZIP` to download this repository in a compressed format. To install using GitHub on terminal, type:

```bash
git clone https://github.com/vanallenlab/moalmanac-docs.git
cd moalmanac-docs
```

### Python dependencies
This repository uses Python 3.12. We recommend using a [virtual environment](https://docs.python.org/3/tutorial/venv.html) and running Python with either [Anaconda](https://www.anaconda.com/download/) or [Miniconda](https://conda.io/miniconda.html). 

Run the following from this repository's directory to create a virtual environment and install dependencies with Anaconda or Miniconda:
```bash
conda create -y -n moalmanac-docs python=3.12
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
To preview the site locally, run:
```bash
mkdocs serve
```
The website will be available at [http://127.0.0.1:8000](http://127.0.0.1:8000).

If the ports fail to close when shutting down the application, use [utils/listen.sh](utils/listen.sh) to obtain the PID value of the service and then use [utils/kill.sh](utils/kill.sh) to shut down the ports. For example:
```bash
(base) vanallenlab@computer:news$ bash utils/listen.sh 8000
COMMAND   PID    USER   FD   TYPE             DEVICE SIZE/OFF NODE NAME
ruby    19849 vanallenlab   12u  IPv4 0xea464cd74b3ffbe0      0t0  TCP 127.0.0.1:8000 (LISTEN)
(base) vanallenlab@computer:news$ bash utils/kill.sh 19849
```

# Deployment
This site is built and deployed using [GitHub Actions](https://github.com/features/actions). On every push to the `main` branch, the workflow builds the site and publishes it to [GitHub Pages](https://docs.github.com/en/pages).

# Repository structure
TO DO

# License
This repository is distributed under the [GNU GENERAL PUBLIC LICENSE Version 2](./LICENSE).
