# CLAUDE.md

Guide for an agent working in this repository. What holds for humans as well is in `@README.md`: usage, installation, performance and the development setup. Machine-specific notes live in `CLAUDE.local.md`, which is not tracked.

## Layout

- `ndtest/maxdist.f90`: the Fortran kernel. `maxdist` returns the largest difference between the two empirical distribution functions with the points of the first sample as origins; `quadct` turns the counts of one origin into the four quadrant fractions.
- `ndtest/ksnd.py`: the Python API. `ks2d2s` is the public function; `avgmaxdist` averages the two directions; `maxdist_wraper` sorts, ranks and calls the kernel.
- `tests/test_ksnd.py`: the test suite. `reference_maxdist` in it evaluates the definition of the statistic without sorting.
- `tools/benchmark_ks2d2s.py`: the timing behind the table of the README.
- `meson.build`: the f2py build; the version of the package is declared here.
- `TODO.md`, `CHANGELOG.md`: open items, and the changes since the last release under `## [unreleased]`.

## Build and verification

- The kernel is compiled when the package is installed. After a change to the kernel, to `ndtest/ksnd.py` or to the build files, run `pytest` from the repository root in an environment with an editable install of the package (see the development setup in the README). Run `pytest`, not `python -m pytest`: the latter puts the checkout first on `sys.path`, where the package has no compiled extension. An editable install rebuilds the kernel at the next import after a source change; `meson` and `ninja` must be on `PATH` then.
- The lint gate is `ruff format --check .` and `ruff check .` with ruff 0.17.4, the version CI pins; the rules are in `ruff.toml`.
- Before a push, run the tests on the oldest and the newest supported Python with the numpy versions available there; the CI matrix adds the platforms.

## Invariants of the kernel

- The statistic does not depend on the order of the points: a point of the first sample sees every point that shares its x coordinate. `test_tied_coordinates_do_not_depend_on_the_order_of_the_points` holds this; a kernel change keeps it green.
- `TestExactValues` pins the outputs of the kernel with `==`. The kernel counts in integers and divides in IEEE double precision with a fixed order of operations, so every platform gives the same bits. A change of the order of operations changes the pinned values: re-pin them from a measurement of the new kernel after it agrees with `reference_maxdist` to a relative 1e-12, never from a calculation.
- A new kernel algorithm is compared bit for bit with the previous one on tied and untied inputs in both directions, and timed with `tools/benchmark_ks2d2s.py`. The table of the README is then re-measured with the tool, which states its environment.
- The kernel receives each sample in the order of its x coordinate, with 1-based dense y ranks over both samples. `maxdist_wraper` does the sorting and the ranking and takes numpy arrays only; `ks2d2s` converts its input with `numpy.asarray`.

## Public API

- `ks2d2s(x1, y1, x2, y2, *, nboot=None, n_jobs=1, rng=None)` is the only public entry point. raddest, a repository of the same owner, imports it, so the positional coordinates and the keyword-only options stay as they are.
- The bootstrap draws its resamples from `numpy.random.default_rng(rng)`, never from the global `numpy.random` state.

## Conventions

- Conventional commits in English. The CHANGELOG describes the change from the last release for a user of the package.
- numpy-style docstrings, pytest class-based tests, absolute imports.
- The numpy C-API target is pinned in `meson.build` (`NPY_TARGET_VERSION=NPY_1_25_API_VERSION`). It is the lowest numpy the compiled module accepts, so it stays at or below the `numpy>=` floor of `pyproject.toml`; it sets no upper bound.
