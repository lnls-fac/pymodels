"""Lattice module.

In this module the lattice of the corresponding accelerator is defined.
"""

import math as _math
import pyaccel as _pyaccel
from . import segmented_models as _segmented_models

energy = 0.150e9  # [eV]
default_optics_mode = 'M1'


class LatticeError(Exception):
    """LatticeError class."""

    pass


def create_lattice(optics_mode=default_optics_mode):
    """Create lattice function."""
    strengths, twiss_at_start = get_optics_mode(optics_mode)

    # -- shortcut symbols --
    marker = _pyaccel.elements.marker
    drift = _pyaccel.elements.drift
    quadrupole = _pyaccel.elements.quadrupole
    rbend_sirius = _pyaccel.elements.rbend
    sextupole = _pyaccel.elements.sextupole

    deg_2_rad = _math.pi / 180.0

    corr_length = 0.07

    # --- drift spaces ---
    l100 = drift('l100', 0.100)
    l150 = drift('l150', 0.150)
    l200 = drift('l200', 0.200)
    l165 = drift('l165', 0.165000)
    l075 = drift('l075', 0.075429)
    l110 = drift('l110', 0.110429)
    l199 = drift('l199', 0.199629)
    l187 = drift('l187', 0.186929)

    lb1p = drift('lb1p', 0.125)
    lb2p = drift('lb2p', 0.275)
    lc2 = drift('lc2',  0.270)
    lc3p = drift('lc3p', 0.2138)
    lc4 = drift('lc4',  0.270)
    ld2 = drift('ld2',  0.220)
    ld3p = drift('ld3p', 0.180)
    le1p = drift('le1p', 0.1856)
    le2 = drift('le2',  0.216)

    l100c = drift('l100c', 0.1000 - corr_length/2)
    l150c = drift('l150c', 0.1500 - corr_length/2)
    l100cc = drift('l100c', 0.1000 - corr_length)

    # --- markers ---
    inicio = marker('start')
    fim = marker('end')

    # --- slits ---
    hslit = marker('SlitH')
    vslit = marker('SlitV')

    # --- beam screens ---
    scrn = marker('Scrn')

    # --- beam current monitors ---
    ict = marker('ICT')

    # --- beam position monitors ---
    bpm = marker('BPM')

    # --- correctors ---
    ch = sextupole('CH', corr_length, 0.0)
    cv = sextupole('CV', corr_length, 0.0)

    # --- quadrupoles ---
    qd1 = quadrupole('QD1', 0.10, strengths['qd1'])
    qf1 = quadrupole('QF1', 0.10, strengths['qf1'])
    qd2a = quadrupole('QD2A', 0.10, strengths['qd2a'])
    qf2a = quadrupole('QF2A', 0.10, strengths['qf2a'])
    qf2b = quadrupole('QF2B', 0.10, strengths['qf2b'])
    qd2b = quadrupole('QD2B', 0.10, strengths['qd2b'])
    qf3 = quadrupole('QF3', 0.10, strengths['qf3'])
    qd3 = quadrupole('QD3', 0.10, strengths['qd3'])
    qf4 = quadrupole('QF4', 0.10, strengths['qf4'])
    qd4 = quadrupole('QD4', 0.10, strengths['qd4'])

    # --- bending magnets ---
    bp = _segmented_models.dipole(sign=+1)
    bn = _segmented_models.dipole(sign=-1)

    # -- sep --
    dip_nam = 'InjSept'
    dip_len = 0.50
    dip_ang = 21.75 * deg_2_rad
    dip_K = 0.0
    dip_S = 0.00
    septine = rbend_sirius(dip_nam, dip_len/2, dip_ang/2,
                           1*dip_ang/2, 0*dip_ang,
                           0, 0, 0, [0, 0, 0], [0, dip_K, dip_S])
    septins = rbend_sirius(dip_nam, dip_len/2, dip_ang/2,
                           0*dip_ang, 1*dip_ang/2,
                           0, 0, 0, [0, 0, 0], [0, dip_K, dip_S])
    bseptin = marker('bInjSept')
    eseptin = marker('eInjSept')
    septin = [bseptin, septine, septins, eseptin]

    # --- lines ---
    ld1 = [l199] + 10 * [l200]
    s01_1 = [lb1p, l200, l200, scrn, bpm, l150c, ch, l100cc, cv, l150c]
    s01_2 = [lb2p, l200]
    s01_3 = [l200, l200, l200, l200, l200, l200, hslit, scrn, bpm, l150c, cv,
             l100cc, ch, l165, vslit, l200, l187]
    s02_1 = [l110, l200, ict, l200, l200, l100]
    s02_2 = [l200, scrn, bpm, l150c, ch, l100cc, cv, l165] + 25*[l200] + [lc3p]
    s02_3 = [l150, l150, l150, scrn, bpm, l150c, ch, l100cc, cv, l075]
    s03_1 = [ld3p, scrn, bpm, l150c, ch, l075]
    s04_1 = [l075, cv, l165, l200, l200, l200, l200, l200, ict, le1p]
    s04_2 = [l150, scrn, bpm, l150c, cv, l100c]

    sector01 = [s01_1, qd1, s01_2, qf1, s01_3, bn]
    sector02 = [s02_1, qd2a, lc2, qf2a, s02_2, qf2b, lc4, qd2b, s02_3, bp]
    sector03 = [ld1, qf3, ld2, qd3, s03_1, bp]
    sector04 = [s04_1, qf4, le2, qd4, scrn, cv, s04_2, septin]

    # --- TB beamline beginning with end of linac ---
    ltlb = [inicio, sector01, sector02, sector03, sector04, fim]

    elist = ltlb

    the_line = _pyaccel.lattice.build(elist)

    # --- shifts model to marker 'start' ---
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
    """Return magnet strengths of a given opics mode."""
    # -- selection of optics mode --
    if optics_mode == 'M1':
        twiss_at_start = \
            _pyaccel.optics.Twiss.make_new(beta=[3.1667, 13.3117],
                                           alpha=[1.5073, -2.9245],
                                           etax=[-0.0586, -0.2588])
        strengths = {
            'qd1': -8.420879613851,
            'qf1': 13.146671512202,
            'qd2a': -5.003211465479,
            'qf2a':  6.783244529016,
            'qf2b':  2.895212566505,
            'qd2b': -2.984706731539,
            'qf3':  7.963034094957,
            'qd3': -2.013774809345,
            'qf4': 11.529185003262,
            'qd4': -7.084093211983,
        }
    elif optics_mode == 'M2':
        twiss_at_start = \
            _pyaccel.optics.Twiss.make_new(beta=[3.6036, 16.6264],
                                           alpha=[1.5671, -1.3144],
                                           etax=[-0.0586, -0.2588])
        strengths = {
            'qd1': -8.420884154134,
            'qf1': 13.146672851601,
            'qd2a': -5.786996070251,
            'qf2a': 7.48800218842,
            'qf2b': 3.444273863854,
            'qd2b': -4.370692899919,
            'qf3': 9.275556378041,
            'qd3': -3.831727343173,
            'qf4': 11.774551301802,
            'qd4': -7.239923812237,
        }
    elif optics_mode == 'M3':
        twiss_at_start = \
            _pyaccel.optics.Twiss.make_new(beta=[3.2556, 19.6968],
                                           alpha=[1.0134, -3.6354],
                                           etax=[-0.0586, -0.2588])
        strengths = {
            'qd1': -8.4202421458,
            'qf1': 13.146512110234,
            'qd2a': -4.742318522445,
            'qf2a': 6.865529327161,
            'qf2b': 3.644627263975,
            'qd2b': -3.640344975066,
            'qf3': 6.882094963212,
            'qd3': -0.650373210524,
            'qf4': 11.456881278596,
            'qd4': -7.183997114808,
        }
    elif optics_mode == 'M4':
        twiss_at_start = \
            _pyaccel.optics.Twiss.make_new(beta=[3.2421,  3.8668],
                                           alpha=[1.7275,  0.2114],
                                           etax=[-0.0586, -0.2588])
        strengths = {
            'qd1': -8.420952075727,
            'qf1': 13.146690356394,
            'qd2a': -6.698085523725,
            'qf2a': 7.789621927907,
            'qf2b': 2.77064582429,
            'qd2b': -3.328855564917,
            'qf3': 8.734105391772,
            'qd3': -3.014211757657,
            'qf4': 11.424069037719,
            'qd4': -6.740424372291,
        }
    elif optics_mode == 'M5':
        twiss_at_start = \
            _pyaccel.optics.Twiss.make_new(beta=[0.4918, 21.7039],
                                           alpha=[0.6437, -3.4604],
                                           etax=[-0.0586, -0.2588])
        strengths = {
            'qd1': -8.420850561756,
            'qf1': 13.146666514846,
            'qd2a': -5.621149037043,
            'qf2a': 8.967988594169,
            'qf2b': 2.958960220371,
            'qd2b': -3.210342770435,
            'qf3': 8.311858252882,
            'qd3': -2.442934101437,
            'qf4': 11.391698651189,
            'qd4': -6.772341213215,
        }
    elif optics_mode == 'M6':
        twiss_at_start = \
            _pyaccel.optics.Twiss.make_new(beta=[2.9771, 11.0431],
                                           alpha=[1.0378, -0.8005],
                                           etax=[-0.0586, -0.2588])
        strengths = {
            'qd1': -8.420886991042,
            'qf1': 13.146673683891,
            'qd2a': -5.452694879372,
            'qf2a': 7.345924165318,
            'qf2b': 3.605078182875,
            'qd2b': -4.255957305622,
            'qf3': 8.858246721391,
            'qd3': -3.243238337219,
            'qf4': 11.728866700839,
            'qd4': -7.246970930681,
        }
    else:
        Exception('Invalid TS optics mode: ' + optics_mode)

    return strengths, twiss_at_start


def set_num_integ_steps(the_line):
    """Set number of integration steps in each lattice element."""
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
    """Set vacuum chamber for all elements."""
    # -- default physical apertures --
    for i in range(len(the_line)):
        the_line[i].hmin = -0.018
        the_line[i].hmax = +0.018
        the_line[i].vmin = -0.018
        the_line[i].vmax = +0.018

    # -- bo injection septum --
    beg = _pyaccel.lattice.find_indices(the_line, 'fam_name', 'bInjSept')[0]
    end = _pyaccel.lattice.find_indices(the_line, 'fam_name', 'eInjSept')[0]
    for i in range(beg, end+1):
        the_line[i].hmin = -0.0110
        the_line[i].hmax = +0.0075
        the_line[i].vmin = -0.0080
        the_line[i].vmax = +0.0080

    # -- dipoles --
    bnd = _pyaccel.lattice.find_indices(the_line, 'fam_name', 'B')
    for i in bnd:
        the_line[i].hmin = -0.0117
        the_line[i].hmax = +0.0117
        the_line[i].vmin = -0.0117
        the_line[i].vmax = +0.0117
