
import os as _os
import numpy as _np
import lnls as _lnls
import pyaccel as _pyaccel
from . import lattice as _lattice


_default_radiation_on = False
_default_vchamber_on = False

def create_accelerator():

    accelerator = _pyaccel.accelerator.Accelerator(
        lattice=_lattice.create_lattice(),
        energy=_lattice._energy,
        radiation_on=_default_radiation_on,
        vchamber_on=_default_vchamber_on )

    return accelerator

_folder_code = _lnls.system.folder_code

accelerator_data = dict()
accelerator_data['lattice_version'] = 'TB_V300'
accelerator_data['dirs'] = {
    'excitation_curves': _os.path.join(_folder_code, 'sirius', 'excitation_curves'),
}
accelerator_data['global_coupling']  = 1.0 # expected corrected value
accelerator_data['pressure_profile'] = None
