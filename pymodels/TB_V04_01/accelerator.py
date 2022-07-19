"""Accelerator module."""

import pyaccel as _pyaccel
from . import lattice as _lattice


default_radiation_on = False
default_quantdiff_on = False
default_vchamber_on = False


def create_accelerator(optics_mode=_lattice.default_optics_mode,
                       simplified=False):
    """Create accelerator model."""
    lattice, twiss_at_start = _lattice.create_lattice(optics_mode=optics_mode)
    accelerator = _pyaccel.accelerator.Accelerator(
        lattice=lattice,
        energy=_lattice.energy,
        radiation_on=default_radiation_on,
        quantdiff_on=default_quantdiff_on,
        vchamber_on=default_vchamber_on
    )
    return accelerator, twiss_at_start


accelerator_data = dict()
accelerator_data['lattice_version'] = 'TB_V04_01'
accelerator_data['pressure_profile'] = None
