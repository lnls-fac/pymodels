#!/usr/bin/env python3

from setuptools import setup, find_packages

with open('VERSION','r') as _f:
    __version__ = _f.read().strip()

setup(
    name='sirius',
    version=__version__,
    author='lnls-fac',
    description='Sirius lattice definitions',
    url='https://github.com/lnls-fac/sirius',
    download_url='https://github.com/lnls-fac/sirius',
    license='MIT License',
    classifiers=[
        'Intended Audience :: Science/Research',
        'Programming Language :: Python',
        'Topic :: Scientific/Engineering'
    ],
    packages=find_packages(),
    package_data={'sirius': ['VERSION']},

    # install_requires=[
    #     'numpy>=1.8.2',
    #     'mathphys>=0.1.0',
    #     'pyaccel>=0.3.0',
    # ],
    # dependency_links=[
    #     'https://github.com/lnls-fac/mathphys/archive/v0.1.0.tar.gz#egg=mathphys-0.1.0',
    #     'https://github.com/lnls-fac/pyaccel/archive/v0.3.0.tar.gz#egg=pyaccel-0.3.0',
    # ],
    zip_safe=False,
)
