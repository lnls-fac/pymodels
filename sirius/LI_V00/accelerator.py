
import numpy as _np
import lnls as _lnls
import pyaccel as _pyaccel
from . import lattice as _lattice


_default_cavity_on = False
_default_radiation_on = False
_default_vchamber_on = False


def create_accelerator():
    accelerator = _pyaccel.accelerator.Accelerator(
        lattice=_lattice.create_lattice(),
        energy=_lattice._energy,
        radiation_on=_default_radiation_on,
        vchamber_on=_default_vchamber_on
    )

    return accelerator


_folder_code = _lnls.system.folder_code

accelerator_data = dict()
accelerator_data['lattice_version'] = 'LI_V00'
accelerator_data['dirs'] = {
    'excitation_curves': _lnls.system.folder_excitation_curves,
}
accelerator_data['global_coupling']  = 1.00 # expected corrected value
accelerator_data['emittance']        = 170.3329758677203e-09 # [m·rad]
accelerator_data['energy_spread']    = 0.005
accelerator_data['twiss_at_exit']    = _pyaccel.optics.Twiss.make_new(beta=[7.0,7.0], alpha=[-1.0,-1.0])
accelerator_data['pressure_profile'] = None
