"""Accelerator module."""

import numpy as _np
import pyaccel as _pyaccel
from . import lattice as _lattice
from mathphys.functions import get_package_string as _get_pkg_str

default_cavity_on = False
default_radiation_on = 'off'
default_vchamber_on = False


def create_accelerator(
        optics_mode=_lattice.default_optics_mode, energy=_lattice.energy):
    """Create accelerator model."""
    lattice = _lattice.create_lattice(optics_mode=optics_mode, energy=energy)
    accelerator = _pyaccel.accelerator.Accelerator(
        lattice=lattice,
        lattice_version=lattice_version,
        energy=energy,
        harmonic_number=_lattice.harmonic_number,
        cavity_on=default_cavity_on,
        radiation_on=default_radiation_on,
        vchamber_on=default_vchamber_on
    )
    return accelerator


lattice_version = 'BO_V06_01'
lattice_version += '_' + _get_pkg_str('pymodels')

accelerator_data = dict()
accelerator_data['lattice_version'] = lattice_version
# Measured value, uncertainty: +/- 0.003
accelerator_data['global_coupling'] = 0.006
# [s [m], p [mbar]]
accelerator_data['pressure_profile'] = _np.array([[0, 496.8], [1.5e-8]*2])
