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
_family_segmentation={ 'b'  : 14, 'qf' : 2, 'qd' : 1, 'sd' : 1,
                       'sf' : 1, 'bpm' : 1, 'ch' : 1, 'cv' : 1 }

def create_lattice(**kwargs):

    energy = kwargs['energy'] if 'energy' in kwargs else _energy

    if energy == 0.15e9:
        rf_voltage = 150e3
    else:
        rf_voltage = 950e3

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

    rfc = rfcavity('cav', 0, rf_voltage, 0) # RF frequency will be set later.

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
    boosinj   = [fodo1sd, fodo2kese, fodo1ch, fodo2si, fodo1ki, fodo2sd, fodo1, fodo2, fodo1, fodo2]
    boosrf    = [fodo1sd, fodo2, fodo1, fodo2, fodo1rf, fodo2sd, fodo1, fodo2, fodo1, fodo2]
    boocor    = [start, boosinj, boos, boosrf, boos, boos, fim]
    elist     = boocor

    the_ring = _pyaccel.lattice.build(elist)

    # -- shifts model to marker 'start'
    idx = _pyaccel.lattice.find_indices(the_ring, 'fam_name', 'start')
    the_ring = _pyaccel.lattice.shift(the_ring, idx[0])

    # -- sets rf frequency
    set_rf_frequency(the_ring, energy)

    # -- sets number of integration steps
    set_num_integ_steps(the_ring)

    # -- define vacuum chamber for all elements
    set_vacuum_chamber(the_ring)

    return the_ring


def set_rf_frequency(the_ring, energy):

    circumference = _pyaccel.lattice.length(the_ring)

    #_, beam_velocity, _, _, _ = _mp.beam_optics.beam_rigidity(energy=_energy)
    #velocity = beam_velocity
    velocity = _mp.constants.light_speed
    rev_frequency = velocity / circumference
    rf_frequency  = _harmonic_number * rev_frequency
    idx = _pyaccel.lattice.find_indices(the_ring, 'fam_name', 'cav')
    for i in idx:
        the_ring[i].frequency = rf_frequency


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

    # dipole model 2014-10-19
    # =======================
    # this model is based on the same approved model6 dipole
    # new python script was used to derived integrated multipoles around
    # trajectory centered in good-field region. init_rx is set to +9.045 mm
    # model segmentation was preserved (14) but multipoles were rescaled
    # from previous integrated values to new ones.
    # b_model = [ ...
    # # len                angle                PolynomB[1]          PolynomB[2] ...
    # +1.9600000000000E-01 +2.0195440847176E-02 +0.0000000000000E+00 -2.2718737794240E-01 -1.9838101973556E+00 -6.7100381692044E+00 +4.9920710941460E-05 -1.3300435827537E-04 +2.4235784274106E-08;...
    # +1.9200000000000E-01 +1.9945732400886E-02 +0.0000000000000E+00 -2.1192778004400E-01 -1.9172568031810E+00 -3.7354632993019E+00 -1.9634481701885E-05 -4.9798831271698E-05 +3.4371169036436E-09;...
    # +1.5800000000000E-01 +1.6625265049598E-02 +0.0000000000000E+00 -1.8590486931855E-01 -1.8737337003164E+00 -1.6541302326730E-01 -1.9338306308259E-05 +1.2255709898644E-05 +4.1512320572352E-09;...
    # +3.4000000000000E-02 +3.4121780697475E-03 +0.0000000000000E+00 -2.0790741807102E-01 -1.9108616811517E+00 +6.0211592722707E+00 -8.0389504785605E-04 +4.2587366778860E-04 -2.0493449755724E-07;...
    # +3.0000000000000E-02 +1.4593537587502E-03 +0.0000000000000E+00 -9.5038400635701E-02 -1.6494710898138E+00 +2.5462042127288E+01 +9.5248097990464E-04 +3.3179449011173E-05 +3.3304203270259E-07;...
    # +1.5800000000000E-01 +1.1796180861276E-03 +0.0000000000000E+00 +4.8538016476408E-03 -7.1806104227790E-01 +3.1726318161202E+00 -2.1836064393780E-05 -7.5534836079246E-06 -2.5720679947909E-09;...
    # +1.0000000000000E-03 +1.4264859509966E-05 +4.1405772719342E-05 +3.0576641299928E-02 -8.2104840247350E+00 -1.3034706925023E+02 -4.3041809412239E-02 -1.1076703523835E-02 -1.0030203613377E-05;...
    # ];

    # # dipole model 2014-10-19
    # # =======================
    # # this model is based on the same approved model6 dipole
    # # new python script was used to derived integrated multipoles around
    # # trajectory centered in good-field region.
    # # model segmentation was preserved (14) but multipoles were rescaled
    # # from previous integrated values to new ones.
    # b_model = [ ...
    # # len               angle               PolynomB[1]         PolynomB[2] ...
    # 1.9600000000000E-01	2.0195440847176E-02	0.0000000000000E+00	-2.2498523857624E-01	-1.9838101973556E+00	-3.8395034249638E+00	 4.9897118923000E-05	-7.6114588512000E-05	 2.4217805205700E-04; ...
    # 1.9200000000000E-01	1.9945732400886E-02	0.0000000000000E+00	-2.0987355277378E-01	-1.9172568031810E+00	-2.1374430025332E+00	-1.9625202646000E-05	-2.8498446214000E-05	 3.4345671137000E-05; ...
    # 1.5800000000000E-01	1.6625265049598E-02	0.0000000000000E+00	-1.8410288350933E-01	-1.8737337003164E+00	-9.4649814703477E-02	-1.9329167222000E-05	 7.0135920950000E-06	 4.1481525082000E-05; ...
    # 3.4000000000000E-02	3.4121780697475E-03	0.0000000000000E+00	-2.0589216038374E-01	-1.9108616811517E+00	 3.4453249095120E+00	-8.0351513526300E-04	 2.4371531431000E-04	-2.0478246899820E-03; ...
    # 3.0000000000000E-02	1.4593537587502E-03	0.0000000000000E+00	-9.4117188351673E-02	-1.6494710898138E+00	 1.4569454821132E+01	 9.5203084711600E-04	 1.8987649287000E-05	 3.3279496888010E-03; ...
    # 1.5800000000000E-01	1.1796180861276E-03	0.0000000000000E+00	 4.8067534895050E-03	-7.1806104227791E-01	 1.8153891851240E+00	-2.1825744893000E-05	-4.3226425370000E-06	-2.5701599325000E-05; ...
    # 1.0000000000000E-03	1.4264859509966E-05	4.1405772719342E-05	 3.0280260285713E-02	-8.2104840247351E+00	-7.4584973468129E+01	-4.3021468292479E-02	-6.3388804826660E-03	-1.0022762809510E-01; ...
    # ];

    # # dipole model
    # # ============
    # # this model is based on the same approved model6 dipole
    # # from matlab-derived fieldmap analysis
    # b_model = [ ...
    # # len               angle                 PolynomB[1]          PolynomB[2] ...
    # +1.9600000000000E-01 +2.0195440847176E-02 +0.0000000000000E+00 -2.2725730095568E-01 -1.9937933516712E+00 -6.4749558242816E+00 +2.1792245824426E+02 -2.0052690828560E+04 -7.4402792791901E+06; ...
    # +1.9200000000000E-01 +1.9945732400886E-02 +0.0000000000000E+00 -2.1199300650646E-01 -1.9269050399702E+00 -3.6045934816304E+00 -8.5711810551822E+01 -7.5080289102069E+03 -1.0551797865958E+06; ...
    # +1.5800000000000E-01 +1.6625265049598E-02 +0.0000000000000E+00 -1.8596208653178E-01 -1.8831629152189E+00 -1.5961787271676E-01 -8.4418894873476E+01 +1.8477587100809E+03 -1.2744100008992E+06; ...
    # +3.4000000000000E-02 +3.4121780697475E-03 +0.0000000000000E+00 -2.0797140715917E-01 -1.9204777356836E+00 +5.8102114050328E+00 -3.5093006829292E+03 +6.4207768098161E+04 +6.2913990260072E+07; ...
    # +3.0000000000000E-02 +1.4593537587502E-03 +0.0000000000000E+00 -9.5067651254331E-02 -1.6577717450130E+00 +2.4569994061559E+01 +4.1579335040946E+03 +5.0023716629309E+03 -1.0224244064030E+08; ...
    # +1.5800000000000E-01 +1.1796180861276E-03 +0.0000000000000E+00 +4.8552955353741E-03 -7.2167455036586E-01 +3.0614804771706E+00 -9.5322537306261E+01 -1.1388173548021E+03 +7.8961357263592E+05; ...
    # +1.0000000000000E-03 +1.4264859509966E-05 +4.1405772719342E-05 +3.0586052081966E-02 -8.2518017521740E+00 -1.2578043431903E+02 -1.8789349625640E+05 -1.6700032543536E+06 +3.0792284362095E+09; ...
    # ];

    marker, rbend = _pyaccel.elements.marker, _pyaccel.elements.rbend

    b = [];
    for i in range(b_model.shape[0]):
        b.append(rbend('b', length=b_model[i,0], angle=b_model[i,1], polynom_b=b_model[i,2:]))
    pb = marker('pb')
    mb = marker('mb')
    bd = [pb, b[::-1], mb, b, pb];
    b_length_segmented = 2*sum(b_model[:,0])

    return (bd, b_length_segmented, b_model)


def sirius_bo_family_data(lattice):
    latt_dict=_pyaccel.lattice.find_dict(lattice,'fam_name')
    data={}

    for key in latt_dict.keys():
        if key in _family_segmentation.keys():
            data[key] = {'index' : latt_dict[key], 'nr_segs' : _family_segmentation[key] , 'families' : key}

    for key in data.keys():
        if key == 'qf':
            idx=data[key]['index'].pop()
            data[key]['index'].insert(0,idx)

        if data[key]['nr_segs'] != 1:
            new_index = []
            j = 0
            for i in range(len(data[key]['index'])//data[key]['nr_segs']):
                new_index.append(data[key]['index'][j:j+data[key]['nr_segs']])
                j += data[key]['nr_segs']
            data[key]['index'] = new_index

    return data

_the_ring = create_lattice()
_family_data = sirius_bo_family_data(_the_ring)
