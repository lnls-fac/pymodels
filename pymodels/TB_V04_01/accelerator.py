"""Accelerator module."""

import pyaccel as _pyaccel
from . import lattice as _lattice
from mathphys.functions import repository_info as _repo_info


default_radiation_on = 'off'
default_vchamber_on = False


def create_accelerator(optics_mode=_lattice.default_optics_mode,
                       simplified=False):
    """Create accelerator model."""
    lattice, twiss_at_start = _lattice.create_lattice(optics_mode=optics_mode)
    lattice_version = 'TB_V04_01'
    accelerator = _pyaccel.accelerator.Accelerator(
        lattice=lattice,
        lattice_version=lattice_version,
        energy=_lattice.energy,
        radiation_on=default_radiation_on,
        vchamber_on=default_vchamber_on
    )
    return accelerator, twiss_at_start


_info = _repo_info(__file__)
lattice_version = 'TB_V04_01'
lattice_version += f"_tag={_info['last_tag']:s}"
lattice_version += f"_commit={_info['last_commit']:s}"
if _info['is_dirty']:
    lattice_version += f"_dirty"

accelerator_data = dict()
accelerator_data['lattice_version'] = lattice_version
accelerator_data['pressure_profile'] = None
