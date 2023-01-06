"""Accelerator module."""

import pyaccel as _pyaccel
from . import lattice as _lattice


default_radiation_on = 'off'
default_vchamber_on = False


def create_accelerator(optics_mode=_lattice.default_optics_mode):
    """Create accelerator model."""
    latt, twiss_at_start = _lattice.create_lattice(optics_mode=optics_mode)
    lattice_version = 'TS_V04_01'
    accelerator = _pyaccel.accelerator.Accelerator(
        lattice=latt,
        lattice_version=lattice_version,
        energy=_lattice.energy,
        radiation_on=default_radiation_on,
        vchamber_on=default_vchamber_on
    )
    return accelerator, twiss_at_start
