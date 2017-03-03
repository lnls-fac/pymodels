#!/usr/bin/env python3

import os as _os
import math as _math
import mathphys as _mp
import pyaccel as _pyaccel

_default_optics_mode_label = 'M0'
_lattice_symmetry = 10
_harmonic_number  = 828
_energy = 0.15e9 #[eV]
_directory = _os.path.dirname(_os.path.realpath(__file__))


def create_lattice():
    filename = "at_flat_file_{0}.txt".format(_default_optics_mode_label)
    the_ring = _pyaccel.lattice.read_flat_file(_os.path.join(_directory, filename))

    if the_ring.energy != _energy:
        raise Exception
    if the_ring.harmonic_number != _harmonic_number:
        raise Exception

    return the_ring


def set_rf_frequency(the_ring):
    circumference = _pyaccel.lattice.length(the_ring)
    velocity = _mp.constants.light_speed
    rev_frequency = velocity / circumference
    rf_frequency  = _harmonic_number * rev_frequency
    idx = _pyaccel.lattice.find_indices(the_ring, 'fam_name', 'cav')
    for i in idx:
        the_ring[i].frequency = rf_frequency


def set_rf_voltage(the_ring, energy):
    overvoltage = 1.525
    energy0 = 0.15e9
    rho0   = 1.152*50/(2*_math.pi)
    U0 = (_mp.constants.rad_cgamma*((energy*1e-9)**4)/rho0)*1e9

    voltage_inj = 150e3 - overvoltage*((_mp.constants.rad_cgamma*((energy0*1e-9)**4)/rho0)*1e9)
    voltage_eje = 950e3
    voltage = min([(overvoltage*U0 + voltage_inj), voltage_eje])

    idx = _pyaccel.lattice.find_indices(the_ring, 'fam_name', 'cav')
    for i in idx:
        the_ring[i].voltage = voltage
