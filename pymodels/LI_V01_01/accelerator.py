"""Accelerator module."""

import pyaccel as _pyaccel
from . import lattice as _lattice
from mathphys.functions import get_package_string as _get_pkg_str

default_cavity_on = False
default_radiation_on = 'off'
default_vchamber_on = False


def create_accelerator(optics_mode=_lattice.default_optics_mode,
                       operation_mode=_lattice.default_operation_mode):
    """Create accelerator model."""
    lattice, twiss_at_match = _lattice.create_lattice(
        optics_mode=optics_mode, operation_mode=operation_mode)
    accelerator = _pyaccel.accelerator.Accelerator(
        lattice=lattice,
        lattice_version=lattice_version,
        energy=_lattice.energy,
        radiation_on=default_radiation_on,
        vchamber_on=default_vchamber_on
    )
    return accelerator, twiss_at_match


lattice_version = 'LI_V01_01'
lattice_version += '_' + _get_pkg_str('pymodels')

accelerator_data = dict()
accelerator_data['global_coupling'] = 1.00  # expected corrected value
accelerator_data['emittance'] = 170.3329758677203e-09  # [m·rad]
accelerator_data['energy_spread'] = 0.005
_, accelerator_data['twiss_at_match'] = _lattice.get_optics_mode(
    optics_mode=_lattice.default_optics_mode)
