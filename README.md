# ndtest

ndtest is a high-performance implementation of 2D Kolmogorov–Smirnov test, inspired by the original project of the same name ([syrte/ndtest](https://github.com/syrte/ndtest)). The following optimizations have been implemented to improve the performance:

- **FORTRAN Backend**: The core components have been rewritten in FORTRAN to achieve significant performance improvements. FORTRAN code is seamlessly integrated into Python via `f2py`.
- **Parallelization**: Utilizing `joblib` for parallel processing, the framework now efficiently calculates p-values using bootstrap resampling.


## Installation

Just 

```
pip install git+https://github.com/astro-jingtao/ndtest.git

# or use gitee mirror if the user have trouble with using github
# pip install git+https://gitee.com/the-wind-is-still-like-snow/ndtest.git
```

### Common Errors and Solutions

1. If you find `'gbk' (or other non-UTF-8 encodings) codec can't decode byte ...` in the output, try to set the `PYTHONIOENCODING` environment variable to `utf-8`. This kind of error is usually found with the system with non-UTF-8 default encoding.

2. If you find `error: extension 'maxdist' has Fortran sources but no Fortran compiler found` in the output, try to install a working FORTRAN compiler. It should be not hard to do so on Linux or macOS. A simple way to do that on Windows is `conda install conda-forge::gfortran`, and then set environment variable `F90EXEC` as the path to `gfortran.exe` before running `pip install git+https://github.com/astro-jingtao/ndtest.git`. 

## Performance

The `distutils` backend is recommended for high performance, which requires `setuptools<74` and `python<3.12`.

| Data Points | Time (ms) | NumPy Version | Backend    | OS      | CPU Model                                 |
|-------------|-----------|---------------|------------|---------|-------------------------------------------|
| 10,000      | ~ 210     | 1.24.3        | distutils  | linux   | Intel(R) Xeon(R) Gold 6248 CPU @ 2.50GHz  |
| 10,000      | ~ 277     | 1.26.4        | meson      | linux   | Intel(R) Xeon(R) Gold 6248 CPU @ 2.50GHz  |
| 10,000      | ~ 286     | 2.0.1         | meson      | linux   | Intel(R) Xeon(R) Gold 6248 CPU @ 2.50GHz  |
| 10,000      | ~ 210     | 2.0.1         | distutils  | linux   | Intel(R) Xeon(R) Gold 6248 CPU @ 2.50GHz  |
