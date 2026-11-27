project(
  'ndtest',
  'c',
  'fortran',
  version: '0.4.0',
  meson_version: '>=1.1.0',
  default_options: [
    'buildtype=release',
    'warning_level=1',
  ],
)

py = import('python').find_installation(pure: false)

fc = meson.get_compiler('fortran')

# The numpy include directories are resolved at configure time from the
# interpreter that runs the build, so an isolated build sees the numpy of its
# own build environment.
incdir_numpy = run_command(
  py, ['-c', 'import numpy; print(numpy.get_include())'],
  check: true,
).stdout().strip()
incdir_f2py = run_command(
  py, ['-c', 'import numpy.f2py; print(numpy.f2py.get_include())'],
  check: true,
).stdout().strip()
inc_numpy = include_directories(incdir_numpy)
inc_f2py = include_directories(incdir_f2py)

# f2py writes the C module and the Fortran wrappers of the extension; the
# Fortran wrapper file exists even when it is empty.
maxdist_wrappers = custom_target(
  'maxdist-wrappers',
  input: 'ndtest/maxdist.f90',
  output: ['maxdistmodule.c', 'maxdist-f2pywrappers.f'],
  command: [
    py, '-m', 'numpy.f2py', '@INPUT@',
    '-m', 'maxdist',
    '--build-dir', '@OUTDIR@',
  ],
)

quadmath_dep = fc.find_library('quadmath', required: false)

# gfortran does not unroll loops at -O3 by default; unrolling the counting
# loops of the kernel cuts its running time by more than a quarter. The flag
# is kept only where the compiler accepts it.
fortran_args = fc.get_supported_arguments('-funroll-loops')

# The Fortran compiler links the extension: the runtime of the kernel is
# libgfortran, which the gfortran driver adds and controls.
# On Windows the runtime libraries of the GNU toolchain (libgfortran, libgcc,
# libquadmath, libwinpthread) are linked statically: `-static` makes the linker
# take the static archives of the toolchain instead of the import libraries of
# its DLLs, so the import needs no directory of the toolchain on PATH.
fortran_link_args = []
if host_machine.system() == 'windows'
  fortran_link_args += fc.get_supported_link_arguments(['-static'])
endif

# The numpy headers expose, by default, a C-API version that each numpy
# release sets for downstream packages (numpy 2.0: 1.19, numpy 2.5: 1.25) and
# that rises over time; a module compiled for a newer API refuses older numpy
# at import. The target is pinned to the API of numpy 1.25 so the runtime
# floor declared in pyproject.toml holds whatever numpy the build environment
# carries. The pin sets no upper bound: numpy accepts modules compiled for an
# older API.
numpy_api_target = ['-DNPY_TARGET_VERSION=NPY_1_25_API_VERSION']

py.extension_module(
  'maxdist',
  [
    'ndtest/maxdist.f90',
    maxdist_wrappers,
    incdir_f2py / 'fortranobject.c',
  ],
  include_directories: [inc_numpy, inc_f2py],
  dependencies: [py.dependency(), quadmath_dep],
  c_args: numpy_api_target,
  fortran_args: fortran_args,
  link_args: fortran_link_args,
  link_language: 'fortran',
  install: true,
  subdir: 'ndtest',
)

py.install_sources(
  ['ndtest/__init__.py', 'ndtest/ksnd.py'],
  subdir: 'ndtest',
)
