# Changelog

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