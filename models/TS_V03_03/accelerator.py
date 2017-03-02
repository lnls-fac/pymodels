
import numpy as _np
import lnls as _lnls
import pyaccel as _pyaccel
from . import lattice as _lattice


default_radiation_on = False
default_vchamber_on = False


def create_accelerator(optics_mode = _lattice.default_optics_mode):
    latt, twiss_at_start = _lattice.create_lattice(optics_mode=optics_mode)
    accelerator = _pyaccel.accelerator.Accelerator(
        lattice= latt,
        energy=_lattice.energy,
        radiation_on=default_radiation_on,
        vchamber_on=default_vchamber_on
    )
    return accelerator, twiss_at_start


accelerator_data = dict()
accelerator_data['lattice_version'] = 'TS_V03_03'
accelerator_data['dirs'] = {
    'excitation_curves': _lnls.folder_excitation_curves,
    'pulse_curves': _lnls.folder_pulse_curves,
}
accelerator_data['pressure_profile'] = None
