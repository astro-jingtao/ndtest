# Changelog

## [unreleased]

### Added

- `pyproject.toml` declares the build requirements, the runtime dependencies (`numpy>=1.26`, `scipy>=1.10`, `joblib>=1.2`), the supported Python range (3.9 to 3.13) and a `test` extra. `pip install` now builds in an isolated environment without pre-installing numpy, meson, ninja or `charset_normalizer`.
- The Fortran source ships in the source distribution, so `python -m build` and `pip install` from an sdist work.
- A test suite under `tests/`: the Fortran kernel against a direct evaluation of the definition of the statistic, the analytic and the bootstrap p-value, and the documented usage. Install with `pip install .[test]` and run `pytest`.
- `ruff.toml` configures the linter; `ruff check .` reports no findings.

### Changed

- The build uses the meson-python backend with a `meson.build` of its own; `setup.py` and its call into `f2py -c` are removed. One build path now serves every platform and Python version, and Windows no longer moves a `.libs` directory after the build.
- `nboot` and `n_jobs` of `ks2d2s` are keyword-only arguments.
- `maxdist.f90` declares `D_max` as a one-element array, which is the shape `ksnd.py` passes.

### Fixed

- Installing with pip >= 25.3 failed while preparing the metadata, because `setup.py` imported numpy in the isolated build environment.
- Building failed with `UnicodeDecodeError` when `charset_normalizer` was not installed; the Fortran source is ASCII now.
- Installing on Windows with Python >= 3.12 or setuptools >= 74 failed when moving a `.libs` directory that the meson build does not create.

## 0.3.0 - 2024-10-29

### Added
- Performance in with different backend in README.
- Automatically choose `f2py` backend on linux and macOS. 
- Add the installing of `charset_normalizer` in README.
- Suggest to use `setuptools<=73` for better performance in README.
- Mention the requirement of `ninja` and `meson` for `setuptools>=74` or `python>=3.12` in README.

### Changed
- Do not require `numpy<2`

## 0.2.0 - 2024-10-29

### Added

- Raise an error if the compiling of FORTRAN fails.
- Add Common Errors and Solutions in README:
  - non-UTF-8 encoding.
  - FORTRAN compiler can not be found.
- Support to use on Windows.

## 0.1.0 - 2024-10-29

### Added

- Initial release.