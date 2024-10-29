# ndtest

ndtest is a high-performance implmentation of 2D Kolmogorov–Smirnov test, inspired by the original project of the same name ([syrte/ndtest](https://github.com/syrte/ndtest)). The following optimizations have been implemented to improve the performance:

- **FORTRAN Backend**: The core components have been rewritten in FORTRAN to achieve significant performance improvements. FORTRAN code is seamlessly integrated into Python via `f2py`.
- **Parallelization**: Utilizing `joblib` for parallel processing, the framework now efficiently calculates p-values using bootstrap resampling.
