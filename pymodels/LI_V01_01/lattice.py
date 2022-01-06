#!/usr/bin/env python-sirius

import math as _math
import pyaccel as _pyaccel

default_optics_mode = 'M1'
default_operation_mode = 'injection'
energy = 0.15e9  # [eV]
emittance = 170.3329758677203e-09  # [m rad]
energy_spread = 0.005
single_bunch_charge = 1e-9  # [Coulomb]
multi_bunch_charge  = 3e-9  # [Coulomb]
single_bunch_pulse_duration = 1e-9  # [seconds]
multi_bunch_pulse_duration = 150e-9  # [seconds]
frequency = 3e9  # [Hz]


def create_lattice(
        optics_mode=default_optics_mode,
        operation_mode=default_operation_mode):
    """."""
    # -- selection of operation_mode --
    if operation_mode == 'emittance_measurement':
        mode0, mode1, mode2 = True, False, False
    elif operation_mode == 'injection':
        mode0, mode1, mode2 = False, True, False
    elif operation_mode == 'energy_dispersion':
        mode0, mode1, mode2 = False, False, True
    else:
        Exception('Invalid LI operation mode: ' + operation_mode)

    strengths, twiss_at_match = get_optics_mode(optics_mode)

    marker = _pyaccel.elements.marker
    drift = _pyaccel.elements.drift
    quadrupole = _pyaccel.elements.quadrupole
    rbend_sirius = _pyaccel.elements.rbend
    hcorrector = _pyaccel.elements.hcorrector
    vcorrector = _pyaccel.elements.vcorrector

    # --- drifts ---
    l100 = drift('l100', 0.1000)
    l200 = drift('l200', 0.2000)
    l300 = drift('l300', 0.3000)
    l500 = drift('l500', 0.5000)
    l600 = drift('l600', 0.6000)
    la1 = drift('la1', 0.1150)
    la2p = drift('la2p', 0.2100)
    la3p = drift('la3p', 0.1488)
    la4p = drift('la4p', 0.0512)

    # --- markers ---
    inicio = marker('start')
    fim = marker('end')
    match_start = marker('match_start')

    egun = marker('EGun')

    # --- beam screens ---
    scrn = marker('Scrn')

    # --- beam current monitors ---
    ict = marker('ICT')

    # --- beam position monitors ---
    bpm = marker('BPM')

    # --- correctors ---
    ch = hcorrector('CH')
    cv = vcorrector('CV')

    # --- lens ---
    lens = marker('Lens')
    lensrev = marker('LensRev')

    # --- dump ---
    dump = marker('Dump')

    # --- solenoids ---
    solnd01 = marker('Slnd01')
    solnd02 = marker('Slnd02')
    solnd03 = marker('Slnd03')
    solnd04 = marker('Slnd04')
    solnd05 = marker('Slnd05')
    solnd06 = marker('Slnd06')
    solnd07 = marker('Slnd07')
    solnd08 = marker('Slnd08')
    solnd09 = marker('Slnd09')
    solnd10 = marker('Slnd10')
    solnd11 = marker('Slnd11')
    solnd12 = marker('Slnd12')
    solnd13 = marker('Slnd13')
    solnd14 = marker('Slnd14')
    solnd15 = marker('Slnd15')
    solnd16 = marker('Slnd16')
    solnd17 = marker('Slnd17')
    solnd18 = marker('Slnd18')
    solnd19 = marker('Slnd19')
    solnd20 = marker('Slnd20')
    solnd21 = marker('Slnd21')

    # --- SHB ---
    shb = marker('SHB')
    bun = marker('Bun')
    acc_str = marker('AccStr')

    # --- quadrupoles ---
    qf1 = quadrupole('QF1', 0.05, strengths['qf1'])
    qd1 = quadrupole('QD1', 0.10, strengths['qd1'])
    qf2 = quadrupole('QF2', 0.05, strengths['qf2'])
    qd2 = quadrupole('QD2', 0.10, strengths['qd2'])
    qf3 = quadrupole('QF3', 0.05, strengths['qf3'])

    # --- bending magnets ---
    ang = 0.0 if mode0 else 15.0 if mode1 else 45.0
    # -- bspec --
    dip_nam = 'Spect'
    dip_len = 0.45003
    dip_ang = -ang * _math.pi/180
    dip_K = 0.0
    dip_S = 0.00
    spech = rbend_sirius(
        dip_nam, dip_len/2, dip_ang/2, 0, 0, 0, 0, 0,
        [0, 0, 0], [0, dip_K, dip_S])
    spec = [spech, spech]

    # --- lists ---
    L1_1 = [inicio, egun, l100, lens, l100, ict, l100, cv, ch, l100, lens]
    L1_2 = [
        l200, lensrev, shb, l200, lens, l100, scrn, bpm, l100, lens, l100,
        cv, ch]
    L1_Bun = [
        l300, solnd01, l100, solnd02, l100, solnd03, l100, cv, ch, solnd04,
        l100, solnd05, l100, solnd06, l100, solnd07, l100, bun, solnd08, l100,
        solnd09, l100, solnd10, l100, solnd11, l100, solnd12, l100, solnd13,
        l200]
    L1_4 = [l200, solnd14, l100, solnd14, l100, scrn, bpm, l200]
    L1_Ac1 = [
        l300, solnd15, l100, solnd15, l100, solnd16, l100, solnd16, cv, ch,
        l100, solnd17, l100, solnd17, l100, solnd18, l100, solnd18, acc_str,
        l100, solnd19, l100, solnd19, l100, solnd20, l100, solnd20, l100,
        solnd21, l100, solnd21, l200, l600, l600]
    L1_6 = [l300]
    L1_Ac2 = [l500, l500, cv, ch, l500, acc_str, l500, l500, l500]
    L1_8 = [l100, qf1, l100, qd1, l100, qf1, l200, scrn, l200]
    L1_Ac3 = [l500, l500, cv, ch, l500, acc_str, l500, l500, l500]
    L1_10 = [l300]
    L1_Ac4 = [l500, l500, cv, ch, l500, acc_str, l500, l500, l500]
    L1_12 = [match_start, la1, qf2, l100, qd2, l100, qf2, l100, qf3]
    L1_13 = [la2p, bpm, la3p, ict, la4p, l200, spec]

    L1 = [
        L1_1, L1_2, L1_Bun, L1_4, L1_Ac1, L1_6, L1_Ac2,
        L1_8, L1_Ac3, L1_10, L1_Ac4, L1_12, L1_13]
    L2 = [l500, l500, scrn, l500, dump]
    L3 = [l500, l500, scrn, l200, dump]

    elist = [L1] + ([L2] if mode0 else [] if mode1 else [L3]) + [fim]

    the_line = _pyaccel.lattice.build(elist)

    # shifts model to marker 'start'
    idx = _pyaccel.lattice.find_indices(the_line, 'fam_name', 'start')
    the_line = _pyaccel.lattice.shift(the_line, idx[0])

    lengths = _pyaccel.lattice.get_attribute(the_line, 'length')
    for length in lengths:
        if length < 0:
            raise LatticeError('Model with negative drift!')

    # sets number of integration steps
    set_num_integ_steps(the_line)

    # -- define vacuum chamber for all elements
    the_line = set_vacuum_chamber(the_line)

    return the_line, twiss_at_match


def get_optics_mode(optics_mode):
    """."""
    # -- selection of optics mode --
    if optics_mode == 'M1':
        strengths = {
            'qf2': 3.197471856142,
            'qd2': -1.57498322484,
            'qf3': 2.16753642533,
            'qd1': 0.00000000000,
            'qf1': 0.00000000000,
        }
        twiss_at_match = _pyaccel.optics.Twiss.make_new(
            beta=[7.0, 7.0], alpha=[0.0, 0.0])
    elif optics_mode == 'M2':
        strengths = {
            'qf2': 9.831704524983,
            'qd2': -4.217071772967,
            'qf3': -8.283779571728,
            'qd1': 0.00000000000,
            'qf1': 0.00000000000,
        }
        twiss_at_match = _pyaccel.optics.Twiss.make_new(
            beta=[10.0, 10.0], alpha=[0.0, 0.0])
    elif optics_mode == 'M3':
        strengths = {
            'qf2': 11.497289971737,
            'qd2': -4.009053542903,
            'qf3': -10.05208966219,
            'qd1': 0.00000000000,
            'qf1': 0.00000000000,
        }
        twiss_at_match = _pyaccel.optics.Twiss.make_new(
            beta=[7.0, 7.0], alpha=[-1.0, -1.0])
    elif optics_mode == 'M4':
        strengths = {
            'qf2': 3.534340054347,
            'qd2': -6.58275439308,
            'qf3': 8.590198057857,
            'qd1': 0.000000000000,
            'qf1': 0.000000000000,
        }
        twiss_at_match = _pyaccel.optics.Twiss.make_new(
            beta=[7.0, 7.0], alpha=[1.0, 1.0])
    elif optics_mode == 'M5':
        strengths = {
            'qf2': 14.330293389213,
            'qd2': -3.670822362331,
            'qf3': -14.999984099609,
            'qd1': 0.000000000000,
            'qf1': 0.000000000000,
        }
        twiss_at_match = _pyaccel.optics.Twiss.make_new(
            beta=[7.0, 7.0], alpha=[1.0, -1.0])
    elif optics_mode == 'M6':
        strengths = {
            'qf2': 10.334311920772,
            'qd2': -2.542582493248,
            'qf3': -10.124615533866,
            'qd1': 0.000000000000,
            'qf1': 0.000000000000,
        }
        twiss_at_match = _pyaccel.optics.Twiss.make_new(
            beta=[7.0, 7.0], alpha=[-1.0, 1.0])
    else:
        Exception('Invalid LI optics mode: ' + optics_mode)

    return strengths, twiss_at_match


def set_num_integ_steps(the_line):
    """."""
    for i in range(len(the_line)):
        if the_line[i].angle:
            length = the_line[i].length
            the_line[i].nr_steps = max(10, int(_math.ceil(length/0.035)))
        elif the_line[i].polynom_b[1]:
            the_line[i].nr_steps = 10
        elif the_line[i].polynom_b[2]:
            the_line[i].nr_steps = 5
        else:
            the_line[i].nr_steps = 1

    ch_indices = _pyaccel.lattice.find_indices(the_line, 'fam_name', 'CH')
    cv_indices = _pyaccel.lattice.find_indices(the_line, 'fam_name', 'CV')
    corr_indices = ch_indices + cv_indices
    for idx in corr_indices:
        the_line[idx].nr_steps = 5


def set_vacuum_chamber(the_line):
    """."""
    # -- default physical apertures --
    for i in range(len(the_line)):
        the_line[i].hmin = -0.018
        the_line[i].hmax = +0.018
        the_line[i].vmin = -0.018
        the_line[i].vmax = +0.018

    return the_line
