import subprocess

from setuptools import find_packages, setup


f2py_command = [
    "f2py",
    "-c",
    "maxdist.f90",
    "-m",
    "maxdist",
    "--f90flags=-O3",
]
subprocess.run(f2py_command, check=True, cwd="ndtest")

setup(
    name="ndtest",
    version="0.1",
    author="Tao Jing",
    author_email="jingt20@mails.tsinghua.edu.cn",
    description=
    "The collection of nonparametric test of the equality of high-dimensional probability distributions",
    packages=find_packages(),
    package_data={
        '': ['*.so', '*.dll'],  # Include shared libraries
    },
)
