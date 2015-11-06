#!/usr/bin/env python3

import math as _math
import numpy as _np
import pyaccel as _pyaccel
import mathphys as _mp
from . import optics_mode_M0 as _optics_mode_M0

_default_optics_mode = _optics_mode_M0
_energy = 0.15e9 #[eV]
_emittance = 170.3329758677203e-09 #[m rad]
_energy_spread = 0.005
_single_bunch_charge = 1e-9 #[Coulomb]
_multi_bunch_charge  = 3e-9 #[Coulomb]
_pulse_duration_interval = 150e-9 #[seconds]
_frequency = 3e9 #[Hz]

def create_lattice(**kwargs):
    marker = _pyaccel.elements.marker
    linac = marker('linac')
    elist = [linac]
    the_line = _pyaccel.lattice.build(elist)

    return the_line
