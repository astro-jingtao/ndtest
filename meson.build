project(
  'ndtest',
  'c',
  'fortran',
  version: '0.3.0',
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

# The numpy headers expose, by default, the C-API version of whichever numpy
# runs the build; the compiled module then refuses older numpy at import. The
# target is pinned to the API of numpy 1.25/1.26 so the runtime floor declared
# in pyproject.toml holds whatever numpy the build environment carries.
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
  install: true,
  subdir: 'ndtest',
)

py.install_sources(
  ['ndtest/__init__.py', 'ndtest/ksnd.py'],
  subdir: 'ndtest',
)
