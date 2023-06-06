"""Lattice module.

In this module the lattice of the corresponding accelerator is defined.
"""

import math as _math
from pyaccel import lattice as _pyacc_lat, elements as _pyacc_ele, \
    accelerator as _pyacc_acc, optics as _pyacc_opt
from . import segmented_models as _segmented_models

energy = 0.150e9  # [eV]
default_optics_mode = 'M1'
default_add_from_li_triplets = True

class LatticeError(Exception):
    """LatticeError class."""


def create_lattice(
        optics_mode=default_optics_mode,
        add_from_li_triplets=default_add_from_li_triplets):
    """Create lattice function."""
    strengths, twiss_at_start = \
        get_optics_mode(optics_mode, add_from_li_triplets)

    # -- shortcut symbols --
    marker = _pyacc_ele.marker
    drift = _pyacc_ele.drift
    quadrupole = _pyacc_ele.quadrupole
    rbend_sirius = _pyacc_ele.rbend
    sextupole = _pyacc_ele.sextupole

    deg_2_rad = _math.pi / 180.0

    corr_length = 0.082

    # --- drift spaces ---
    lp2 = drift('lp2', 0.0002)
    lp3 = drift('lp3', 0.0003)
    lp4 = drift('lp4', 0.0004)
    lp5 = drift('lp5', 0.0005)
    lp6 = drift('lp6', 0.0006)
    lp7 = drift('lp7', 0.0007)

    l1 = drift('l1', 0.001)
    l2 = drift('l2', 0.002)
    l3 = drift('l3', 0.003)
    l4 = drift('l4', 0.004)
    l5 = drift('l5', 0.005)
    l6 = drift('l6', 0.006)
    l7 = drift('l7', 0.007)
    l8 = drift('l8', 0.008)
    l9 = drift('l9', 0.009)
    l10 = drift('l10', 0.010)
    l30 = drift('l30', 0.030)
    l40 = drift('l40', 0.040)
    l60 = drift('l60', 0.060)
    l70 = drift('l70', 0.070)
    l80 = drift('l80', 0.080)
    l90 = drift('l90', 0.090)
    l100 = drift('l100', 0.100)
    l200 = drift('l200', 0.200)

    # --- markers ---
    start = marker('start')
    end = marker('end')

    # --- slits ---
    slith = marker('SlitH')
    slitv = marker('SlitV')

    # --- beam screens ---
    scrn = marker('Scrn')

    # --- beam current monitors ---
    ict = marker('ICT')
    fct = marker('FCT')

    # --- beam position monitors ---
    bpm = marker('BPM')

    # --- correctors ---
    chv = sextupole('CHV', corr_length, 0.0)
    qs = quadrupole('QS', corr_length, 0.0)

    # --- quadrupoles ---
    qf2L = quadrupole('QF2L', 0.112, strengths['qf2l'])  # LINAC TRIPLET
    qd2L = quadrupole('QD2L', 0.162, strengths['qd2l'])  # LINAC TRIPLET
    qf3L = quadrupole('QF3L', 0.112, strengths['qf3l'])  # LINAC QUADRUPOLE

    # -- spec --
    ang = 15.0  # injection mode
    dip_nam = 'Spect'
    dip_len = 0.45003
    dip_ang = -ang * deg_2_rad
    dip_K = 0.0
    dip_S = 0.00
    spech = rbend_sirius(dip_nam, dip_len/2, dip_ang/2,
                         0, 0,
                         0, 0, 0, [0, 0, 0], [0, dip_K, dip_S])
    spec = [spech, spech]

    qd1 = quadrupole('QD1', 0.100, strengths['qd1'])
    qf1 = quadrupole('QF1', 0.100, strengths['qf1'])
    qd2a = quadrupole('QD2A', 0.100, strengths['qd2a'])
    qf2a = quadrupole('QF2A', 0.100, strengths['qf2a'])
    qf2b = quadrupole('QF2B', 0.100, strengths['qf2b'])
    qd2b = quadrupole('QD2B', 0.100, strengths['qd2b'])
    qf3 = quadrupole('QF3', 0.100, strengths['qf3'])
    qd3 = quadrupole('QD3', 0.100, strengths['qd3'])
    qf4 = quadrupole('QF4', 0.100, strengths['qf4'])
    qd4 = quadrupole('QD4', 0.100, strengths['qd4'])

    # --- bending magnets ---
    bp = _segmented_models.dipole(sign=+1)
    bn = _segmented_models.dipole(sign=-1)

    septin = _segmented_models.septum(strengths)

    #  --- lines ---
    s00_1 = [l80, l4, qf2L, l30, l8, qd2L, l30, l8, qf2L, l30, l8, qf3L]
    s00_2 = [l80, l7, bpm, l200, l40, l6, ict, l200, l100, l90, l5]
    s01_1 = [
        l200, l200, l200, l80, l4, lp2, scrn, l100, l40, lp2, bpm,
        l100, l2, lp4]
    s01_2 = [l80, l8, lp4, chv, l200, l90, l1, lp2]
    s01_3 = [
        l200, l200, l200, l200, l200, l40, l4, slith, l100, l80, scrn,
        l100, l40, bpm, l100, l90, l9, chv, l100, l90, l3, lp3, slitv,
        l200, l10, lp4]
    s02_1 = [l100, l90, l4, lp4, ict, l200, l200, l200, l10, l6]
    s02_2 = [l200, l70]
    s02_3 = [
        l200, scrn, l100, l40, bpm, l60, l9, chv] + [l200]*26 + \
        [l100, l70, l3]
    s02_4 = [l200, l70]
    s02_5 = [
        l200, scrn, l100, l40, bpm, l60, l8, lp5, chv, l200, l100,
        l10, l9, lp7]
    s03_1 = [l200] * 10 + [l100, l90, l9, lp6]
    s03_2 = [l200, l6]
    s03_3 = [l100, bpm, l100, l40, l4, scrn, l200, l10, lp4]
    s04_1 = [
        l200, l70, l2, lp4, chv, l200, l200, l100, l80, lp5, fct,
        l100, l40, ict, l200, l100, l5, lp7, bpm, l100, l10, l5, lp6]
    s04_2 = [l200, l10, l6]
    s04_3 = [l100, l70, scrn, l60, l1, lp2, qs, l80, l6, lp6]

    sector00 = [s00_1, s00_2, spec]
    sector01 = [s01_1, qd1, s01_2, qf1, s01_3, bn]
    sector02 = [s02_1, qd2a, s02_2, qf2a, s02_3, qf2b, s02_4, qd2b, s02_5, bp]
    sector03 = [s03_1, qf3, s03_2, qd3, s03_3, bp]
    sector04 = [s04_1, qf4, s04_2, qd4, s04_3, septin]

    # TB beamline
    if add_from_li_triplets:
        ltlb = [
            start, sector00, sector01, sector02, sector03, sector04, end]
    else:
        ltlb = [start, sector01, sector02, sector03, sector04, end]
    elist = ltlb

    the_line = _pyacc_lat.build(elist)

    # --- shifts model to marker 'start' ---
    idx = _pyacc_lat.find_indices(the_line, 'fam_name', 'start')
    the_line = _pyacc_lat.shift(the_line, idx[0])

    lengths = _pyacc_lat.get_attribute(the_line, 'length')
    for length in lengths:
        if length < 0:
            raise LatticeError('Model with negative drift!')

    # sets number of integration steps
    set_num_integ_steps(the_line)

    # -- define vacuum chamber for all elements
    the_line = set_vacuum_chamber(the_line)

    return the_line, twiss_at_start


def get_optics_mode(optics_mode ,add_from_li_triplets):
    """Return magnet strengths of a given opics mode."""
    # -- selection of optics mode --
    if optics_mode == 'M1':
        # Initial Conditions from Linac measured parameters on 30/08/2019
        # Linac second quadrupole triplet set to same values used during
        # measurements
        # (Sem tripleto)
        # QD4 freed to be focusing in fitting.
        if add_from_li_triplets:
            twiss_at_start = _pyacc_opt.Twiss.make_new(
                beta=[1.45401, 2.47656],
                alpha=[-1.57249, 0.527312], etax=[0, 0])
        else:
            # propagated from above twiss value
            twiss_at_start = _pyacc_opt.Twiss.make_new(
                beta=[1.1654363475785563, 7.3582182762528765],
                alpha=[0.5607752743579607, -2.9557170327962807],
                etax=[-0.05857309412506855, 0])

        strengths = {
            'qf2l': 12.37,
            'qd2l': -14.85,
            'qf3l': 6.3387,
            'qd1': -8.8224,
            'qf1':  13.3361,
            'qd2a': -10.8698,
            'qf2a': 13.8136,
            'qf2b': 6.9037,
            'qd2b': -6.3496,
            'qf3':  13.4901,
            'qd3': -10.8577,
            'qf4':  8.1889,
            'qd4':  0.6693,
            'injsept_kxl': -0.39475202,
            'injsept_kyl': +0.35823882,
            'injsept_ksxl': -0.04944937,
            'injsept_ksyl': -0.00393883,
            }

    if optics_mode == 'M2':
        # Initial Conditions from Linac measured parameters on 30/08/2019
        # Linac second quadrupole triplet set to same values used during
        # measurements
        # (Sem tripleto)
        if add_from_li_triplets:
            twiss_at_start = _pyacc_opt.Twiss.make_new(
                beta=[1.45401, 2.47656],
                alpha=[-1.57249, 0.527312], etax=[0, 0])
        else:
            twiss_at_start = _pyacc_opt.Twiss.make_new(
                beta=[1.1636775006139601, 7.362467566808375],
                alpha=[0.5604253077073319, -2.958197325547372],
                etax=[-0.05857309412506855, 0])

        strengths = {
            'qf2l': 12.37,
            'qd2l': -14.85,
            'qf3l': 6.342735948415,
            'qd1': -8.822330690694,
            'qf1': 13.336079810152,
            'qd2a': -11.779088961602,
            'qf2a': 14.331275527616,
            'qf2b': 8.958478776817,
            'qd2b': -8.99233133968,
            'qf3': 11.263508962434,
            'qd3': -6.891349798498,
            'qf4': 9.84840688362,
            'qd4': -3.114739958144,
            'injsept_kxl': -0.3,
            'injsept_kyl': 0.3,
            'injsept_ksxl': 0.0,
            'injsept_ksyl': 0.0,
            }

    if optics_mode == 'M3':
        # Initial Conditions from Linac measured parameters on 16/07/2019
        # Linac second quadrupole triplet set to same values used during
        # measurements
        # (Sem tripleto)
        if add_from_li_triplets:
            twiss_at_start = _pyacc_opt.Twiss.make_new(
                beta=[2.71462, 4.69925], alpha=[-2.34174, 1.04009],
                etax=[0.0, 0.0])
        else:
            twiss_at_start = _pyacc_opt.Twiss.make_new(
                beta=[0.9328309787451605, 9.635141097929187],
                alpha=[0.877121666572456, -3.059132550219447],
                etax=[-0.05857309412506855, 0.0])

        strengths = {
            'qf2l': 12.37,
            'qd2l': -14.85,
            'qf3l': 5.713160289024,
            'qd1': -8.821809143987,
            'qf1': 13.335946597802,
            'qd2a': -11.859318300947,
            'qf2a': 14.532892396682,
            'qf2b': 8.647545577362,
            'qd2b': -8.836916532517,
            'qf3': 10.020651462368,
            'qd3': -4.974049498621,
            'qf4': 11.168208453391,
            'qd4': -6.191738912262,
            'injsept_kxl': 0.0,
            'injsept_kyl': 0.0,
            'injsept_ksxl': 0.0,
            'injsept_ksyl': 0.0,
        }

    elif optics_mode == 'M4':
        # Initial Conditions from Linac measured parameters on 16/07/2019
        # Linac second quadrupole triplet is used to match the LBT optics
        # (Sem tripleto)
        if add_from_li_triplets:
            twiss_at_start = _pyacc_opt.Twiss.make_new(
                beta=[2.71462, 4.69925], alpha=[-2.34174, 1.04009],
                etax=[0.0, 0.0])
        else:
            twiss_at_start = _pyacc_opt.Twiss.make_new(
                beta=[1.7650781208685327, 7.886431240236215],
                alpha=[1.1103521949355937, -2.139509773304648],
                etax=[-0.05857309412506855, 0.0])

        strengths = {
            'qf2l':  11.78860,
            'qd2l': -14.298290,
            'qf3l': 4.801910,
            'qd1': -8.822256368219,
            'qf1': 13.336060990905,
            'qd2a': -9.382785447106,
            'qf2a': 12.670391768958,
            'qf2b': 7.994238513566,
            'qd2b': -7.118805773505,
            'qf3': 10.328752039153,
            'qd3': -5.519539215470,
            'qf4': 11.635406805193,
            'qd4': -6.936225524796,
            'injsept_kxl': 0.0,
            'injsept_kyl': 0.0,
            'injsept_ksxl': 0.0,
            'injsept_ksyl': 0.0,
        }
    else:
        _pyacc_acc.AcceleratorException(
            'Invalid TB optics mode: ' + optics_mode)

    return strengths, twiss_at_start


def set_num_integ_steps(the_line):
    """Set number of integration steps in each lattice element."""
    dl = 0.035
    for i, _ in enumerate(the_line):
        if the_line[i].angle:
            length = the_line[i].length
            the_line[i].nr_steps = max(10, int(_math.ceil(length/dl)))
        elif the_line[i].polynom_b[1]:
            the_line[i].nr_steps = 10
        elif the_line[i].polynom_b[2]:
            the_line[i].nr_steps = 10
        else:
            the_line[i].nr_steps = 1

    ch_indices = _pyacc_lat.find_indices(the_line, 'fam_name', 'CHV')
    cv_indices = _pyacc_lat.find_indices(the_line, 'fam_name', 'CHV')
    qs_indices = _pyacc_lat.find_indices(the_line, 'fam_name', 'QS')
    corr_indices = ch_indices + cv_indices + qs_indices
    for idx in corr_indices:
        the_line[idx].nr_steps = 5


def set_vacuum_chamber(the_line):
    """Set vacuum chamber for all elements."""
    # -- default physical apertures --
    for i, _ in enumerate(the_line):
        the_line[i].hmin = -0.018
        the_line[i].hmax = +0.018
        the_line[i].vmin = -0.018
        the_line[i].vmax = +0.018

    # -- bo injection septum --
    beg = _pyacc_lat.find_indices(the_line, 'fam_name', 'bInjS')[0]
    end = _pyacc_lat.find_indices(the_line, 'fam_name', 'eInjS')[0]
    for i in range(beg, end+1):
        the_line[i].hmin = -0.0075
        the_line[i].hmax = +0.0075
        the_line[i].vmin = -0.0080
        the_line[i].vmax = +0.0080

    # -- dipoles --
    bnd = _pyacc_lat.find_indices(the_line, 'fam_name', 'B')
    for i in bnd:
        the_line[i].hmin = -0.0117
        the_line[i].hmax = +0.0117
        the_line[i].vmin = -0.0117
        the_line[i].vmax = +0.0117

    return the_line
