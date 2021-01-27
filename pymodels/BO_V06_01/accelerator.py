
import numpy as _np
import lnls as _lnls
import pyaccel as _pyaccel
from . import lattice as _lattice


default_cavity_on = False
default_radiation_on = False
default_vchamber_on = False


def create_accelerator(optics_mode=_lattice.default_optics_mode, energy=_lattice.energy):
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


accelerator_data = dict()
accelerator_data['lattice_version'] = 'BO_V06_01'
accelerator_data['global_coupling'] = 0.0002  # expected corrected value
accelerator_data['pressure_profile'] = _np.array([[0, 496.8], [1.5e-8]*2])  # [s [m], p [mbar]]o
496.78745
