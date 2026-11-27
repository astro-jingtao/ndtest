# TODO

Open work and the decision that each item waits for. Every item names the current state and the intended state.

## Packaging

- Build wheels for Linux, macOS and Windows with [cibuildwheel](https://cibuildwheel.pypa.io/) and attach them to a GitHub release. Current state: `pip install` compiles the Fortran kernel on the installing machine, which therefore needs a Fortran compiler and a C compiler. Intended state: a pushed version tag builds the wheels, the release carries them, and users install without a compiler. The Windows wheel needs no DLL of the toolchain next to the extension: the extension imports `KERNEL32.dll`, the C runtime of Windows and the interpreter DLL only. Verification: `pip download ndtest==<version>` on all three platforms, then importing the installed wheel in a clean environment whose `PATH` holds no compiler.

## Naming

- The name `ndtest` is taken on PyPI by another package ([syrte/ndtest](https://github.com/syrte/ndtest)); this package is installed from its git repository only. Current state: `pip install ndtest` installs the other package, and the first paragraph of the README states the relation between the two. Intended state: either a package on PyPI under a name that is free there, or the documented decision to stay with the git installation; the first changes the distribution name in `pyproject.toml` and `meson.build`, the README and the import name `ndtest`.
