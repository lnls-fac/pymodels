#!/usr/bin/env python3

from setuptools import setup, find_packages

with open('VERSION','r') as _f:
    __version__ = _f.read().strip()

setup(
    name='models',
    version=__version__,
    author='lnls-fac',
    description='Models lattice definitions',
    url='https://github.com/lnls-fac/models',
    download_url='https://github.com/lnls-fac/models',
    license='MIT License',
    classifiers=[
        'Intended Audience :: Science/Research',
        'Programming Language :: Python',
        'Topic :: Scientific/Engineering'
    ],
    packages=find_packages(),
    package_data={'models': ['VERSION','BO_V02A/at_flat_file_M0.txt']},
    zip_safe=False
)
