"""Lattice module.

In this module the lattice of the corresponding accelerator is defined.
"""

import math as _math
import numpy as _np

from pyaccel import lattice as _pyacc_lat, elements as _pyacc_ele, \
    accelerator as _pyacc_acc, optics as _pyacc_opt
import mathphys as _mp

from . import segmented_models as _seg_models


default_optics_mode = 'M0'
lattice_symmetry = 10
harmonic_number = 828
energy = 0.15e9  # [eV]
_d2r = _math.pi/180.0


def create_lattice(energy=energy, optics_mode=None):
    """Create lattice function."""
    # -- shortcut symbols --
    marker = _pyacc_ele.marker
    drift = _pyacc_ele.drift
    quadrupole = _pyacc_ele.quadrupole
    sextupole = _pyacc_ele.sextupole
    rfcavity = _pyacc_ele.rfcavity

    optics_mode = optics_mode or default_optics_mode

    strengths = get_optics_mode(optics_mode, energy)

    B, _ = _seg_models.dipole(energy)

    dcircum = 496.78745 - 496.80000

    # ----- DRIFTS ----
    L008100p = drift('l008100p', 0.08100 + dcircum/50/2)
    L008800 = drift('l008800', 0.08800)
    L010350p = drift('l010350p', 0.10350 + dcircum/50/2)
    L013350 = drift('l013350', 0.13350)
    L010600p = drift('l010600p', 0.10600 + dcircum/50/2)
    L013600 = drift('l013600', 0.13600)
    L016100 = drift('l016100', 0.16100)
    L016750 = drift('l016750', 0.16750)
    L018860 = drift('l018860', 0.18860)
    L027250 = drift('l027250', 0.27250)
    L035000 = drift('l035000', 0.35000)
    L038600 = drift('l038600', 0.38600)
    L045000 = drift('l045000', 0.45000)
    L053572 = drift('l053572', 0.53572)
    L062000 = drift('l062000', 0.62000)
    L069811p = drift('l069811p', 0.69811 + dcircum/50/2)
    L072500 = drift('l072500', 0.72500)
    L109600 = drift('l109600', 1.09600)
    L115740 = drift('l115740', 1.15740)
    L130389 = drift('l130389', 1.30389)
    L134600 = drift('l134600', 1.34600)
    L137100 = drift('l137100', 1.37100)
    L144600 = drift('l144600', 1.44600)
    L151200 = drift('l151200', 1.51200)
    L159628 = drift('l159628', 1.59628)
    L165200p = drift('l165200p', 1.65200 + dcircum/50/2)
    L168300 = drift('l168300', 1.68300)
    L172600 = drift('l172600', 1.72600)
    L177100 = drift('l177100', 1.77100)
    L179350 = drift('l179350', 1.79350)
    L179600 = drift('l179600', 1.79600)
    L182100 = drift('l182100', 1.82100)
    L189350 = drift('l189350', 1.89350)
    L200200p = drift('l200200p', 2.00200 + dcircum/50/2)
    L213200 = drift('l213200', 2.13200)

    STR  = marker('start')     # start of the model
    FIM  = marker('end'  )     # end of the model
    GIR  = marker('girder')

    SIN  = marker('InjSept')
    SEX  = marker('EjeSeptF')

    DCCT = marker('DCCT')
    BPM  = marker('BPM')
    Scrn = marker('Scrn')
    GSL  = marker('GSL')
    TunePkup= marker('TunePkup')
    TuneShkr= marker('TuneShkr')

    KIN  = quadrupole('InjKckr', 0.40000, 0.0)
    KEX  = quadrupole('EjeKckr', 0.40000, 0.0)
    CH   = sextupole('CH',   0.150, 0.0)
    CV   = sextupole('CV',   0.150, 0.0)

    SF,_  = _seg_models.sx_sextupole(energy, 'SF', strengths['sf'] * 0.105)
    SD,_  = _seg_models.sx_sextupole(energy, 'SD', strengths['sd'] * 0.105)

    QD,_  = _seg_models.qd_quadrupole(energy, 'QD', strengths['qd'] * 0.100)
    QF,_  = _seg_models.qf_quadrupole(energy, 'QF', strengths['qf'] * 0.228)
    QS    = quadrupole('QS', 0.100, strengths['qs'])
    QF0   = [QF[0], FIM, STR, QF[1:]]

    RFC = rfcavity('P5Cav', 0, 0, 0) # RF frequency will be set later.

    # --- lines ---

    US_SF = [GIR, L200200p, BPM, L189350, GIR, SF, L013350]
    US_CS = [
        L010350p, SD, L027250, CV, GIR, L137100, BPM, L182100, GIR, CH, L016100]
    US_CC = [L008100p, CV, GIR, L177100, BPM, L182100, GIR, CH, L016100]
    US_SS = [L010350p, SD, GIR, L179350, BPM, L189350, GIR, SF, L013350]
    US_SF_Scrn = [GIR, L200200p, BPM, L172600, GIR, Scrn, L016750, SF, L013350]
    US_SE = [L008100p, CV, GIR, L168300, SEX, L008800, L159628, BPM, L053572, GIR]
    US_SI = [L008100p, CV, GIR, L177100, BPM, L109600, SIN, L072500, GIR, CH, L016100]
    US_SF_GSL = [GIR, L165200p, GSL, L035000, BPM, L189350, GIR, SF, L013350]

    DS = [GIR, L213200, L200200p, GIR]
    DS_QD = [GIR, L213200, L179600, GIR, QD, L010600p]
    DS_RF = [GIR, L213200, RFC, L200200p, GIR]
    DS_KE = [GIR, L038600, KEX, L134600, L179600, GIR, QD, L010600p]
    DS_CH = [L016100, CH, GIR, L182100, L200200p, GIR]
    DS_KI = [GIR, L038600, KIN, L018860, Scrn, L115740, L130389, Scrn, L069811p, GIR]
    DS_QS_TuS = [L013600, QS, GIR, L144600, TuneShkr, L045000, L179600, GIR, QD, L010600p]
    DS_DCCT = [GIR, L213200, DCCT, L200200p, GIR]
    DS_QD_TuP = [GIR, L151200, TunePkup, L062000, L179600, GIR, QD, L010600p]

    # -- upstream and downstream subsectors

    US_01 = US_SI
    DS_01 = DS_KI
    US_02 = US_SF_Scrn
    DS_02 = DS_QS_TuS
    US_03 = US_CS
    DS_03 = DS
    US_04 = US_SF_GSL
    DS_04 = DS_QD_TuP
    US_05 = US_CC
    DS_05 = DS_RF
    US_06 = US_SF
    DS_06 = DS_QD
    US_07 = US_CC
    DS_07 = DS
    US_08 = US_SS
    DS_08 = DS_QD
    US_09 = US_CC
    DS_09 = DS
    US_10 = US_SF
    DS_10 = DS_QD
    US_11 = US_CC
    DS_11 = DS
    US_12 = US_SF
    DS_12 = DS_QD
    US_13 = US_CS
    DS_13 = DS
    US_14 = US_SF
    DS_14 = DS_QD
    US_15 = US_CC
    DS_15 = DS
    US_16 = US_SF
    DS_16 = DS_QD
    US_17 = US_CC
    DS_17 = DS
    US_18 = US_SS
    DS_18 = DS_QD
    US_19 = US_CC
    DS_19 = DS
    US_20 = US_SF
    DS_20 = DS_QD
    US_21 = US_CC
    DS_21 = DS
    US_22 = US_SF
    DS_22 = DS_QD
    US_23 = US_CS
    DS_23 = DS
    US_24 = US_SF
    DS_24 = DS_QD
    US_25 = US_CC
    DS_25 = DS
    US_26 = US_SF
    DS_26 = DS_QD
    US_27 = US_CC
    DS_27 = DS
    US_28 = US_SS
    DS_28 = DS_QD
    US_29 = US_CC
    DS_29 = DS
    US_30 = US_SF
    DS_30 = DS_QD
    US_31 = US_CC
    DS_31 = DS
    US_32 = US_SF
    DS_32 = DS_QD
    US_33 = US_CS
    DS_33 = DS
    US_34 = US_SF
    DS_34 = DS_QD
    US_35 = US_CC
    DS_35 = DS_DCCT
    US_36 = US_SF
    DS_36 = DS_QD
    US_37 = US_CC
    DS_37 = DS
    US_38 = US_SS
    DS_38 = DS_QD
    US_39 = US_CC
    DS_39 = DS
    US_40 = US_SF
    DS_40 = DS_QD
    US_41 = US_CC
    DS_41 = DS
    US_42 = US_SF
    DS_42 = DS_QD
    US_43 = US_CS
    DS_43 = DS
    US_44 = US_SF
    DS_44 = DS_QD
    US_45 = US_CC
    DS_45 = DS
    US_46 = US_SF
    DS_46 = DS_QD
    US_47 = US_CC
    DS_47 = DS
    US_48 = US_SS
    DS_48 = DS_KE
    US_49 = US_SE
    DS_49 = DS_CH
    US_50 = US_SF
    DS_50 = DS_QD

    S01 = [US_01, QF0, DS_01, B]
    S02 = [US_02, QF, DS_02, B]
    S03 = [US_03, QF, DS_03, B]
    S04 = [US_04, QF, DS_04, B]
    S05 = [US_05, QF, DS_05, B]
    S06 = [US_06, QF, DS_06, B]
    S07 = [US_07, QF, DS_07, B]
    S08 = [US_08, QF, DS_08, B]
    S09 = [US_09, QF, DS_09, B]
    S10 = [US_10, QF, DS_10, B]
    S11 = [US_11, QF, DS_11, B]
    S12 = [US_12, QF, DS_12, B]
    S13 = [US_13, QF, DS_13, B]
    S14 = [US_14, QF, DS_14, B]
    S15 = [US_15, QF, DS_15, B]
    S16 = [US_16, QF, DS_16, B]
    S17 = [US_17, QF, DS_17, B]
    S18 = [US_18, QF, DS_18, B]
    S19 = [US_19, QF, DS_19, B]
    S20 = [US_20, QF, DS_20, B]
    S21 = [US_21, QF, DS_21, B]
    S22 = [US_22, QF, DS_22, B]
    S23 = [US_23, QF, DS_23, B]
    S24 = [US_24, QF, DS_24, B]
    S25 = [US_25, QF, DS_25, B]
    S26 = [US_26, QF, DS_26, B]
    S27 = [US_27, QF, DS_27, B]
    S28 = [US_28, QF, DS_28, B]
    S29 = [US_29, QF, DS_29, B]
    S30 = [US_30, QF, DS_30, B]
    S31 = [US_31, QF, DS_31, B]
    S32 = [US_32, QF, DS_32, B]
    S33 = [US_33, QF, DS_33, B]
    S34 = [US_34, QF, DS_34, B]
    S35 = [US_35, QF, DS_35, B]
    S36 = [US_36, QF, DS_36, B]
    S37 = [US_37, QF, DS_37, B]
    S38 = [US_38, QF, DS_38, B]
    S39 = [US_39, QF, DS_39, B]
    S40 = [US_40, QF, DS_40, B]
    S41 = [US_41, QF, DS_41, B]
    S42 = [US_42, QF, DS_42, B]
    S43 = [US_43, QF, DS_43, B]
    S44 = [US_44, QF, DS_44, B]
    S45 = [US_45, QF, DS_45, B]
    S46 = [US_46, QF, DS_46, B]
    S47 = [US_47, QF, DS_47, B]
    S48 = [US_48, QF, DS_48, B]
    S49 = [US_49, QF, DS_49, B]
    S50 = [US_50, QF, DS_50, B]

    elist = [
        S01, S02, S03, S04, S05, S06, S07, S08, S09, S10,
        S11, S12, S13, S14, S15, S16, S17, S18, S19, S20,
        S21, S22, S23, S24, S25, S26, S27, S28, S29, S30,
        S31, S32, S33, S34, S35, S36, S37, S38, S39, S40,
        S41, S42, S43, S44, S45, S46, S47, S48, S49, S50]

    the_ring = _pyacc_lat.build(elist)

    # -- shifts model to marker 'start'
    idx = _pyacc_lat.find_indices(the_ring, 'fam_name', 'start')
    the_ring = _pyacc_lat.shift(the_ring, idx[0])

    # -- sets rf frequency
    set_rf_frequency(the_ring)

    # -- sets rf voltage
    set_rf_voltage(the_ring, energy)

    # -- sets number of integration steps
    set_num_integ_steps(the_ring)

    # -- define vacuum chamber for all elements
    the_ring = set_vacuum_chamber(the_ring)

    return the_ring


def get_optics_mode(optics_mode, energy=energy):
    """Return magnet strengths of a given opics mode."""
    if optics_mode == 'M0':
        # 2019-08-01 Murilo
        # tunes fitted to [19.20433 7.31417] for new dipoles segmented model
        #
        # 2020-11-30 Ximenes
        # New circumference

        # NOTE: To be updated with strengths of resimmetrized optics (MAD)

        qf_high_en = 1.6546257316588266
        qd_high_en = -0.11289748549970072
        qs_high_en = 0.0
        sf_high_en = 11.308079742311124
        sd_high_en = 10.519518298912761

        qf_low_en = 1.6538462056686665
        qd_low_en = -0.0011251597339454525
        qs_low_en = 0.0
        sf_low_en = 11.320709999244496
        sd_low_en = 10.374355202009147

    else:
        raise _pyacc_acc.AcceleratorException('Optics mode not recognized.')

    coeff = (energy-0.15e9)/(3e9-0.15e9)
    strengths = {
        'qf' : qf_low_en + coeff*(qf_high_en - qf_low_en),
        'qd' : qd_low_en + coeff*(qd_high_en - qd_low_en),
        'qs' : qs_low_en + coeff*(qs_high_en - qs_low_en),
        'sf' : sf_low_en + coeff*(sf_high_en - sf_low_en),
        'sd' : sd_low_en + coeff*(sd_high_en - sd_low_en),
    }
    return strengths


def set_rf_frequency(the_ring):
    """Set RF frequency of the lattice."""
    circumference = _pyacc_lat.length(the_ring)
    velocity = _mp.constants.light_speed
    rev_frequency = velocity / circumference
    rf_frequency  = harmonic_number * rev_frequency
    idx = _pyacc_lat.find_indices(the_ring, 'fam_name', 'P5Cav')
    for i in idx:
        the_ring[i].frequency = rf_frequency


def set_rf_voltage(the_ring, energy):
    """Set RF voltage of the lattice."""
    overvoltage = 1.525
    energy0 = 0.15e9
    rho0 = 1.152*50/(2*_math.pi)
    U0 = (_mp.constants.rad_cgamma*((energy*1e-9)**4)/rho0)*1e9

    voltage_inj = 150e3 - overvoltage*((_mp.constants.rad_cgamma*((energy0*1e-9)**4)/rho0)*1e9)
    voltage_eje = 950e3
    voltage = min([(overvoltage*U0 + voltage_inj), voltage_eje])

    idx = _pyacc_lat.find_indices(the_ring, 'fam_name', 'P5Cav')
    for i in idx:
        the_ring[i].voltage = voltage


def set_num_integ_steps(the_ring):
    """Set number of integration steps in each lattice element."""
    bends = []
    for i, _ in enumerate(the_ring):
        if the_ring[i].angle:
            bends.append(i)

    len_b = 3e-2
    len_qs = 1.5e-2

    zero_polyB = ('InjSept', 'InjKckr', 'EjeSeptF', 'EjeKckr', 'QS')

    for i, _ in enumerate(the_ring):
        if i in bends:
            nr_steps = int(_math.ceil(the_ring[i].length/len_b))
            the_ring[i].nr_steps = nr_steps
        elif any(the_ring[i].polynom_b) or the_ring[i].fam_name in zero_polyB:
            nr_steps = int(_math.ceil(the_ring[i].length/len_qs))
            the_ring[i].nr_steps = nr_steps


def set_vacuum_chamber(the_ring):
    """Set vacuum chamber for all elements."""
    # vchamber = [hmin, hmax, vmin, vmax]
    bends_vchamber = [-0.0117, 0.0117, -0.0117, 0.0117]
    other_vchamber = [-0.018, 0.018, -0.018, 0.018]
    extraction_vchamber = [-0.018, 0.026, -0.018, 0.018]

    sept_in = _pyacc_lat.find_indices(the_ring, 'fam_name', 'InjSept')[0]
    kick_in = _pyacc_lat.find_indices(the_ring, 'fam_name', 'InjKckr')[0]

    b = _np.array(_pyacc_lat.find_indices(the_ring, 'fam_name', 'B'))
    sept_ex = _pyacc_lat.find_indices(the_ring, 'fam_name', 'EjeSeptF')[0]
    kick_ex = _pyacc_lat.find_indices(the_ring, 'fam_name', 'EjeKckr')[0]
    b_ex = b[b > kick_ex]; b_ex = b_ex[b_ex < sept_ex]

    for i, _ in enumerate(the_ring):
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

    return the_ring
