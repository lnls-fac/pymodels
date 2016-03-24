
import numpy as _np
import lnls as _lnls
import pyaccel as _pyaccel
from . import lattice as _lattice


_default_cavity_on = False
_default_radiation_on = False
_default_vchamber_on = False


def create_accelerator():
    lattice = _lattice.create_lattice()

    if isinstance(lattice, _pyaccel.accelerator.Accelerator):
        accelerator = lattice
        accelerator.energy = _lattice._energy
        accelerator.cavity_on = _default_cavity_on
        accelerator.radiation_on = _default_radiation_on
        accelerator.vchamber_on = _default_vchamber_on
        _lattice.set_rf_frequency(accelerator)
        _lattice.set_rf_voltage(accelerator, accelerator.energy)
    else:
        accelerator = _pyaccel.accelerator.Accelerator(
            lattice=lattice,
            energy=_lattice._energy,
            harmonic_number=_lattice._harmonic_number,
            cavity_on=_default_cavity_on,
            radiation_on=_default_radiation_on,
            vchamber_on=_default_vchamber_on
        )

    return accelerator


accelerator_data = dict()
accelerator_data['lattice_version'] = 'BO_V02A'
accelerator_data['dirs'] = {
    'excitation_curves': _lnls.system.folder_excitation_curves,
    'pulse_curves': _lnls.system.folder_pulse_curves,
}
accelerator_data['global_coupling'] = 0.0002 # expected corrected value
accelerator_data['pressure_profile'] = _np.array([[0, 496.8], [1.5e-8]*2]) # [s [m], p [mbar]]
accelerator_data['injection_kicker_nominal_deflection']  = -0.01934 # [rad]
accelerator_data['extraction_kicker_nominal_deflection'] =  0.00132 # [rad]
