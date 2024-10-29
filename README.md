# ndtest

ndtest is a high-performance implementation of 2D Kolmogorov–Smirnov test, inspired by the original project of the same name ([syrte/ndtest](https://github.com/syrte/ndtest)). The following optimizations have been implemented to improve the performance:

- **FORTRAN Backend**: The core components have been rewritten in FORTRAN to achieve significant performance improvements. FORTRAN code is seamlessly integrated into Python via `f2py`.
- **Parallelization**: Utilizing `joblib` for parallel processing, the framework now efficiently calculates p-values using bootstrap resampling.


## Installation

Just 

```
pip install git+https://github.com/astro-jingtao/ndtest.git

# or use gitee mirror if the user have trouble with using github
# pip install git+https://gitee.com/the-wind-is-still-like-snow/ndtest
```

### Common Errors and Solutions

1. If you find `'gbk' (or other non-UTF-8 encodings) codec can't decode byte ...` in the output, try to set the `PYTHONIOENCODING` environment variable to `utf-8`. This kind of error is usually found with the system with non-UTF-8 default encoding.

2. If you find `error: extension 'maxdist' has Fortran sources but no Fortran compiler found` in the output, try to install a working FORTRAN compiler. It should be not hard to do so on Linux or macOS. A simple way to do that on Windows is `conda install conda-forge::gfortran`, and then set environment variable `F90EXEC` as the path to `gfortran.exe` before running `pip install git+https://github.com/astro-jingtao/ndtest.git`. 