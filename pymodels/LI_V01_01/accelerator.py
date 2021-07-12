
import numpy as _np
import lnls as _lnls
import pyaccel as _pyaccel
from . import lattice as _lattice


default_cavity_on = False
default_radiation_on = False
default_vchamber_on = False

def create_accelerator(optics_mode=_lattice.default_optics_mode,
                       operation_mode = _lattice.default_operation_mode):
    lattice, twiss_at_match = _lattice.create_lattice(optics_mode=optics_mode,operation_mode=operation_mode)
    accelerator = _pyaccel.accelerator.Accelerator(
        lattice=lattice,
        energy=_lattice.energy,
        radiation_on=default_radiation_on,
        vchamber_on=default_vchamber_on
    )
    return accelerator, twiss_at_match


accelerator_data = dict()
accelerator_data['lattice_version'] = 'LI_V01'
accelerator_data['global_coupling']  = 1.00 # expected corrected value
accelerator_data['emittance']        = 170.3329758677203e-09 # [m·rad]
accelerator_data['energy_spread']    = 0.005
accelerator_data['pressure_profile'] = None
_, accelerator_data['twiss_at_match'] = _lattice.get_optics_mode(optics_mode=_lattice.default_optics_mode)
