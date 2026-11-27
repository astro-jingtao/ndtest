# ndtest

ndtest is a high-performance implementation of 2D Kolmogorov–Smirnov test, inspired by the original project of the same name ([syrte/ndtest](https://github.com/syrte/ndtest)). The following optimizations have been implemented to improve the performance:

- **FORTRAN Backend**: The core components have been rewritten in FORTRAN to achieve significant performance improvements. FORTRAN code is seamlessly integrated into Python via `f2py`.
- **Parallelization**: Utilizing `joblib` for parallel processing, the framework now efficiently calculates p-values using bootstrap resampling.

## Usage

```python
import numpy as np
from ndtest.ksnd import ks2d2s

rng = np.random.default_rng(0)
x1, y1 = rng.normal(size=(2, 1000))
x2, y2 = rng.normal(size=(2, 1000))
D, p = ks2d2s(x1, y1, x2, y2)
```

`ks2d2s` takes the coordinates of two samples and returns the KS statistic `D` and the two-tailed p-value `p`. Small p-values mean that the two samples are significantly different. The coordinates are one-dimensional array-likes of equal length within each sample, and the two samples may have different sizes.

By default (`nboot=None`) the p-value is an analytic approximation. With `nboot=N`, `N` bootstrap resamples of the pooled sample estimate the p-value instead, and `n_jobs` sets the number of parallel jobs (`-1` uses all CPUs). Both are keyword arguments.

## Installation

The Fortran kernel is compiled when the package is installed, so a Fortran compiler must be on `PATH`. One way to provide it is `gfortran` from a system package manager (`sudo apt install gfortran` on Debian and Ubuntu, `brew install gfortran` on macOS). Everything else that the build needs, and the runtime dependencies `numpy`, `scipy` and `joblib`, are installed by pip.

```
pip install git+https://github.com/astro-jingtao/ndtest.git

# or use gitee mirror if the user have trouble with using github
# pip install git+https://gitee.com/the-wind-is-still-like-snow/ndtest.git
```

Python 3.9 to 3.13 are supported. If the installation stops with `ERROR: Unknown compiler(s): [['gfortran'], ['flang-new'], ...]`, no Fortran compiler was found.

### Windows

On Windows a [MinGW-w64](https://www.mingw-w64.org/) toolchain provides both the C and the Fortran compiler that the build needs, for example the `mingw` package of [Chocolatey](https://chocolatey.org/) (`choco install mingw`), whose `bin` directory the package adds to `PATH` for new shells. The toolchain is needed to install only: its runtime libraries are linked into the extension, so `ndtest` imports without the toolchain on `PATH`.

## Performance

`tools/benchmark_ks2d2s.py` times one call of the Fortran kernel and one call of `ks2d2s` with its analytic p-value, on two samples of standard normal points each (the second one with y = x + noise). The times below are the minimum of 7 batches of 2 calls, measured on an Intel Xeon Gold 6248 CPU @ 2.50GHz with gfortran 8.5.0, Python 3.9 and numpy 1.26.4.

| Points per sample | Fortran kernel | `ks2d2s` with analytic p-value |
|-------------------|----------------|-------------------------------|
| 1,000             | 0.9 ms         | 3.6 ms                        |
| 5,000             | 20 ms          | 43 ms                         |
| 10,000            | 79 ms          | 163 ms                        |
| 20,000            | 327 ms         | 699 ms                        |

The kernel compares every point of the first sample with all points, so its running time grows with the square of the sample size. `ks2d2s` evaluates the kernel once per direction and averages the two statistics. A bootstrap p-value evaluates the statistic once per resample: with `nboot=100` and 10,000 points per sample, the kernel runs 200 times for about 16 s in total, spread over `n_jobs` processes.

To measure on your machine, install the package and run `python tools/benchmark_ks2d2s.py --n 10000`.

## Development

```
git clone https://github.com/astro-jingtao/ndtest.git
cd ndtest
pip install meson-python numpy ninja
pip install --no-build-isolation -e .[test]
pytest
```

An editable install keeps the build tools in the environment itself and is therefore installed without build isolation: the package rebuilds the Fortran kernel at the next import after a source changed. The build tools must be on `PATH` at that import, which an activated environment provides.

The sources are formatted and linted with ruff; `ruff format --check .` and `ruff check .` report nothing. The version of the package is declared in `meson.build`. `python -m build` creates the source distribution and the wheel from a git checkout.
