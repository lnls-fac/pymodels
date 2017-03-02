
import numpy as _np
import lnls as _lnls
import pyaccel as _pyaccel
from . import lattice as _lattice


default_cavity_on = False
default_radiation_on = False
default_vchamber_on = False


def create_accelerator(optics_mode=_lattice.default_optics_mode):
    accelerator = _pyaccel.accelerator.Accelerator(
        lattice=_lattice.create_lattice(mode=optics_mode),
        energy=_lattice.energy,
        harmonic_number=_lattice.harmonic_number,
        cavity_on=default_cavity_on,
        radiation_on=default_radiation_on,
        vchamber_on=default_vchamber_on
    )

    return accelerator


_folder_code = _lnls.folder_code

accelerator_data = dict()
accelerator_data['lattice_version'] = 'SI_V21_02'
accelerator_data['dirs'] = {
    'excitation_curves': _lnls.folder_excitation_curves,
    'pulse_curves': _lnls.folder_pulse_curves,
}
accelerator_data['global_coupling'] = 0.01 # expected corrected value
accelerator_data['pressure_profile'] = _np.array([[0, 518.396],[1.333e-9]*2]) # [s [m], p [mbar]]
