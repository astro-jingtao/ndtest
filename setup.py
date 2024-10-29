import os

from setuptools import Extension, find_packages, setup
from setuptools.command.build_ext import build_ext


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
            result = os.system(
                f'cd {build_lib}/{ext.name};f2py -c {to_compile} -m {module_name} --f90flags=-O3'
            )
            if result != 0:
                raise RuntimeError(f'Failed to compile {to_compile}')


setup(
    name="ndtest",
    version="0.1.0",
    author="Tao Jing",
    author_email="jingt20@mails.tsinghua.edu.cn",
    description=
    "The collection of nonparametric test of the equality of high-dimensional probability distributions",
    packages=find_packages(),
    ext_modules=[f2py_Extension('ndtest', ['ndtest/maxdist.f90'])],
    cmdclass=dict(build_ext=f2py_Build))
