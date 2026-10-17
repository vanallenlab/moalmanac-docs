---
title: Algorithm release 0.8.2
date: 2025-06-25
categories:
- Algorithm
- Release
slug: 2025-06-25-algorithm-release
---

This release utilizes the [v.2025-02-07](https://github.com/vanallenlab/moalmanac-db/releases) release of the underlying MOAlmanac database. The codebase now supports Python 3.13 with no warnings produced, although we will continue officially using 3.12 for the time being.

<!-- more -->

[View on GitHub](https://github.com/vanallenlab/moalmanac/releases/tag/0.8.2)

Additions:

- [snfpy](https://github.com/rmarkello/snfpy) was removed as a dependency from the repository, with the relevant module imported with proper attribution. See [Pull Request #42](https://github.com/vanallenlab/moalmanac/pull/42) for more information.

Revisions:

- Several dependencies were updated to their latest versions, notably:
  - matplotlib: 3.8.3 > 3.10.0
  - numpy: 1.26.4 > 2.3.0
  - requests: 2.31.0 > 2.32.4
  - scikit-learn: 1.4.2 > 1.7.0
  - scipy: 1.13.0 > 1.16.0
- Unit tests checking precise float values were modified to use assertAlmostEqual to 10 places.
