
import math as _math
import pyaccel as _pyaccel
import numpy as _np
import mathphys as _mp
from . import segmented_models as _segmented_models


class LatticeError(Exception):
    pass

energy = 3e9  #[eV]
default_optics_mode = 'M1'

def create_lattice(optics_mode = default_optics_mode):

    strengths, twiss_at_start = get_optics_mode(optics_mode)

    # -- shortcut symbols --
    marker       = _pyaccel.elements.marker
    drift        = _pyaccel.elements.drift
    quadrupole   = _pyaccel.elements.quadrupole
    rbend_sirius = _pyaccel.elements.rbend
    sextupole    = _pyaccel.elements.sextupole
    hcorrector   = _pyaccel.elements.hcorrector
    vcorrector   = _pyaccel.elements.vcorrector

    corr_length = 0.07

    # --- drift spaces ---
    ldif = 0.1442
    l015 = drift('l015', 0.15)
    l020 = drift('l020', 0.20)
    l025 = drift('l025', 0.25)
    l060 = drift('l060', 0.60)
    l080 = drift('l080', 0.80)
    l090 = drift('l090', 0.90)
    l160 = drift('l160', 1.60)
    l280 = drift('l280', 2.80)
    l400 = drift('l400', 4.00)
    la2p = drift('la2p', 0.08323)
    la3p = drift('la3p', 0.232-ldif)
    lb1p = drift('lb1p', 0.220-ldif)
    lb2p = drift('lb2p', 0.83251)
    lb3p = drift('lb3p', 0.30049)
    lb4p = drift('lb4p', 0.19897-ldif)
    lc1p = drift('lc1p', 0.18704-ldif)
    lc2p = drift('lc2p', 0.07304)
    lc3p = drift('lc3p', 0.19934)
    lc4p = drift('lc4p', 0.72666-ldif)
    ld1p = drift('ld1p', 0.25700-ldif)
    ld2p = drift('ld2p', 0.05389)
    ld3p = drift('ld3p', 0.154)
    ld4p = drift('ld4p', 0.192)
    ld5p = drift('ld5p', 0.456)
    ld6p = drift('ld6p', 0.258)
    ld7p = drift('ld7p', 0.175)

    # --- markers ---
    inicio = marker('start')
    fim    = marker('end')

    # --- beam screens ---
    scrn   = marker('Scrn')

    # --- beam current monitors ---
    ict    = marker('ICT')
    fct    = marker('FCT')

    # --- beam position monitors ---
    bpm    = marker('BPM')

    # --- correctors ---
    ch     = hcorrector('CH', 0.0)
    cv     = vcorrector('CV', 0.0)

    # --- quadrupoles ---
    qf1a   = quadrupole('QF1A', 0.14, strengths['qf1a'])
    qf1b   = quadrupole('QF1B', 0.14, strengths['qf1b'])
    qd2    = quadrupole('QD2',  0.14, strengths['qd2'])
    qf2    = quadrupole('QF2',  0.20, strengths['qf2'])
    qf3    = quadrupole('QF3',  0.20, strengths['qf3'])
    qd4a   = quadrupole('QD4A', 0.14, strengths['qd4a'])
    qf4    = quadrupole('QF4',  0.20, strengths['qf4'])
    qd4b   = quadrupole('QD4B', 0.14, strengths['qd4b'])

    # --- bending magnets ---
    d2r = (_math.pi/180)

    # -- b --
    bend = _segmented_models.dipole(sign=+1)

    # -- Thin Septum --
    dip_nam =  'EjeSeptF'
    dip_len =  0.5773
    dip_ang =  -3.6 * d2r
    dip_K   =  0.0
    dip_S   =  0.00
    h1      = rbend_sirius(dip_nam, dip_len/2, dip_ang/2, 1*dip_ang/2, 0*dip_ang,   0,0,0, [0,0,0], [0,dip_K,dip_S])
    h2      = rbend_sirius(dip_nam, dip_len/2, dip_ang/2, 0*dip_ang/2, 1*dip_ang/2, 0,0,0, [0,0,0], [0,dip_K,dip_S])
    bejesf = marker('bEjeSeptF') # marker at the beginning of thin septum
    mejesf = marker('mEjeSeptF') # marker at the center of thin septum
    eejesf = marker('eEjeSeptF') # marker at the end of thin septum
    ejesf = [bejesf, h1, mejesf, h2, eejesf]

    # -- bo thick ejection septum --
    dip_nam  =  'EjeSeptG'
    dip_len  =  0.5773
    dip_ang  =  -3.6 * d2r
    dip_K    =  0.0
    dip_S    =  0.00
    h1       = rbend_sirius(dip_nam, dip_len/2, dip_ang/2, 1*dip_ang/2, 0*dip_ang, 0,0,0, [0,0,0], [0,dip_K,dip_S])
    h2       = rbend_sirius(dip_nam, dip_len/2, dip_ang/2, 0*dip_ang, 1*dip_ang/2, 0,0,0, [0,0,0], [0,dip_K,dip_S])
    bejesg = marker('bEjeSeptG') # marker at the beginning of thick septum
    mejesg = marker('mEjeSeptG') # marker at the center of thick septum
    eejesg = marker('eEjeSeptG') # marker at the end of thick septum
    ejesg = [bejesg, h1, mejesg, h2, eejesg]

    # -- si thick injection septum (2 of these are used) --
    dip_nam  =  'InjSeptG'
    dip_len  =  0.5773
    dip_ang  =  +3.6 * d2r
    dip_K    =  0.0
    dip_S    =  0.00
    h1       = rbend_sirius(dip_nam, dip_len/2, dip_ang/2, 1*dip_ang/2, 0*dip_ang, 0,0,0, [0,0,0], [0,dip_K,dip_S])
    h2       = rbend_sirius(dip_nam, dip_len/2, dip_ang/2, 0*dip_ang, 1*dip_ang/2, 0,0,0, [0,0,0], [0,dip_K,dip_S])
    binjsg = marker('bInjSeptG') # marker at the beginning of thick septum
    minjsg = marker('mInjSeptG') # marker at the center of thick septum
    einjsg = marker('eInjSeptG') # marker at the end of thick septum
    injsg = [binjsg, h1, minjsg, h2, einjsg]

    # -- si thin injection septum --
    dip_nam  =  'InjSeptF'
    dip_len  =  0.5773
    dip_ang  =  +3.118 * d2r
    dip_K    =  0.0
    dip_S    =  0.00
    h1       = rbend_sirius(dip_nam, dip_len/2, dip_ang/2, 1*dip_ang/2, 0*dip_ang, 0,0,0, [0,0,0], [0,dip_K,dip_S])
    h2       = rbend_sirius(dip_nam, dip_len/2, dip_ang/2, 0*dip_ang, 1*dip_ang/2, 0,0,0, [0,0,0], [0,dip_K,dip_S])
    binjsf = marker('bInjSeptF') # marker at the beginning of thin septum
    minjsf = marker('mInjSeptF') # marker at the center of thin septum
    einjsf = marker('eInjSeptF') # marker at the end of thin septum
    injsf = [binjsf, h1, minjsf, h2, einjsf]


    # --- lines ---
    sec01 = [
        ejesf,l025,ejesg,l060,cv,l090,qf1a,la2p,ict,l280,scrn,bpm,
            l020,l020,ch,qf1b,l020,cv,l020,la3p,bend
            ]
    sec02 = [l080,lb1p,qd2,lb2p,scrn,bpm,lb3p,ch,qf2,l020,cv,l025,l015,lb4p,bend]
    sec03 = [lc1p,l400,scrn,bpm,l020,lc2p,ch,qf3,lc3p,cv,lc4p,bend]
    sec04 = [
        ld1p,l060,qd4a,ld2p,l160,bpm,scrn,l020,ld3p,cv,l020,ch,qf4,ld4p,fct,
            ld4p,ict,ld4p,qd4b,ld5p,bpm,scrn,ld6p,cv,ld7p,injsg,l025,injsg,l025,injsf,scrn
            ]

    ts  = [inicio,sec01,sec02,sec03,sec04,fim]

    elist = ts

    the_line = _pyaccel.lattice.build(elist)

    # shifts model to marker 'start'
    idx = _pyaccel.lattice.find_indices(the_line, 'fam_name', 'start')
    the_line = _pyaccel.lattice.shift(the_line, idx[0])

    lengths = _pyaccel.lattice.get_attribute(the_line, 'length')
    for length in lengths:
        if length < 0: raise LatticeError('Model with negative drift!')

    # sets number of integration steps
    set_num_integ_steps(the_line)

    # -- define vacuum chamber for all elements
    set_vacuum_chamber(the_line)

    return the_line, twiss_at_start


def get_optics_mode(optics_mode):
    twiss_at_start = _pyaccel.optics.Twiss.make_new(beta=[9.321, 12.881],
                                                    alpha=[-2.647, 2.000],
                                                    etax=[0.231, 0.069])
    # -- selection of optics mode --
    if optics_mode == 'M1':
        strengths = {
            'qf1a'  :  1.70521151606,
            'qf1b'  :  1.734817173998,
            'qd2'   : -2.8243902951,
            'qf2'   :  2.76086143922,
            'qf3'   :  2.632182549934,
            'qd4a'  : -3.048732667316,
            'qf4'   :  3.613066375692,
            'qd4b'  : -1.46213606815,
        }
    elif optics_mode == 'M2':
        strengths = {
            'qf1a' :  1.670801801437,
            'qf1b' :  2.098494339697,
            'qd2'  : -2.906779151209,
            'qf2'  :  2.807031512313,
            'qf3'  :  2.533815202102,
            'qd4a' : -2.962460334623,
            'qf4'  :  3.537403658428,
            'qd4b' : -1.421177262593,
        }
    else:
        Exception('Invalid TS optics mode: ' + optics_mode)

    return strengths, twiss_at_start


def set_num_integ_steps(the_line):

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


def set_vacuum_chamber(the_line):

    # -- default physical apertures --
    for i in range(len(the_line)):
        the_line[i].hmin = -0.012
        the_line[i].hmax = +0.012
        the_line[i].vmin = -0.012
        the_line[i].vmax = +0.012

    # -- bo ejection septa --
    beg = _pyaccel.lattice.find_indices(the_line, 'fam_name', 'bEjeSeptF')[0]
    end = _pyaccel.lattice.find_indices(the_line, 'fam_name', 'eEjeSeptG')[0]
    for i in range(beg,end+1):
        the_line[i].hmin = -0.0150
        the_line[i].hmax = +0.0150
        the_line[i].vmin = -0.0040
        the_line[i].vmax = +0.0040

    # -- si thick injection septum --
    beg = _pyaccel.lattice.find_indices(the_line, 'fam_name', 'bInjSeptG')[0]
    end = _pyaccel.lattice.find_indices(the_line, 'fam_name', 'eInjSeptG')[0]
    for i in range(beg,end+1):
        the_line[i].hmin = -0.0045
        the_line[i].hmax = +0.0045
        the_line[i].vmin = -0.0035
        the_line[i].vmax = +0.0035

    # -- si thin injection septum --
    beg = _pyaccel.lattice.find_indices(the_line, 'fam_name', 'bInjSeptF')[0]
    end = _pyaccel.lattice.find_indices(the_line, 'fam_name', 'eInjSeptF')[0]
    for i in range(beg,end+1):
        the_line[i].hmin = -0.0150
        the_line[i].hmax = +0.0150
        the_line[i].vmin = -0.0035
        the_line[i].vmax = +0.0035
