from numpy.distutils.core import Extension
from setuptools import find_packages, setup

f2py_compile = Extension(
    name='ndtest.maxdist',  # Name of the extension module
    sources=['ndtest/maxdist.f90'],  # Fortran source file(s)
    extra_compile_args=['-O3'],  # Additional compilation options if needed
    f2py_options=['--quiet'],  # f2py-specific options
)

setup(
    name="ndtest",
    version="0.1",
    author="Tao Jing",
    author_email="jingt20@mails.tsinghua.edu.cn",
    description=
    "The collection of nonparametric test of the equality of high-dimensional probability distributions",
    ext_modules=[f2py_compile],
    packages=find_packages())
