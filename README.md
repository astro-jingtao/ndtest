# ndtest

ndtest is a high-performance implementation of 2D Kolmogorov–Smirnov test, inspired by the original project of the same name ([syrte/ndtest](https://github.com/syrte/ndtest)). The following optimizations have been implemented to improve the performance:

- **FORTRAN Backend**: The core components have been rewritten in FORTRAN to achieve significant performance improvements. FORTRAN code is seamlessly integrated into Python via `f2py`.
- **Parallelization**: Utilizing `joblib` for parallel processing, the framework now efficiently calculates p-values using bootstrap resampling.


## Installation

Make sure `charset_normalizer` have been installed, which is used to determine correct encoding of FORTRAN code.

```
pip install charset_normalizer
```

The `setuptools<=73` is recommended for better performance, but `setuptools>73` should also work. See [Performance](#Performance) for details.
```
pip install setuptools==73
```

If you use `setuptools>=74` or `python>=3.12` (not recommended, see [Performance](#Performance) for details), `ninja` and `meson` are needed.

```
pip install ninja meson
```

Then

```
pip install git+https://github.com/astro-jingtao/ndtest.git

# or use gitee mirror if the user have trouble with using github
# pip install git+https://gitee.com/the-wind-is-still-like-snow/ndtest.git
```

### Common Errors and Solutions

1. If you find `'gbk' (or other non-UTF-8 encodings) codec can't decode byte ...` in the output. 
   - Make sure you have `charset_normalizer` package installed.
   - Try to set the `PYTHONIOENCODING` environment variable to `utf-8`. 

2. If you find `error: extension 'maxdist' has Fortran sources but no Fortran compiler found` in the output, try to install a working FORTRAN compiler. It should be not hard to do so on Linux or macOS. A simple way to do that on Windows is `conda install conda-forge::gfortran`, and then set environment variable `F90EXEC` as the path to `gfortran.exe` before running `pip install git+https://github.com/astro-jingtao/ndtest.git`. 

## Performance
<a id="Performance"></a>

The `distutils` backend is recommended for high performance, which requires `setuptools<74` and `python<3.12`.

| Data Points | Time (ms) | NumPy Version | Backend    | OS      | CPU Model                                 |
|-------------|-----------|---------------|------------|---------|-------------------------------------------|
| 10,000      | ~ 210     | 1.24.3        | distutils  | linux   | Intel(R) Xeon(R) Gold 6248 CPU @ 2.50GHz  |
| 10,000      | ~ 277     | 1.26.4        | meson      | linux   | Intel(R) Xeon(R) Gold 6248 CPU @ 2.50GHz  |
| 10,000      | ~ 286     | 2.0.1         | meson      | linux   | Intel(R) Xeon(R) Gold 6248 CPU @ 2.50GHz  |
| 10,000      | ~ 210     | 2.0.1         | distutils  | linux   | Intel(R) Xeon(R) Gold 6248 CPU @ 2.50GHz  |
