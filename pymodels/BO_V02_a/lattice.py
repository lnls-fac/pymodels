#!/usr/bin/env python-sirius

import math as _math
import numpy as _np
import pyaccel as _pyaccel
import mathphys as _mp
from . import optics_mode_M0 as _optics_mode_M0


_default_optics_mode = _optics_mode_M0
_lattice_symmetry = 10
_harmonic_number  = 828
_energy = 0.15e9 #[eV]


def create_lattice(**kwargs):
    energy = kwargs['energy'] if 'energy' in kwargs else _energy

    # -- selection of optics mode --
    global _default_optics_mode
    _default_optics_mode = _optics_mode_M0

    # -- shortcut symbols --
    marker       = _pyaccel.elements.marker
    drift        = _pyaccel.elements.drift
    quadrupole   = _pyaccel.elements.quadrupole
    sextupole    = _pyaccel.elements.sextupole
    rbend_sirius = _pyaccel.elements.rbend
    rfcavity     = _pyaccel.elements.rfcavity
    hcorrector   = _pyaccel.elements.hcorrector
    vcorrector   = _pyaccel.elements.vcorrector
    strengths    = _default_optics_mode.strengths

    B, b_len_seg = dipole_segmented_model()
    b_len_hdedge = 1.152
    lenDif       = (b_len_seg - b_len_hdedge)/2.0

    L013377  = drift('l013377', 0.13377)
    L016118  = drift('l016118', 0.16118)
    L017241  = drift('l017241', 0.17241)
    L024100  = drift('l024100', 0.24100)
    L033627  = drift('l033627', 0.33627)
    L036000  = drift('l036000', 0.36000)
    L055500  = drift('l055500', 0.55500)
    L072491  = drift('l072491', 0.72491)
    L100000  = drift('l100000', 1.00000)
    L109600  = drift('l109600', 1.09600)
    L129600  = drift('l109600', 1.29600)
    L113227  = drift('l113227', 1.13227)
    L141091  = drift('l141091', 1.41091)
    L147091  = drift('l147091', 1.47091)
    L177091  = drift('l177091', 1.77091)
    L179350  = drift('l179350', 1.79350)
    L179563  = drift('l179563', 1.79563)
    L182091  = drift('l182091', 1.82091)
    L189350  = drift('l18935',  1.89350)
    L213227  = drift('l213227', 2.13227)

    # drifts affected by the dipole modelling:
    D024750 = drift('d024750',  0.24750-lenDif)
    D024963 = drift('d024963',  0.24963-lenDif)
    D214600 = drift('d214600',  2.14600-lenDif)
    D022491 = drift('d022491',  0.22491-lenDif)

    STR  = marker('start')     # start of the model
    FIM  = marker('end'  )     # end of the model
    GIR  = marker('girder')
    SIN  = marker('sept_in')
    SEX  = marker('sept_ex')
    MQF  = marker('mqf')
    BPM  = marker('bpm')

    KIN  = quadrupole('kick_in', 0.50000, 0.0)
    KEX  = quadrupole('kick_ex', 0.50000, 0.0)
    CH   = sextupole ('ch',      0.15018, 0.0)
    CV   = sextupole ('cv',      0.15018, 0.0)
    SF   = sextupole ('sf',      0.10500, strengths['sf'])
    SD   = sextupole ('sd',      0.10500, strengths['sd'])
    QD   = quadrupole('qd',      0.10074, strengths['qd'])
    QFI  = quadrupole('qf',      0.11373, strengths['qf'])
    QF   = [QFI,MQF,QFI]

    RFC = rfcavity('cav', 0, 0, 0) # RF frequency will be set later.

    UP_SF = [GIR, D214600, BPM,                           L189350, GIR, SF, L013377]
    UP_SS = [D024750, SD, GIR, L179350, BPM,              L189350, GIR, SF, L013377]
    UP_SI = [D022491, CV, GIR, L177091, BPM,              L109600, SIN, L072491, GIR, CH, L016118]
    UP_CS = [D024750, SD, L017241, CV, GIR, L147091, BPM, L182091, GIR, CH, L016118]
    UP_CC = [D022491, CV, GIR, L177091, BPM,              L182091, GIR, CH, L016118]
    UP_SE = [D022491, CV, GIR, L141091, SEX, L036000,     L100000, BPM, L113227, GIR]

    DW    = [GIR, L213227,                                D214600, GIR]
    DW_QD = [GIR, L213227,                                L179563, GIR, QD, D024963]
    DW_KE = [GIR, L033627, KEX, L024100, KEX, L055500,    L179563, GIR, QD, D024963]
    DW_RF = [GIR, L213227, RFC,                           D214600, GIR]
    DW_KI = [GIR, L033627, KIN, L129600,                  D214600, GIR]
    DW_CH = [L016118, CH, GIR, L182091,                   D214600, GIR]

    UP_01 = UP_SI;        DW_01 = DW_KI;        S01 = [UP_01, QFI, FIM, STR, MQF, QFI, DW_01, B]
    UP_02 = UP_SF;        DW_02 = DW_QD;        S02 = [UP_02, QF, DW_02, B]
    UP_03 = UP_CS;        DW_03 = DW;           S03 = [UP_03, QF, DW_03, B]
    UP_04 = UP_SF;        DW_04 = DW_QD;        S04 = [UP_04, QF, DW_04, B]
    UP_05 = UP_CC;        DW_05 = DW_RF;        S05 = [UP_05, QF, DW_05, B]
    UP_06 = UP_SF;        DW_06 = DW_QD;        S06 = [UP_06, QF, DW_06, B]
    UP_07 = UP_CC;        DW_07 = DW;           S07 = [UP_07, QF, DW_07, B]
    UP_08 = UP_SS;        DW_08 = DW_QD;        S08 = [UP_08, QF, DW_08, B]
    UP_09 = UP_CC;        DW_09 = DW;           S09 = [UP_09, QF, DW_09, B]
    UP_10 = UP_SF;        DW_10 = DW_QD;        S10 = [UP_10, QF, DW_10, B]
    UP_11 = UP_CC;        DW_11 = DW;           S11 = [UP_11, QF, DW_11, B]
    UP_12 = UP_SF;        DW_12 = DW_QD;        S12 = [UP_12, QF, DW_12, B]
    UP_13 = UP_CS;        DW_13 = DW;           S13 = [UP_13, QF, DW_13, B]
    UP_14 = UP_SF;        DW_14 = DW_QD;        S14 = [UP_14, QF, DW_14, B]
    UP_15 = UP_CC;        DW_15 = DW;           S15 = [UP_15, QF, DW_15, B]
    UP_16 = UP_SF;        DW_16 = DW_QD;        S16 = [UP_16, QF, DW_16, B]
    UP_17 = UP_CC;        DW_17 = DW;           S17 = [UP_17, QF, DW_17, B]
    UP_18 = UP_SS;        DW_18 = DW_QD;        S18 = [UP_18, QF, DW_18, B]
    UP_19 = UP_CC;        DW_19 = DW;           S19 = [UP_19, QF, DW_19, B]
    UP_20 = UP_SF;        DW_20 = DW_QD;        S20 = [UP_20, QF, DW_20, B]
    UP_21 = UP_CC;        DW_21 = DW;           S21 = [UP_21, QF, DW_21, B]
    UP_22 = UP_SF;        DW_22 = DW_QD;        S22 = [UP_22, QF, DW_22, B]
    UP_23 = UP_CS;        DW_23 = DW;           S23 = [UP_23, QF, DW_23, B]
    UP_24 = UP_SF;        DW_24 = DW_QD;        S24 = [UP_24, QF, DW_24, B]
    UP_25 = UP_CC;        DW_25 = DW;           S25 = [UP_25, QF, DW_25, B]
    UP_26 = UP_SF;        DW_26 = DW_QD;        S26 = [UP_26, QF, DW_26, B]
    UP_27 = UP_CC;        DW_27 = DW;           S27 = [UP_27, QF, DW_27, B]
    UP_28 = UP_SS;        DW_28 = DW_QD;        S28 = [UP_28, QF, DW_28, B]
    UP_29 = UP_CC;        DW_29 = DW;           S29 = [UP_29, QF, DW_29, B]
    UP_30 = UP_SF;        DW_30 = DW_QD;        S30 = [UP_30, QF, DW_30, B]
    UP_31 = UP_CC;        DW_31 = DW;           S31 = [UP_31, QF, DW_31, B]
    UP_32 = UP_SF;        DW_32 = DW_QD;        S32 = [UP_32, QF, DW_32, B]
    UP_33 = UP_CS;        DW_33 = DW;           S33 = [UP_33, QF, DW_33, B]
    UP_34 = UP_SF;        DW_34 = DW_QD;        S34 = [UP_34, QF, DW_34, B]
    UP_35 = UP_CC;        DW_35 = DW;           S35 = [UP_35, QF, DW_35, B]
    UP_36 = UP_SF;        DW_36 = DW_QD;        S36 = [UP_36, QF, DW_36, B]
    UP_37 = UP_CC;        DW_37 = DW;           S37 = [UP_37, QF, DW_37, B]
    UP_38 = UP_SS;        DW_38 = DW_QD;        S38 = [UP_38, QF, DW_38, B]
    UP_39 = UP_CC;        DW_39 = DW;           S39 = [UP_39, QF, DW_39, B]
    UP_40 = UP_SF;        DW_40 = DW_QD;        S40 = [UP_40, QF, DW_40, B]
    UP_41 = UP_CC;        DW_41 = DW;           S41 = [UP_41, QF, DW_41, B]
    UP_42 = UP_SF;        DW_42 = DW_QD;        S42 = [UP_42, QF, DW_42, B]
    UP_43 = UP_CS;        DW_43 = DW;           S43 = [UP_43, QF, DW_43, B]
    UP_44 = UP_SF;        DW_44 = DW_QD;        S44 = [UP_44, QF, DW_44, B]
    UP_45 = UP_CC;        DW_45 = DW;           S45 = [UP_45, QF, DW_45, B]
    UP_46 = UP_SF;        DW_46 = DW_QD;        S46 = [UP_46, QF, DW_46, B]
    UP_47 = UP_CC;        DW_47 = DW;           S47 = [UP_47, QF, DW_47, B]
    UP_48 = UP_SS;        DW_48 = DW_KE;        S48 = [UP_48, QF, DW_48, B]
    UP_49 = UP_SE;        DW_49 = DW_CH;        S49 = [UP_49, QF, DW_49, B]
    UP_50 = UP_SF;        DW_50 = DW_QD;        S50 = [UP_50, QF, DW_50, B]


    elist = [S01,S02,S03,S04,S05,S06,S07,S08,S09,S10,
             S11,S12,S13,S14,S15,S16,S17,S18,S19,S20,
             S21,S22,S23,S24,S25,S26,S27,S28,S29,S30,
             S31,S32,S33,S34,S35,S36,S37,S38,S39,S40,
             S41,S42,S43,S44,S45,S46,S47,S48,S49,S50]

    the_ring = _pyaccel.lattice.build(elist)

    # -- shifts model to marker 'start'
    idx = _pyaccel.lattice.find_indices(the_ring, 'fam_name', 'start')
    the_ring = _pyaccel.lattice.shift(the_ring, idx[0])

    # -- sets rf frequency
    set_rf_frequency(the_ring)

    # -- sets rf voltage
    set_rf_voltage(the_ring, energy)

    # -- sets number of integration steps
    set_num_integ_steps(the_ring)

    # -- define vacuum chamber for all elements
    set_vacuum_chamber(the_ring)

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


def set_num_integ_steps(the_ring):

    bends = []
    for i in range(len(the_ring)):
        if the_ring[i].angle:
            bends.append(i)

    len_b  = 3e-2
    len_qs = 1.5e-2

    for i in range(len(the_ring)):
        if the_ring[i].angle:
            nr_steps = int( _math.ceil(the_ring[i].length/len_b))
            the_ring[i].nr_steps = nr_steps
        elif any(the_ring[i].polynom_b) and i not in bends:
            nr_steps = int( _math.ceil(the_ring[i].length/len_qs))
            the_ring[i].nr_steps = nr_steps


def set_vacuum_chamber(the_ring):

    # vchamber = [hmin, hmax, vmin, vmax]
    bends_vchamber      = [-0.0117, 0.0117, -0.0117, 0.0117]
    other_vchamber      = [-0.018,   0.018,  -0.018,  0.018]
    extraction_vchamber = [-0.018,   0.026,  -0.018,  0.018]

    sept_in = _pyaccel.lattice.find_indices(the_ring, 'fam_name', 'sept_in')[0]
    kick_in = _pyaccel.lattice.find_indices(the_ring, 'fam_name', 'kick_in')[0]

    b = _np.array(_pyaccel.lattice.find_indices(the_ring, 'fam_name', 'b'))
    sept_ex = _pyaccel.lattice.find_indices(the_ring, 'fam_name', 'sept_ex')[0]
    kick_ex = _pyaccel.lattice.find_indices(the_ring, 'fam_name', 'kick_ex')[0]
    b_ex = b[b > kick_ex]; b_ex = b_ex[b_ex < sept_ex]

    for i in range(len(the_ring)):
        if the_ring[i].angle:
            the_ring[i].hmin = bends_vchamber[0]
            the_ring[i].hmax = bends_vchamber[1]
            the_ring[i].vmin = bends_vchamber[2]
            the_ring[i].vmax = bends_vchamber[3]
        elif the_ring[i].fam_name in ['mb']:
            the_ring[i].hmin = bends_vchamber[0]
            the_ring[i].hmax = bends_vchamber[1]
            the_ring[i].vmin = bends_vchamber[2]
            the_ring[i].vmax = bends_vchamber[3]
        else:
            the_ring[i].hmin = other_vchamber[0]
            the_ring[i].hmax = other_vchamber[1]
            the_ring[i].vmin = other_vchamber[2]
            the_ring[i].vmax = other_vchamber[3]

    # vaccum chamber on the injection section
    for i in range(sept_in, len(the_ring)):
        the_ring[i].hmin = -0.05 # Verificar valor real
    for i in range(kick_in):
        the_ring[i].hmin = -0.05 # Verificar valor real

    # vaccum chamber on the extraction section
    for i in range(b_ex[0], b_ex[-1]+1): # Verificar
        the_ring[i].hmin = other_vchamber[0]
        the_ring[i].hmax = other_vchamber[1]
        the_ring[i].vmin = other_vchamber[2]
        the_ring[i].vmax = other_vchamber[3]
    for i in range(b_ex[-1], sept_ex +1):
        the_ring[i].hmin = extraction_vchamber[0]
        the_ring[i].hmax = extraction_vchamber[1]
        the_ring[i].vmin = extraction_vchamber[2]
        the_ring[i].vmax = extraction_vchamber[3]


def dipole_segmented_model():

    d2r = _math.pi/180.0

    # dipole model 2015-09-16
    # =======================
    # this model is based on the same approved model6 dipole
    # new python script was used to derived integrated multipoles around
    # trajectory centered in good-field region. init_rx is set to +9.045 mm
    # *** intertpolation of fields is now cubic ***
    # *** dipole angles were normalized to better close 360 degrees ***
    #--- model polynom_b (rz > 0). units: [m] for length, [rad] for angle and [m],[T] for polynom_b ---
    b_model = _np.array([
    #len[m]   angle[rad]     PolynomB(n=0)   PolynomB(n=1)   PolynomB(n=2)   PolynomB(n=3)   PolynomB(n=4)   PolynomB(n=5)   PolynomB(n=6)
    [0.1960,  d2r* 1.1572,  +0.000000e+00,  -2.272565e-01,  -1.982429e+00,  -6.357730e+00,  -3.090667e+02,  -2.050288e+04,  -7.485474e+05],
    [0.1920,  d2r* 1.1428,  +0.000000e+00,  -2.119941e-01,  -1.926460e+00,  -3.535411e+00,  -1.182766e+02,  -7.140587e+03,  -4.763814e+05],
    [0.1580,  d2r* 0.9526,  +0.000000e+00,  -1.859630e-01,  -1.881590e+00,  -1.730076e-01,  -1.650540e+02,  +2.652761e+03,  -8.366171e+04],
    [0.0340,  d2r* 0.1955,  +0.000000e+00,  -2.077807e-01,  -1.948986e+00,  +7.187891e+00,  -2.640959e+02,  +6.127578e+03,  -3.988633e+05],
    [0.0300,  d2r* 0.0836,  +0.000000e+00,  -9.481689e-02,  -1.587599e+00,  +2.464462e+01,  -8.268328e+02,  +1.074123e+04,  -3.337856e+05],
    [0.1580,  d2r* 0.0675,  +0.000000e+00,  +5.004115e-03,  -7.199178e-01,  +2.971617e+00,  -5.090294e+01,  -4.863955e+02,  +2.188990e+04],
    [0.0010,  d2r* 0.0008,  -4.984551e-04,  +1.062454e-02,  -6.308172e-01,  -4.353379e-01,  +1.842258e+01,  +8.052845e+00,  -4.619714e+02],
    ])

    marker, rbend = _pyaccel.elements.marker, _pyaccel.elements.rbend

    b = []
    for i in range(b_model.shape[0]):
        b.append(rbend('b', length=b_model[i,0], angle=b_model[i,1], polynom_b=b_model[i,2:]))
    pb = marker('pb')
    mb = marker('mb')
    bd = [pb, b[::-1] , mb, b, pb]
    b_length_segmented = 2*sum(b_model[:,0])

    return (bd, b_length_segmented)
