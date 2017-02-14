#!/usr/bin/env python3

import math as _math
import numpy as _np
import pyaccel as _pyaccel
import mathphys as _mp
from . import segmented_models as _seg_models


default_optics_mode = 'M0'
lattice_symmetry = 10
harmonic_number  = 828
energy = 0.15e9 #[eV]
_d2r = _math.pi/180.0


def create_lattice(**kwargs):

    # -- shortcut symbols --
    marker       = _pyaccel.elements.marker
    drift        = _pyaccel.elements.drift
    quadrupole   = _pyaccel.elements.quadrupole
    sextupole    = _pyaccel.elements.sextupole
    rfcavity     = _pyaccel.elements.rfcavity
    hcorrector   = _pyaccel.elements.hcorrector
    vcorrector   = _pyaccel.elements.vcorrector


    energy = kwargs['energy'] if 'energy' in kwargs else energy
    optics_mode = kwargs['optics_mode'] if 'optics_mode' in kwargs else default_optics_mode

    strengths = get_optics_mode(optics_mode,energy)

    B, b_len_seg = _seg_models.dipole(energy)
    b_len_hdedge = 1.152
    lenDif       = (b_len_seg - b_len_hdedge)/2.0

    # ----- DRIFTS ----
    L00880  = drift('l00880', 0.0880)
    L01335  = drift('l01335', 0.1335)
    L01360  = drift('l01360', 0.1360)
    L01610  = drift('l01610', 0.1610)
    L01675  = drift('l01675', 0.1675)
    L01725  = drift('l01725', 0.1725)
    L02500  = drift('l02500', 0.2500)
    L03500  = drift('l03500', 0.3500)
    L03860  = drift('l03860', 0.3860)
    L04500  = drift('l04500', 0.4500)
    L06200  = drift('l06200', 0.6200)
    L07250  = drift('l07250', 0.7250)
    L10960  = drift('l10960', 1.0960)
    L10000  = drift('l10000', 1.0000)
    L10960  = drift('l10960', 1.0960)
    L11320  = drift('l11320', 1.1320)
    L13460  = drift('l13460', 1.3460)
    L14460  = drift('l14460', 1.4460)
    L14710  = drift('l14710', 1.4710)
    L15120  = drift('l15120', 1.5120)
    L16830  = drift('l16830', 1.6830)
    L17260  = drift('l17260', 1.7260)
    L17710  = drift('l17710', 1.7710)
    L17935  = drift('l17935', 1.7935)
    L17960  = drift('l17960', 1.7960)
    L18210  = drift('l18210', 1.8210)
    L18935  = drift('l18935', 1.8935)
    L18960  = drift('l18960', 1.8960)
    L21320  = drift('l21320', 2.1320)

    # drifts affected by the dipole modelling:
    D02250 = drift('d02250',  0.2250-lenDif)
    D02475 = drift('d02475',  0.2475-lenDif)
    D02500 = drift('d02500',  0.2500-lenDif)
    D17960 = drift('d17960',  1.7960-lenDif)
    D21460 = drift('d21460',  2.1460-lenDif)

    STR  = marker('start')     # start of the model
    FIM  = marker('end'  )     # end of the model
    GIR  = marker('girder')

    SIN  = marker('InjS')
    SEX  = marker('EjeSF')

    DCCT = marker('DCCT')
    BPM  = marker('BPM')
    Scrn = marker('Scrn')
    TuneP= marker('TuneP')
    TuneS= marker('TuneS')
    GSL  = marker('GSL')

    KIN  = quadrupole('InjK', 0.40000, 0.0)
    KEX  = quadrupole('EjeK', 0.40000, 0.0)
    CH   = sextupole ('CH',   0.150, 0.0)
    CV   = sextupole ('CV',   0.150, 0.0)

    SF,_  = _seg_models.sx_sextupole(energy, 'SF', strengths['sf'] * 0.105)
    SD,_  = _seg_models.sx_sextupole(energy, 'SD', strengths['sd'] * 0.105)

    QD,_  = _seg_models.qd_quadrupole(energy, 'QD', strengths['qd'] * 0.100)
    QF,_  = _seg_models.qf_quadrupole(energy, 'QF', strengths['qf'] * 0.228)
    QS    = quadrupole('QS', 0.10, 0.0)
    QF0   = [QF[0], FIM, STR, QF[1:]]

    RFC = rfcavity('RFCav', 0, 0, 0) # RF frequency will be set later.


    US_SF      = [GIR, D21460, BPM,                            L18935, GIR, SF, L01335]
    US_CS      = [D02475, SD, L01725, CV, GIR, L14710, BPM,    L18210, GIR, CH, L01610]
    US_CC      = [D02250, CV, GIR, L17710, BPM,                L18210, GIR, CH, L01610]
    US_SS      = [D02475, SD, GIR, L17935, BPM,                L18935, GIR, SF, L01335]
    US_SF_Scrn = [GIR, D21460, BPM,                            L17260, GIR, Scrn, L01675, SF, L01335]
    US_SE      = [D02250, CV, GIR, L16830, SEX, L00880,        L10000, BPM, L11320, GIR]
    US_SI      = [D02250, CV, GIR, L17710, BPM,                L10960, SIN, L07250, GIR, CH, L01610]
    US_SF_GSL  = [GIR, D17960, GSL, L03500, BPM,               L18935, GIR, SF, L01335]

    DS         = [GIR, L21320,                                 D21460, GIR]
    DS_QD      = [GIR, L21320,                                 L17960, GIR, QD, D02500]
    DS_RF      = [GIR, L21320, RFC,                            D21460, GIR]
    DS_KE      = [GIR, L03860, KEX, L13460,                    L17960, GIR, QD, D02500]
    DS_CH      = [L01610, CH, GIR, L18210,                     D21460, GIR]
    DS_KI      = [GIR, L03860, KIN, L02500, Scrn, L10960,      L18960, Scrn, D02500, GIR]
    DS_QS_TuS  = [L01360, QS, GIR, L14460, TuneS, L04500,      L17960, GIR, QD, D02500]
    DS_DCCT    = [GIR, L21320,  DCCT,                          D21460, GIR]
    DS_QD_TuP  = [GIR, L15120, TuneP, L06200,                  L17960, GIR, QD, D02500]


    US_01 = US_SI;        DS_01 = DS_KI;        S01 = [US_01, QF0,DS_01, B];
    US_02 = US_SF_Scrn;   DS_02 = DS_QS_TuS;    S02 = [US_02, QF, DS_02, B];
    US_03 = US_CS;        DS_03 = DS;           S03 = [US_03, QF, DS_03, B];
    US_04 = US_SF_GSL;    DS_04 = DS_QD_TuP;    S04 = [US_04, QF, DS_04, B];
    US_05 = US_CC;        DS_05 = DS_RF;        S05 = [US_05, QF, DS_05, B];
    US_06 = US_SF;        DS_06 = DS_QD;        S06 = [US_06, QF, DS_06, B];
    US_07 = US_CC;        DS_07 = DS;           S07 = [US_07, QF, DS_07, B];
    US_08 = US_SS;        DS_08 = DS_QD;        S08 = [US_08, QF, DS_08, B];
    US_09 = US_CC;        DS_09 = DS;           S09 = [US_09, QF, DS_09, B];
    US_10 = US_SF;        DS_10 = DS_QD;        S10 = [US_10, QF, DS_10, B];
    US_11 = US_CC;        DS_11 = DS;           S11 = [US_11, QF, DS_11, B];
    US_12 = US_SF;        DS_12 = DS_QD;        S12 = [US_12, QF, DS_12, B];
    US_13 = US_CS;        DS_13 = DS;           S13 = [US_13, QF, DS_13, B];
    US_14 = US_SF;        DS_14 = DS_QD;        S14 = [US_14, QF, DS_14, B];
    US_15 = US_CC;        DS_15 = DS;           S15 = [US_15, QF, DS_15, B];
    US_16 = US_SF;        DS_16 = DS_QD;        S16 = [US_16, QF, DS_16, B];
    US_17 = US_CC;        DS_17 = DS;           S17 = [US_17, QF, DS_17, B];
    US_18 = US_SS;        DS_18 = DS_QD;        S18 = [US_18, QF, DS_18, B];
    US_19 = US_CC;        DS_19 = DS;           S19 = [US_19, QF, DS_19, B];
    US_20 = US_SF;        DS_20 = DS_QD;        S20 = [US_20, QF, DS_20, B];
    US_21 = US_CC;        DS_21 = DS;           S21 = [US_21, QF, DS_21, B];
    US_22 = US_SF;        DS_22 = DS_QD;        S22 = [US_22, QF, DS_22, B];
    US_23 = US_CS;        DS_23 = DS;           S23 = [US_23, QF, DS_23, B];
    US_24 = US_SF;        DS_24 = DS_QD;        S24 = [US_24, QF, DS_24, B];
    US_25 = US_CC;        DS_25 = DS;           S25 = [US_25, QF, DS_25, B];
    US_26 = US_SF;        DS_26 = DS_QD;        S26 = [US_26, QF, DS_26, B];
    US_27 = US_CC;        DS_27 = DS;           S27 = [US_27, QF, DS_27, B];
    US_28 = US_SS;        DS_28 = DS_QD;        S28 = [US_28, QF, DS_28, B];
    US_29 = US_CC;        DS_29 = DS;           S29 = [US_29, QF, DS_29, B];
    US_30 = US_SF;        DS_30 = DS_QD;        S30 = [US_30, QF, DS_30, B];
    US_31 = US_CC;        DS_31 = DS;           S31 = [US_31, QF, DS_31, B];
    US_32 = US_SF;        DS_32 = DS_QD;        S32 = [US_32, QF, DS_32, B];
    US_33 = US_CS;        DS_33 = DS;           S33 = [US_33, QF, DS_33, B];
    US_34 = US_SF;        DS_34 = DS_QD;        S34 = [US_34, QF, DS_34, B];
    US_35 = US_CC;        DS_35 = DS_DCCT;      S35 = [US_35, QF, DS_35, B];
    US_36 = US_SF;        DS_36 = DS_QD;        S36 = [US_36, QF, DS_36, B];
    US_37 = US_CC;        DS_37 = DS;           S37 = [US_37, QF, DS_37, B];
    US_38 = US_SS;        DS_38 = DS_QD;        S38 = [US_38, QF, DS_38, B];
    US_39 = US_CC;        DS_39 = DS;           S39 = [US_39, QF, DS_39, B];
    US_40 = US_SF;        DS_40 = DS_QD;        S40 = [US_40, QF, DS_40, B];
    US_41 = US_CC;        DS_41 = DS;           S41 = [US_41, QF, DS_41, B];
    US_42 = US_SF;        DS_42 = DS_QD;        S42 = [US_42, QF, DS_42, B];
    US_43 = US_CS;        DS_43 = DS;           S43 = [US_43, QF, DS_43, B];
    US_44 = US_SF;        DS_44 = DS_QD;        S44 = [US_44, QF, DS_44, B];
    US_45 = US_CC;        DS_45 = DS;           S45 = [US_45, QF, DS_45, B];
    US_46 = US_SF;        DS_46 = DS_QD;        S46 = [US_46, QF, DS_46, B];
    US_47 = US_CC;        DS_47 = DS;           S47 = [US_47, QF, DS_47, B];
    US_48 = US_SS;        DS_48 = DS_KE;        S48 = [US_48, QF, DS_48, B];
    US_49 = US_SE;        DS_49 = DS_CH;        S49 = [US_49, QF, DS_49, B];
    US_50 = US_SF;        DS_50 = DS_QD;        S50 = [US_50, QF, DS_50, B];


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


def get_optics_mode(optics_mode,energy=energy):

    if optics_mode == 'M0':
        # 2017-01-11 ximenes (overall checking of model - quadrupole qd model 02)
        # tunes fitted to [19.20433 7.31417] with "[THERING, conv, t2, t1] = lnls_correct_tunes(THERING,[19.20433 7.31417],{'QF','QD'},'svd','add',10,1e-9)"
        # chroms fitted to [0.5 0.5] with "THERING = fitchrom2(THERING, [0.5, 0.5], 'SD', 'SF')"
        # effective length changed from 227 mm to 228 mm.
        # added model data for injection energy (2016-12-06 - ximenes)
        qf_high_en = 1.654036900448982
        qd_high_en = -0.005474886350700
        sf_high_en = 11.326236792215228
        sd_high_en = 6.282586036135388

        qf_low_en = 1.653947031926041
        qd_low_en = 0.011197961538728  # this is correct! the sign has changed!
        sf_low_en = 11.331918124055948
        sd_low_en = 5.007982970980575
    else:
        raise Exception('Optics mode not recognized.')

    coeff = (energy-0.15e9)/(3e9-0.15e9)
    strengths = {
        'qf' : qf_low_en + coeff*(qf_high_en - qf_low_en),
        'qd' : qd_low_en + coeff*(qd_high_en - qd_low_en),
        'sf' : sf_low_en + coeff*(sf_high_en - sf_low_en),
        'sd' : sd_low_en + coeff*(sd_high_en - sd_low_en),
    }
    return strengths

def set_rf_frequency(the_ring):

    circumference = _pyaccel.lattice.length(the_ring)
    velocity = _mp.constants.light_speed
    rev_frequency = velocity / circumference
    rf_frequency  = harmonic_number * rev_frequency
    idx = _pyaccel.lattice.find_indices(the_ring, 'fam_name', 'Cav')
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

    idx = _pyaccel.lattice.find_indices(the_ring, 'fam_name', 'Cav')
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

    sept_in = _pyaccel.lattice.find_indices(the_ring, 'fam_name', 'InjS')[0]
    kick_in = _pyaccel.lattice.find_indices(the_ring, 'fam_name', 'InjK')[0]

    b = _np.array(_pyaccel.lattice.find_indices(the_ring, 'fam_name', 'B'))
    sept_ex = _pyaccel.lattice.find_indices(the_ring, 'fam_name', 'EjeSF')[0]
    kick_ex = _pyaccel.lattice.find_indices(the_ring, 'fam_name', 'EjeK')[0]
    b_ex = b[b > kick_ex]; b_ex = b_ex[b_ex < sept_ex]

    for i in range(len(the_ring)):
        if the_ring[i].angle:
            the_ring[i].hmin = bends_vchamber[0]
            the_ring[i].hmax = bends_vchamber[1]
            the_ring[i].vmin = bends_vchamber[2]
            the_ring[i].vmax = bends_vchamber[3]
        elif the_ring[i].fam_name in ['mB']:
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
