import os
import numpy
import sys
import setuptools
from setuptools import Extension, find_packages, setup
from setuptools.command.build_ext import build_ext
import setuptools.version


class f2py_Extension(Extension):

    def __init__(self, name, sourcedirs):
        Extension.__init__(self, name, sources=[])
        self.sourcedirs = [
            os.path.abspath(sourcedir) for sourcedir in sourcedirs
        ]
        self.dirs = sourcedirs


class f2py_Build(build_ext):

    def run(self):
        for ext in self.extensions:
            self.build_extension(ext)

    def build_extension(self, ext):

        # the build directory
        build_lib = os.path.abspath(self.build_lib)

        # compile
        for to_compile in ext.sourcedirs:
            module_name = os.path.split(to_compile)[1].split('.')[0]
            if os.name == 'posix':  # if Linux or macOS

                if (sys.version_info >= (3, 12)) or (setuptools.__version__ >= '74'):
                    # for python version https://numpy.org/doc/stable/f2py/usage.html
                    # for setuptools version https://github.com/numpy/numpy/issues/27405
                    if numpy.__version__ < '1.26':
                        raise ValueError("Only numpy>=1.26 support --backend meson, which is required by your python (>=3.12) or setuptools (>=74) version")
                    cmd_backend = '--backend meson'
                else:
                    cmd_backend = ''

                command = f'cd {build_lib}/{ext.name};python -m numpy.f2py -c {to_compile} -m {module_name} --f90flags=-O3 {cmd_backend}'
            elif os.name == 'nt':  # if Windows
                # try to find gfortran
                gfortran_path = os.getenv('F90EXEC')
                cmd_f90exec = '' if gfortran_path is None else f'--f90exec={gfortran_path}'

                # copy libs, see https://stackoverflow.com/questions/58466447/using-f2py-get-importerror-dll-load-failed-the-specified-module-could-not-be-f
                cmd_copy_libs = f'mv {build_lib}/{ext.name}/{module_name}/.libs/* {build_lib}/{ext.name}'
                # cmd_copy_libs = ''

                # use powershell
                command = f'powershell.exe -Command cd {build_lib}/{ext.name};python -m numpy.f2py -c {to_compile} -m {module_name} --f90flags=-O3 {cmd_f90exec};{cmd_copy_libs}'
            else:
                raise OSError('Unsupported OS')
            result = os.system(command)
            if result != 0:
                raise RuntimeError(
                    f'Failed to compile {to_compile} with command: {command}')


setup(
    name="ndtest",
    version="0.3.0",
    author="Tao Jing",
    author_email="jingt20@mails.tsinghua.edu.cn",
    description=
    "The collection of nonparametric test of the equality of high-dimensional probability distributions",
    packages=find_packages(),
    ext_modules=[f2py_Extension('ndtest', ['ndtest/maxdist.f90'])],
    cmdclass=dict(build_ext=f2py_Build))
