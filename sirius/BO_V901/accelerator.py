
import numpy as _np
import pyaccel as _pyaccel
from . import lattice as _lattice


_default_cavity_on = False
_default_radiation_on = False
_default_vchamber_on = False


def create_accelerator():
    accelerator = _pyaccel.accelerator.Accelerator(
        lattice=_lattice.create_lattice(),
        energy=_lattice._energy,
        harmonic_number=_lattice._harmonic_number,
        cavity_on=_default_cavity_on,
        radiation_on=_default_radiation_on,
        vchamber_on=_default_vchamber_on)

    return accelerator


accelerator_data = dict()
accelerator_data['lattice_version'] = 'BO_V901'
# accelerator_data['dirs'] = {
#     'excitation_curves': _os.path.join(_folder_code, 'sirius', 'excitation_curves'),
# }
accelerator_data['global_coupling'] = 0.0002 # expected corrected value
accelerator_data['pressure_profile'] = _np.array([0, 1.5e-8]) # [s [m], p [mbar]]
