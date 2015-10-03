
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
        harmonic_number=_lattice._harmonic_number,
        cavity_on=_default_cavity_on,
        radiation_on=_default_radiation_on,
        vchamber_on=_default_vchamber_on
    )

    return accelerator


_folder_code = _lnls.system.folder_code

accelerator_data = dict()
accelerator_data['lattice_version'] = 'SI_V12'
accelerator_data['dirs'] = {
    'excitation_curves': _lnls.system.folder_excitation_curves,
}
accelerator_data['global_coupling'] = 0.01 # expected corrected value
accelerator_data['pressure_profile'] = _np.array([[0, 518.396],[1.333e-9]*2]) # [s [m], p [mbar]]
accelerator_data['on_axis_kicker_nominal_deflection']  = -0.00537 # [rad]
accelerator_data['pmm_integ_polynom_b'] = [0.0, 0.0, 1.783421291201796e-12, -1.381477177995143e+04, -4.429672105977303e-08,
                                  1.876651541471924e+08, 2.355070967964111e-04, -6.583350601500055e+11]
