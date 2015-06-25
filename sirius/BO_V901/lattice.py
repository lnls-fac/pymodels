#!/usr/bin/env python3

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

    #correctors length
    c_length = 0.1 #Verificar tamanho real

    #kickers length
    k_length = 0.5

    # -- loads dipole segmented model --
    bd, b_len_seg, _b_model = dipole_segmented_model()
    b_len_hdedge            = 1.152; # [m]
    half_model_diff         = (b_len_seg - b_len_hdedge)/2.0

    lt       = drift('lt',      2.146000)
    lt2      = drift('lt2',     2.146000 - half_model_diff)
    l25      = drift('l25',     0.250000)
    l25_2    = drift('l25_2',   0.250000 - half_model_diff)
    l30_2    = drift('l30_2',   0.300000 - half_model_diff)
    l36      = drift('l36',     0.360000)
    l60      = drift('l60',     0.600000)
    l80      = drift('l80',     0.800000)
    l100     = drift('l100',    1.000000)
    lm25     = drift('lm25',    1.896000)
    lm30     = drift('lm30',    1.846000)
    lm45     = drift('lm45',    1.696000)
    lm60     = drift('lm60',    1.546000)
    lm66     = drift('lm66',    1.486000)
    lm70     = drift('lm70',    1.446000)
    lm100    = drift('lm100',   1.146000)
    lm105    = drift('lm105',   1.096000)
    sfus     = drift('sfus',    1.746000+0.05)
    sfds     = drift('sfds',    0.200000-0.05)

    l25c     = drift('l25c',    0.250000 - c_length/2.0)
    l30_2c   = drift('l30_2c',  0.300000 - half_model_diff - c_length/2.0)
    l80c     = drift('l80c',    0.800000 - c_length/2.0)
    lm25c    = drift('lm25c',   1.896000 - c_length/2.0)
    lm30c    = drift('lm30c',   1.846000 - c_length/2.0)
    lm66c    = drift('lm66c',   1.486000 - c_length/2.0)
    lm70c    = drift('lm70c',   1.446000 - c_length/2.0)

    l60k     = drift('l60k',    0.600000 - k_length/2.0)
    lm60k    = drift('lm60k',   1.546000 - k_length/2.0)
    lkk      = drift('lkk',     0.741000 - k_length)
    lm60_kk  = drift('lm60_kk', 0.805000 - k_length/2.0)

    start    = marker('start')   # start of the model
    fim      = marker('end')     # end of the model
    girder   = marker('girder')
    sept_in  = marker('sept_in')
    sept_ex  = marker('sept_ex')
    mqf      = marker('mqf')

    qd       = quadrupole('qd', 0.200000, strengths['qd'])
    qf       = quadrupole('qf', 0.100000, strengths['qf'])
    sf       = sextupole ('sf', 0.200000, strengths['sf'])
    sd       = sextupole ('sd', 0.200000, strengths['sd'])

    bpm      = marker('bpm')
    ch       = quadrupole('ch', c_length, 0.0)
    cv       = quadrupole('cv', c_length, 0.0)
    kick_in  = quadrupole('kick_in', k_length, 0.0)
    kick_ex  = quadrupole('kick_ex', k_length, 0.0)

    rfc = rfcavity('cav', 0, 0, 0) # RF frequency will be set later.

    b            = bd
    lfree        = lt
    lfree_2      = lt2
    lqd_2        = [lm45, qd, l25_2]
    lsd_2        = [lm45, sd, l25_2]
    lsf          = [sfus, sf, sfds]
    lch          = [lm25c, ch, l25c]
    lcv_2        = [lm30c, cv, l30_2c]
    lsdcv_2      = [lm70c, cv, l25c, sd, l25_2]
    fodo1        = [mqf, qf, lfree, girder, lfree_2, b,       lfree_2, girder, bpm, lsf, qf]
    fodo2        = [mqf, qf, lfree, girder, lqd_2,   b,   lcv_2[::-1], girder, bpm, lch, qf]
    fodo2sd      = [mqf, qf, lfree, girder, lqd_2,   b, lsdcv_2[::-1], girder, bpm, lch, qf]
    fodo1sd      = [mqf, qf, lfree, girder, lfree_2, b,   lsd_2[::-1], girder, bpm, lsf, qf]

    boos         = [fodo1sd, fodo2, fodo1, fodo2, fodo1, fodo2sd, fodo1, fodo2, fodo1, fodo2]
    lke          = [l60k, kick_ex, lkk, kick_ex, lm60_kk]
    lcvse_2      = [l36, sept_ex, lm66c, cv, l30_2c]
    lmon         = [l100, bpm, lm100]
    lsich        = [lm105, sept_in, l80c, ch, l25c]
    lki          = [l60k, kick_in, lm60k]
    fodo2kese    = [mqf, qf, lke,        girder, lqd_2,   b, lcvse_2[::-1], girder, lmon, qf]
    fodo2si      = [mqf, qf, lfree,      girder, lqd_2,   b,   lcv_2[::-1], girder, bpm, lsich, qf]
    fodo1ki      = [mqf, qf, lki,        girder, lfree_2, b,       lfree_2, girder, bpm, lsf, qf]
    fodo1ch      = [mqf, qf, lch[::-1],  girder, lfree_2, b,       lfree_2, girder, bpm, lsf, qf]
    fodo1rf      = [mqf, qf, lfree, rfc, girder, lfree_2, b,       lfree_2, girder, bpm, lsf, qf]

    #booster   = [boos, boos, boos, boos, boos]
    boosinj   = [fodo1sd, fodo2kese, fodo1ch, fodo2si, fodo1ki, fodo2sd, fodo1, fodo2, fodo1rf, fodo2]
    boosrf    = [fodo1sd, fodo2, fodo1, fodo2, fodo1, fodo2sd, fodo1, fodo2, fodo1, fodo2]
    boocor    = [start, boosinj, boos, boosrf, boos, boos, fim]
    elist     = boocor

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
    rho0   = 1.152*50/2/_math.pi
    U0 = 88.5*((energy*1e-9)**4/rho0)*1e3

    voltage_inj = 150e3 - overvoltage*(((88.5*(energy0*1e-9)**4)/rho0)*1e3)
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

    bends_vchamber = [0.0117, 0.0117]
    other_vchamber = [0.018,   0.018]

    for i in range(len(the_ring)):
        if the_ring[i].angle:
            the_ring[i].hmax = bends_vchamber[0]
            the_ring[i].vmax = bends_vchamber[1]
        elif the_ring[i].fam_name in ['mb', 'pb']:
            the_ring[i].hmax = bends_vchamber[0]
            the_ring[i].vmax = bends_vchamber[1]
        else:
            the_ring[i].hmax = other_vchamber[0]
            the_ring[i].vmax = other_vchamber[1]


def dipole_segmented_model():
    # dipole model 2014-12-01
    # =======================
    # this model is based on the same approved model6 dipole
    # new python script was used to derived integrated multipoles around
    # trajectory centered in good-field region. init_rx is set to +9.045 mm
    # falled back to 'solve' method for polynomial interpolation.
    b_model = _np.array([
        # len  angle                PolynomB[1]          PolynomB[2] ...
        [0.1960, +2.019543e-02, +0.000000e+00, -2.272773e-01, -1.983148e+00, -5.887754e+00, -3.025835e+02, -2.317689e+04, -7.875649e+05],
        [0.1920, +1.994573e-02, +0.000000e+00, -2.120079e-01, -1.926535e+00, -3.207544e+00, -1.203679e+02, -8.935228e+03, -4.719305e+05],
        [0.1580, +1.662526e-02, +0.000000e+00, -1.859618e-01, -1.882988e+00, -2.007607e-01, -1.432845e+02, +2.788161e+03, -1.791886e+05],
        [0.0340, +3.411849e-03, +0.000000e+00, -2.067510e-01, -1.851285e+00, -9.283365e+00, -1.011630e+03, +5.867357e+04, +9.576563e+05],
        [0.0300, +1.459518e-03, +0.000000e+00, -9.546626e-02, -1.722479e+00, +3.516586e+01, +3.371373e+02, -2.222028e+04, -2.863012e+06],
        [0.1580, +1.179063e-03, +0.000000e+00, +4.997853e-03, -7.327753e-01, +3.067168e+00, +6.866808e+01, -7.770617e+02, -2.591275e+05],
        [0.0010, +1.403307e-05, +9.722121e-07, +9.781965e-03, -6.822178e-01, +2.200638e+00, +5.710292e+02, -4.725951e+03, -1.263824e+06],
    ])
    marker, rbend = _pyaccel.elements.marker, _pyaccel.elements.rbend

    b = [];
    for i in range(b_model.shape[0]):
        b.append(rbend('b', length=b_model[i,0], angle=b_model[i,1], polynom_b=b_model[i,2:]))
    pb = marker('pb')
    mb = marker('mb')
    bd = [pb, b[::-1], mb, b, pb];
    b_length_segmented = 2*sum(b_model[:,0])

    return (bd, b_length_segmented, b_model)


_the_ring = create_lattice()
