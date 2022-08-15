"""Accelerator module."""

import numpy as _np
import pyaccel as _pyaccel
from . import lattice as _lattice


default_cavity_on = False
default_radiation_on = 'off'
default_vchamber_on = False


def create_accelerator(
        optics_mode=_lattice.default_optics_mode, simplified=False, ids=None,
        ids_vchamber=True):
    """Create accelerator model."""
    lattice = _lattice.create_lattice(
        optics_mode=optics_mode, simplified=simplified, ids=ids,
        ids_vchamber=ids_vchamber)
    accelerator = _pyaccel.accelerator.Accelerator(
        lattice=lattice,
        energy=_lattice.energy,
        harmonic_number=_lattice.harmonic_number,
        cavity_on=default_cavity_on,
        radiation_on=default_radiation_on,
        vchamber_on=default_vchamber_on)

    return accelerator


accelerator_data = dict()
accelerator_data['lattice_version'] = 'SI_V25_04'
accelerator_data['global_coupling'] = 0.01  # expected corrected value
accelerator_data['pressure_profile'] = \
    _np.array([[0, 518.3899], [1.333e-9]*2])  # [s [m], p [mbar]]
