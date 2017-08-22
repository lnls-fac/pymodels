#!/usr/bin/env python-sirius

from setuptools import setup, find_packages

with open('VERSION','r') as _f:
    __version__ = _f.read().strip()

setup(
    name='pymodels',
    version=__version__,
    author='lnls-fac',
    description='pyModels lattice definitions',
    url='https://github.com/lnls-fac/pymodels',
    download_url='https://github.com/lnls-fac/pymodels',
    license='MIT License',
    classifiers=[
        'Intended Audience :: Science/Research',
        'Programming Language :: Python',
        'Topic :: Scientific/Engineering'
    ],
    packages=find_packages(),
    package_data={'pymodels': ['VERSION','BO_V02A/at_flat_file_M0.txt']},
    zip_safe=False
)
