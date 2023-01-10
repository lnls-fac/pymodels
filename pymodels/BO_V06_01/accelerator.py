
import numpy as _np
import pyaccel as _pyaccel
from . import lattice as _lattice
from mathphys.functions import repository_info as _repo_info

default_cavity_on = False
default_radiation_on = 'off'
default_vchamber_on = False


def create_accelerator(
        optics_mode=_lattice.default_optics_mode, energy=_lattice.energy):
    """Create accelerator model."""
    lattice = _lattice.create_lattice(optics_mode=optics_mode, energy=energy)
    accelerator = _pyaccel.accelerator.Accelerator(
        lattice=lattice,
        energy=energy,
        harmonic_number=_lattice.harmonic_number,
        cavity_on=default_cavity_on,
        radiation_on=default_radiation_on,
        vchamber_on=default_vchamber_on
    )
    return accelerator


_info = _repo_info(__file__)
lattice_version = 'BO_V06_01'
lattice_version += f"_tag={_info['last_tag']:s}"
lattice_version += f"_commit={_info['last_commit']:s}"
if _info['is_dirty']:
    lattice_version += f"_dirty"

accelerator_data = dict()
accelerator_data['lattice_version'] = lattice_version
# Measured value, uncertainty: +/- 0.003
accelerator_data['global_coupling'] = 0.006
# [s [m], p [mbar]]
accelerator_data['pressure_profile'] = _np.array([[0, 496.8], [1.5e-8]*2])
