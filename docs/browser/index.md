# Browser

The MOAlmanac browser ([moalmanac-browser](https://github.com/vanallenlab/moalmanac-browser)) is the website for searching and reading the [database](../database/index.md), at [moalmanac.org](https://moalmanac.org). It can also be used to [suggest a new entry](https://moalmanac.org/add).

The browser does not read the database directly: it requests records from the [API](../api/index.md) and keeps a local cache of them. Several instances run from the same code, each with its own configuration, including [moalmanac.org](https://moalmanac.org), [ie.moalmanac.org](https://ie.moalmanac.org) and [ca.moalmanac.org](https://ca.moalmanac.org).

To run or deploy the browser yourself, see the [repository's README](https://github.com/vanallenlab/moalmanac-browser#readme).

The database records the browser shows are licensed under CC BY 4.0 and the browser software under GPL v2. See the [Terms of use](../about/terms-of-use.md) and [Citation](../about/citation.md).
