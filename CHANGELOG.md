# Changelog

## Unreleased

### Added

- Python 3.15 is supported: `pyproject.toml` declares it, the README lists it and the CI matrix tests it on Linux, macOS and Windows.
- `ks2d2s` takes the keyword argument `backend`, the joblib backend that runs the bootstrap resamples when `n_jobs` is not 1; `None`, the default, leaves the choice to joblib. `backend="threading"` starts no worker processes and is the faster choice for a single call: with `nboot=100` and `n_jobs=2`, 0.27 s against 0.9 s at 10,000 points per sample. The README states the measured times of both backends and why the threads overlap only the sorting and ranking.
- `TODO.md` lists two planned tests: the Kolmogorov-Smirnov test in more than two dimensions and the energy test of raddest.

### Changed

- The analytic p-value takes the correlation of the coordinates from `numpy.corrcoef` instead of `scipy.stats.pearsonr`, which also built the beta distribution for a p-value of the correlation that the approximation does not use. `ks2d2s` with the analytic p-value takes a third of its former time at 1,000 points per sample and about four fifths at 100,000, where the statistic dominates. A sample of one point gives a p-value of `nan` now instead of raising `ValueError`.
- The y coordinates are ranked through one `numpy.argsort` and reach the kernel as 32-bit ranks, the type the kernel takes, instead of through `numpy.unique` and a conversion on the way in. The ranks are the same, and one evaluation of the statistic in one direction takes 4% to 18% less time at 1,000 to 100,000 points per sample.
- `ks2d2s` on two samples of 10,000 points takes about 3.5 ms on an Intel Xeon Gold 6248 with gfortran 8.5, and 45 ms at 100,000 points (5.5 ms and 80 ms in 0.4.0); the performance table of the README states the measurements of this build.
- The function `maxdist_wraper` of `ndtest.ksnd`, which sorts and ranks the points for the kernel, is named `maxdist_wrapper`.

### Fixed

- The bootstrap p-value was a single-precision number (`numpy.float32`), so one third of the resamples came out as 0.33333334; it is a double-precision number now.

## 0.4.0 -- 2026-11-27

### Added

- `pyproject.toml` declares the build requirements, the runtime dependencies (`numpy>=1.26`, `scipy>=1.10`, `joblib>=1.2`), the supported Python range (3.9 to 3.14) and a `test` extra. `pip install` now builds in an isolated environment without pre-installing numpy, meson, ninja or `charset_normalizer`.
- The Fortran source ships in the source distribution, so `python -m build` and `pip install` from an sdist work.
- A test suite under `tests/`: the Fortran kernel against a direct evaluation of the definition of the statistic, the analytic and the bootstrap p-value, and the documented usage. Install with `pip install .[test]` and run `pytest`.
- `ruff.toml` configures the linter; `ruff format --check .` and `ruff check .` report no findings.
- `tools/benchmark_ks2d2s.py` measures the running time of the Fortran kernel and of `ks2d2s`.
- `TODO.md` lists the open items: wheels for the three platforms, the package name on PyPI and the release of 0.4.0.
- A GitHub Actions workflow: `ruff format --check .` and `ruff check .`; the test suite against an isolated `pip install ".[test]"` on Linux, macOS and Windows for Python 3.9 to 3.14; and a check that builds the sdist, builds a wheel from it, installs the wheel and runs the tests.

### Changed

- The build uses the meson-python backend with a `meson.build` of its own; `setup.py` and its call into `f2py -c` are removed. One build path now serves every platform and Python version, and Windows no longer moves a `.libs` directory after the build.
- The Fortran compiler links the extension. On Windows the runtime libraries of the GNU toolchain (`libgfortran`, `libgcc`, `libquadmath`, `libwinpthread`) are linked statically, so the extension imports the C runtime of Windows and the interpreter DLL only, and the toolchain is needed to install only.
- `nboot` and `n_jobs` of `ks2d2s` are keyword-only arguments.
- `ks2d2s` draws its bootstrap resamples from a generator of its own. The keyword argument `rng` takes a seed or a `numpy.random.Generator`, as `numpy.random.default_rng` does; without it the resamples come from a new generator fed by the operating system. `numpy.random.seed` no longer makes the bootstrap repeatable.
- The Fortran kernel visits the points in the order of their x coordinate and keeps the quadrant counts in Fenwick trees over the y ranks, so its running time grows with (n1 + n2) log(n1 + n2) instead of n1 (n1 + n2). `ks2d2s` on two samples of 10,000 points takes about 5.5 ms on an Intel Xeon Gold 6248 with gfortran 8.5, and 80 ms at 100,000 points.
- The Fortran kernel computes the statistic in double precision, with no loss in running time. Coordinates that differ only below single precision are told apart now, and the statistic differs from the one of the single-precision kernel beyond the seventh digit.
- The README states the one requirement left for the installation (a Fortran compiler), shows the usage of `ks2d2s`, replaces the performance table with measurements of the current build, and describes the development setup.
- The package description names what the package provides: a two-dimensional two-sample Kolmogorov-Smirnov test with a Fortran kernel.
- The docstring of `ks2d2s` states that the coordinates are array-likes, that the analytic p-value is an approximation and the bootstrap p-value an estimate, and its typos are corrected.
- `maxdist.f90` declares `D_max` as a one-element array, which is the shape `ksnd.py` passes.

### Fixed

- The statistic of data with duplicate x coordinates in the first sample was wrong: a point saw only the points before it in the sorted order, not the points that share its x coordinate. The kernel now counts the whole group, so the result agrees with the definition of the statistic and is the same on every platform: before, it followed the order of the tied points, which the sort sets differently on x86-64 and arm64.
- Installing with pip >= 25.3 failed while preparing the metadata, because `setup.py` imported numpy in the isolated build environment.
- Building failed with `UnicodeDecodeError` when `charset_normalizer` was not installed; the Fortran source is ASCII now.
- Installing on Windows with Python >= 3.12 or setuptools >= 74 failed when moving a `.libs` directory that the meson build does not create.
- The extension built on Windows imported DLLs of the GNU toolchain (`libgfortran`, `libquadmath`, `libwinpthread`), so `import ndtest` failed with `DLL load failed` wherever the toolchain was not on `PATH`, as on the GitHub runner image of 2026-11-23. The extension imports the C runtime of Windows and the interpreter DLL only now.

## 0.3.0 -- 2024-10-29

### Added
- Performance in with different backend in README.
- Automatically choose `f2py` backend on linux and macOS. 
- Add the installing of `charset_normalizer` in README.
- Suggest to use `setuptools<=73` for better performance in README.
- Mention the requirement of `ninja` and `meson` for `setuptools>=74` or `python>=3.12` in README.

### Changed
- Do not require `numpy<2`

## 0.2.0 -- 2024-10-29

### Added

- Raise an error if the compiling of FORTRAN fails.
- Add Common Errors and Solutions in README:
  - non-UTF-8 encoding.
  - FORTRAN compiler can not be found.
- Support to use on Windows.

## 0.1.0 -- 2024-10-29

### Added

- Initial release.