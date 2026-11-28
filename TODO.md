# TODO

Open work and the decision that each item waits for. Every item names the current state and the intended state.

## Packaging

- Build wheels for Linux, macOS and Windows with [cibuildwheel](https://cibuildwheel.pypa.io/) and attach them to a GitHub release. Current state: `pip install` compiles the Fortran kernel on the installing machine, which therefore needs a Fortran compiler and a C compiler. Intended state: a pushed version tag builds the wheels, the release carries them, and users install without a compiler. The Windows wheel needs no DLL of the toolchain next to the extension: the extension imports `KERNEL32.dll`, the C runtime of Windows and the interpreter DLL only. Verification: `pip download ndtest==<version>` on all three platforms, then importing the installed wheel in a clean environment whose `PATH` holds no compiler.

## Naming

- Publish under a name that is free on PyPI, or decide to stay with the git installation. Current state: PyPI lists no project named `ndtest` (checked 2026-11-27: the JSON API and the simple index answer 404 and `pip index versions ndtest` finds nothing), and whether the name can be registered is not verified; [syrte/ndtest](https://github.com/syrte/ndtest), the project of the same name, is installed from git only, and the first paragraph of the README states the relation between the two. Intended state: either a package on PyPI under a free name, or the documented decision to stay with the git installation; the first changes the distribution name in `pyproject.toml` and `meson.build` and the README, and the import name `ndtest` when the name differs from it.

## Release

- Publish 0.4.0. Current state: `meson.build` declares the version 0.4.0 and the CHANGELOG lists the changes under `0.4.0 -- 2026-11-27`, the day the work on the version was completed; no tag exists and nothing is published. Intended state: the tag `v0.4.0` is pushed and the GitHub release is created from the tag with the CHANGELOG section as its text. Verification: the CI run of the pushed commit is green on every platform and Python version; `pip install git+https://github.com/astro-jingtao/ndtest.git@v0.4.0` installs, and `python -c "from importlib.metadata import version; print(version('ndtest'))"` prints 0.4.0.
