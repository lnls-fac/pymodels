
import math as _math
import pyaccel as _pyaccel
from . import segmented_models as _segmented_models


class LatticeError(Exception):
    pass


energy = 3e9  # [eV]
default_optics_mode = 'M1'


def create_lattice(optics_mode=default_optics_mode):
    strengths, twiss_at_start = get_optics_mode(optics_mode)

    # -- shortcut symbols --
    marker = _pyaccel.elements.marker
    drift = _pyaccel.elements.drift
    rbend_sirius = _pyaccel.elements.rbend
    sextupole = _pyaccel.elements.sextupole

    # --- drift spaces ---
    ldif = 0.1442
    lcv = 0.150
    l015 = drift('l015', 0.15)
    l020 = drift('l020', 0.20)
    l0125 = drift('l0125', 0.20-lcv/2)
    l025 = drift('l025', 0.25)
    l0175 = drift('l0175', 0.25-lcv/2)
    l060 = drift('l060', 0.60)
    l0525 = drift('l0525', 0.60-lcv/2)
    l080 = drift('l080', 0.80)
    l0825 = drift('l0825', 0.90-lcv/2)
    l160 = drift('l160', 1.60)
    l280 = drift('l280', 2.80)
    la2p = drift('la2p', 0.08323)
    la3p = drift('la3p', 0.232-ldif)
    lb1p = drift('lb1p', 0.220-ldif)
    lb2p = drift('lb2p', 0.83251)
    lb3p = drift('lb3p', 0.30049)
    lb4p = drift('lb4p', 0.19897-ldif)
    lc1p = drift('lc1p', 1.314-ldif)
    lc2p = drift('lc2p', 0.07304)
    lc3p = drift('lc3p', 0.19934-lcv/2)
    lc4p = drift('lc4p', 0.72666-ldif-lcv/2)
    ld1p = drift('ld1p', 0.25700 + ldif - ldif)
    # ld1p drift length in the drawing is specified differently
    ld2p = drift('ld2p', 0.05428)
    ld3p = drift('ld3p', 0.35361-lcv/2)
    ld4p = drift('ld4p', 0.192)
    ld5p = drift('ld5p', 0.45593)
    ld6p = drift('ld6p', 0.48307-lcv/2)
    ld7p = drift('ld7p', 0.175-lcv/2)
    # --- markers ---
    inicio = marker('start')
    fim = marker('end')

    # --- beam screens ---
    scrn = marker('Scrn')

    # --- beam current monitors ---
    ict = marker('ICT')
    fct = marker('FCT')

    # --- beam position monitors ---
    bpm = marker('BPM')

    # --- correctors ---
    # CHs are inside quadrupoles
    cv = sextupole('CV', lcv, 0.0)  # same model as BO correctors

    # --- quadrupoles ---
    qf1a = _segmented_models.quadrupole_q14('QF1A', strengths['qf1a'])
    qf1b = _segmented_models.quadrupole_q14('QF1B', strengths['qf1b'])
    qd2 = _segmented_models.quadrupole_q14('QD2', strengths['qd2'])
    qf2 = _segmented_models.quadrupole_q20('QF2', strengths['qf2'])
    qf3 = _segmented_models.quadrupole_q20('QF3', strengths['qf3'])
    qd4a = _segmented_models.quadrupole_q14('QD4A', strengths['qd4a'])
    qf4 = _segmented_models.quadrupole_q20('QF4', strengths['qf4'])
    qd4b = _segmented_models.quadrupole_q14('QD4B', strengths['qd4b'])

    # --- bending magnets ---
    d2r = (_math.pi/180)

    # -- b --
    bend = _segmented_models.dipole(sign=+1)

    # -- Thin Septum --
    dip_nam = 'EjeSeptF'
    dip_len = 0.5773
    dip_ang = -3.6 * d2r
    dip_K = 0.0
    dip_S = 0.0
    h1 = rbend_sirius(
        dip_nam, dip_len/2, dip_ang/2, 1*dip_ang/2, 0*dip_ang/2, 0, 0, 0,
        [0, 0, 0], [0, dip_K, dip_S])
    h2 = rbend_sirius(
        dip_nam, dip_len/2, dip_ang/2, 0*dip_ang/2, 1*dip_ang/2, 0, 0, 0,
        [0, 0, 0], [0, dip_K, dip_S])
    bejesf = marker('bEjeSeptF')  # marker at the beginning of thin septum
    mejesf = marker('mEjeSeptF')  # marker at the center of thin septum
    eejesf = marker('eEjeSeptF')  # marker at the end of thin septum
    ejesf = [bejesf, h1, mejesf, h2, eejesf]

    # -- bo thick ejection septum --
    dip_nam = 'EjeSeptG'
    dip_len = 0.5773
    dip_ang = -3.6 * d2r
    dip_K = 0.0
    dip_S = 0.0
    h1 = rbend_sirius(
        dip_nam, dip_len/2, dip_ang/2, 1*dip_ang/2, 0*dip_ang/2, 0, 0, 0,
        [0, 0, 0], [0, dip_K, dip_S])
    h2 = rbend_sirius(
        dip_nam, dip_len/2, dip_ang/2, 0*dip_ang/2, 1*dip_ang/2, 0, 0, 0,
        [0, 0, 0], [0, dip_K, dip_S])
    bejesg = marker('bEjeSeptG')  # marker at the beginning of thick septum
    mejesg = marker('mEjeSeptG')  # marker at the center of thick septum
    eejesg = marker('eEjeSeptG')  # marker at the end of thick septum
    ejesg = [bejesg, h1, mejesg, h2, eejesg]

    # -- si thick injection septum (2 of these are used) --
    dip_nam = 'InjSeptG'
    dip_len = 0.5773
    dip_ang = +3.6 * d2r
    dip_K = 0.0
    dip_S = 0.0
    h1 = rbend_sirius(
        dip_nam, dip_len/2, dip_ang/2, 1*dip_ang/2, 0*dip_ang/2, 0, 0, 0,
        [0, 0, 0], [0, dip_K, dip_S])
    h2 = rbend_sirius(
        dip_nam, dip_len/2, dip_ang/2, 0*dip_ang/2, 1*dip_ang/2, 0, 0, 0,
        [0, 0, 0], [0, dip_K, dip_S])
    binjsg = marker('bInjSeptG')  # marker at the beginning of thick septum
    minjsg = marker('mInjSeptG')  # marker at the center of thick septum
    einjsg = marker('eInjSeptG')  # marker at the end of thick septum
    injsg = [binjsg, h1, minjsg, h2, einjsg]

    # -- si thin injection septum --
    dip_nam = 'InjSeptF'
    dip_len = 0.5773
    dip_ang = +3.118 * d2r
    dip_K = 0.0
    dip_S = 0.0
    h1 = rbend_sirius(
        dip_nam, dip_len/2, dip_ang/2, 1*dip_ang/2, 0*dip_ang/2, 0, 0, 0,
        [0, 0, 0], [0, dip_K, dip_S])
    h2 = rbend_sirius(
        dip_nam, dip_len/2, dip_ang/2, 0*dip_ang/2, 1*dip_ang/2, 0, 0, 0,
        [0, 0, 0], [0, dip_K, dip_S])
    binjsf = marker('bInjSeptF')  # marker at the beginning of thin septum
    minjsf = marker('mInjSeptF')  # marker at the center of thin septum
    einjsf = marker('eInjSeptF')  # marker at the end of thin septum
    injsf = [binjsf, h1, minjsf, h2, einjsf]

    # --- lines ---
    sec01 = [
        ejesf, l025, ejesg, l0525, cv, l0825, qf1a, la2p, ict, l280, scrn, bpm,
        l020, l020, qf1b, l0125, cv, l0125, la3p, bend]
    sec02 = [
        l080, lb1p, qd2, lb2p, scrn, bpm, lb3p, qf2, l0125, cv, l0175, l015,
        lb4p, bend]
    sec03 = [lc1p, l280, scrn, bpm, l020, lc2p, qf3, lc3p, cv, lc4p, bend]
    sec04 = [
        ld1p, l060, qd4a, ld2p, l160, bpm, scrn, ld3p, cv, l0125, qf4, ld4p,
        fct, ld4p, ict, ld4p, qd4b, ld5p, bpm, scrn, ld6p, cv, ld7p, injsg,
        l025, injsg, l025, injsf, scrn]

    ts = [inicio, sec01, sec02, sec03, sec04, fim]

    elist = ts

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
    set_vacuum_chamber(the_line)

    return the_line, twiss_at_start


def get_optics_mode(optics_mode):
    twiss_at_start = _pyaccel.optics.Twiss.make_new(
        beta=[9.321, 12.881], alpha=[-2.647, 2.000], etax=[0.231, 0.069])
    # -- selection of optics mode --

    if optics_mode == 'M1':
        # Matched alpha and disp (betax_max = 40m)
        strengths = {
            'qf1a': 1.247810891477,
            'qf1b': 2.269454982012,
            'qd2': -3.095390628668,
            'qf2': 2.478673710387,
            'qf3': 2.48378256297,
            'qd4a': -2.570893964278,
            'qf4': 3.549734282477,
            'qd4b': -2.209083568757,
        }
    elif optics_mode == 'M2':
        # Mismatched optics @ NLK
        strengths = {
            'qf1a': 1.563599428323,
            'qf1b': 2.303150061796,
            'qd2': -2.95822108328,
            'qf2': 2.815338463764,
            'qf3': 2.433331684549,
            'qd4a': -2.295731518617,
            'qf4': 3.413868033048,
            'qd4b': -2.230138095518,
        }
    elif optics_mode == 'M3':
         # Matched optics (betax_max = 100m)
         strengths = {
             'qf1a': 0.801090058058,
             'qf1b': 2.83641570018,
             'qd2': -3.025223032377,
             'qf2': 1.753256050021,
             'qf3': 2.353655122791,
             'qd4a': -2.670345064247,
             'qf4': 3.530990934212,
             'qd4b': -2.073377200462,
         }
    else:
        Exception('Invalid TS optics mode: ' + optics_mode)

    return strengths, twiss_at_start


def set_num_integ_steps(the_line):

    for i in range(len(the_line)):
        if the_line[i].angle:
            length = the_line[i].length
            the_line[i].nr_steps = max(10, int(_math.ceil(length/0.035)))
            print(the_line[i].nr_steps, the_line[i].fam_name)
        elif the_line[i].polynom_b[1]:
            the_line[i].nr_steps = 10
        elif the_line[i].polynom_b[2]:
            the_line[i].nr_steps = 5
        else:
            the_line[i].nr_steps = 1


def set_vacuum_chamber(the_line):

    # -- default physical apertures --
    for ele in the_line:
        ele.hmin = -0.012
        ele.hmax = +0.012
        ele.vmin = -0.012
        ele.vmax = +0.012

    # -- bo ejection septa --
    beg = _pyaccel.lattice.find_indices(the_line, 'fam_name', 'bEjeSeptF')[0]
    end = _pyaccel.lattice.find_indices(the_line, 'fam_name', 'eEjeSeptG')[0]
    for i in range(beg, end+1):
        the_line[i].hmin = -0.0150
        the_line[i].hmax = +0.0150
        the_line[i].vmin = -0.0040
        the_line[i].vmax = +0.0040

    # -- si thick injection septum --
    beg = _pyaccel.lattice.find_indices(the_line, 'fam_name', 'bInjSeptG')[0]
    end = _pyaccel.lattice.find_indices(the_line, 'fam_name', 'eInjSeptG')[0]
    for i in range(beg, end+1):
        the_line[i].hmin = -0.0045
        the_line[i].hmax = +0.0045
        the_line[i].vmin = -0.0035
        the_line[i].vmax = +0.0035

    # -- si thin injection septum --
    beg = _pyaccel.lattice.find_indices(the_line, 'fam_name', 'bInjSeptF')[0]
    end = _pyaccel.lattice.find_indices(the_line, 'fam_name', 'eInjSeptF')[0]
    for i in range(beg, end+1):
        the_line[i].hmin = -0.0150
        the_line[i].hmax = +0.0150
        the_line[i].vmin = -0.0035
        the_line[i].vmax = +0.0035
