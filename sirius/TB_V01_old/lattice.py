
import math as _math
import pyaccel as _pyaccel
import mathphys as _mp
from . import optics_mode_M1 as _optics_mode_M1
from . import optics_mode_M2 as _optics_mode_M2
from . import optics_mode_M3 as _optics_mode_M3
from . import optics_mode_M4 as _optics_mode_M4
from . import optics_mode_M5 as _optics_mode_M5
from . import optics_mode_M6 as _optics_mode_M6

class LatticeError(Exception):
    pass

_energy = 0.15e9 #[eV]
_default_optics_mode = _optics_mode_M1

def create_lattice(optics_mode = _default_optics_mode.label):

    # -- selection of optics mode --
    if optics_mode == 'M1':
        strengths = _optics_mode_M1.strengths
    elif optics_mode == 'M2':
        strengths = _optics_mode_M2.strengths
    elif optics_mode == 'M3':
        strengths = _optics_mode_M3.strengths
    elif optics_mode == 'M4':
        strengths = _optics_mode_M4.strengths
    elif optics_mode == 'M5':
        strengths = _optics_mode_M5.strengths
    elif optics_mode == 'M6':
        strengths = _optics_mode_M6.strengths
    else:
        Exception('Invalid TS optics mode: ' + optics_mode)

    # -- shortcut symbols --
    marker = _pyaccel.elements.marker
    drift  = _pyaccel.elements.drift
    quadrupole   = _pyaccel.elements.quadrupole
    rbend_sirius = _pyaccel.elements.rbend
    sextupole    = _pyaccel.elements.sextupole
    hcorrector   = _pyaccel.elements.hcorrector
    vcorrector   = _pyaccel.elements.vcorrector
    strengths    = _default_optics_mode.strengths

    corr_length = 0.07

    # --- drift spaces ---
    l100   = drift('l100', 0.1000)
    l150   = drift('l150', 0.1500)
    l200   = drift('l200', 0.2000)
    la1    = drift('la1',  0.1150)
    la2p   = drift('la2p', 0.1588)
    lb1p   = drift('lb1p', 0.1250)
    lb2p   = drift('lb2p', 0.2750)
    lb3p   = drift('lb3p', 0.2765)
    lc2    = drift('lc2',  0.2700)
    lc3p   = drift('lc3p', 0.2138)
    lc4    = drift('lc4',  0.2700)
    ld1p   = drift('ld1p', 0.2892)
    ld2    = drift('ld2',  0.2200)
    ld3p   = drift('ld3p', 0.1800)
    le1p   = drift('le1p', 0.1856)
    le2    = drift('le2',  0.2160)

    l100c  = drift('l100c', 0.1000 - corr_length/2)
    l150c  = drift('l150c', 0.1500 - corr_length/2)
    l200c  = drift('l200c', 0.2000 - corr_length/2)
    l100cc = drift('l100c', 0.1000 - corr_length)

    # --- markers ---
    mbspec = marker('mbspec')
    mbn    = marker('mbn')
    mbp    = marker('mbp')
    msep   = marker('msep')
    inicio = marker('start')
    fim    = marker('end')
    fenda  = marker('fenda')

    # --- beam position monitors ---
    bpm = marker('bpm')

    # --- correctors ---
    ch  = sextupole('ch', corr_length, 0.0)
    cv  = sextupole('cv', corr_length, 0.0)

    # --- linac correctors ---
    lch = hcorrector('ch',  0)
    lcv = vcorrector('cv',  0)

    # --- quadrupoles ---
    q1a  = quadrupole('q1a', 0.05, strengths['q1a'])
    q1b  = quadrupole('q1b', 0.10, strengths['q1b'])
    q1c  = quadrupole('q1c', 0.05, strengths['q1c'])
    qd2  = quadrupole('qd2', 0.10, strengths['qd2'])
    qf2  = quadrupole('qf2', 0.10, strengths['qf2'])
    qd3a = quadrupole('qd3a', 0.10, strengths['qd3a'])
    qf3a = quadrupole('qf3a', 0.10, strengths['qf3a'])
    qf3b = quadrupole('qf3b', 0.10, strengths['qf3b'])
    qd3b = quadrupole('qd3b', 0.10, strengths['qd3b'])
    qf4  = quadrupole('qf4', 0.10, strengths['qf4'])
    qd4  = quadrupole('qd4', 0.10, strengths['qd4'])
    qf5  = quadrupole('qf5', 0.10, strengths['qf5'])
    qd5  = quadrupole('qd5', 0.10, strengths['qd5'])

    # --- bending magnets ---
    deg_2_rad = (_math.pi/180)

    # -- bspec --
    dip_nam =  'spec'
    dip_len =  0.45003
    dip_ang =  -15 * deg_2_rad
    dip_K   =  0.0
    dip_S   =  0.00
    spech   = rbend_sirius(dip_nam, dip_len/2, dip_ang/2, 0, 0, 0,0,0, [0,0,0], [0,dip_K,dip_S])
    spec    = [spech, spech]

    # -- bn --
    dip_nam =  'bn'
    dip_len =  0.300858
    dip_ang =  -15 * deg_2_rad
    dip_K   =  0.0
    dip_S   =  0.00
    bne     = rbend_sirius(dip_nam, dip_len/2, dip_ang/2, 1*dip_ang/2, 0*dip_ang/2, 0,0,0, [0,0,0], [0,dip_K,dip_S])
    bns     = rbend_sirius(dip_nam, dip_len/2, dip_ang/2, 0*dip_ang/2, 1*dip_ang/2, 0,0,0, [0,0,0], [0,dip_K,dip_S])
    bn      = [bne, bns]

    # -- bp --
    dip_nam =  'bp'
    dip_len =  0.300858
    dip_ang =  15 * deg_2_rad
    dip_K   =  0.0
    dip_S   =  0.00
    bpe     = rbend_sirius(dip_nam, dip_len/2, dip_ang/2, 1*dip_ang/2, 0*dip_ang/2, 0,0,0, [0,0,0], [0,dip_K,dip_S])
    bps     = rbend_sirius(dip_nam, dip_len/2, dip_ang/2, 0*dip_ang/2, 1*dip_ang/2, 0,0,0, [0,0,0], [0,dip_K,dip_S])
    bp      = [bpe, bps]

    # -- sep --
    dip_nam =  'septin'
    dip_len =  0.50
    dip_ang =  21.75 * deg_2_rad
    dip_K   =  0.0
    dip_S   =  0.00
    septine = rbend_sirius(dip_nam, dip_len/2, dip_ang/2, 1*dip_ang/2, 0*dip_ang, 0,0,0, [0,0,0], [0,dip_K,dip_S])
    septins = rbend_sirius(dip_nam, dip_len/2, dip_ang/2, 0*dip_ang, 1*dip_ang/2, 0,0,0, [0,0,0], [0,dip_K,dip_S])
    bseptin = marker('bseptin')
    eseptin = marker('eseptin')
    septin  = [bseptin, septine, septins, eseptin]

    #booster
    l800    = drift('l800', 0.80)
    l600    = drift('l600', 0.60)
    l250    = drift('l250', 0.25)
    qf      = quadrupole('qf', 0.1, 1.8821)
    kick_in = marker('kick_in')

    lbooster = [l800, l250, qf, qf, l600, kick_in]


    ## # --- lines ---

    la2   = [la2p, l200, l200, l200]
    lb1   = [lb1p, l200, l200, bpm, l150c, ch, l100cc, cv, l150c]
    lb2   = [lb2p, l200]
    lb3   = [l200, l200, l200, l200, l200, fenda, l200, bpm, l150c, cv, l100cc, ch, l200c, l200, lb3p]
    lc1   = [l200, l200, l200, l200, l100]
    lc3   = [l200, bpm, l150c, cv, l100cc, ch, l200c, [l200]*25, lc3p]
    lc5   = [l150, l150, l150, bpm, l150c, ch, l100cc, cv, l200c]
    ld1   = [ld1p, [l200]*10]
    ld3   = [ld3p, bpm, l150c, ch, l200c]
    le1   = [l200c, cv, l200c, l200, l200, l200, l200, l200, le1p]
    le3   = [l150, bpm, l150c, cv, l100c]
    line1 = [lch, lcv, la1, q1a, l100, q1b, l100, q1a, l100, q1c, la2]
    arc1  = [lb1, qd2, lb2, qf2, lb3]
    line2 = [lc1, qd3a, lc2, qf3a, lc3, qf3b, lc4, qd3b, lc5]
    arc2  = [ld1, qf4, ld2, qd4, ld3]
    line3 = [le1, qf5, le2, qd5, le3]
    ltlb  = [inicio, line1, spec, arc1, bn, line2, bp, arc2, bp, line3, septin, bpm, fim]
    elist = ltlb

    # finalization
    elist = ltlb

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

    return the_line


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

    ch_indices = _pyaccel.lattice.find_indices(the_line, 'fam_name', 'ch')
    cv_indices = _pyaccel.lattice.find_indices(the_line, 'fam_name', 'cv')
    corr_indices = ch_indices + cv_indices
    for idx in corr_indices:
        the_line[idx].nr_steps = 5
        

def set_vacuum_chamber(the_line):

    # -- default physical apertures --
    for i in range(len(the_line)):
        the_line[i].hmin = -0.018
        the_line[i].hmax = +0.018
        the_line[i].vmin = -0.018
        the_line[i].vmax = +0.018

    # -- bo injection septum --
    beg = _pyaccel.lattice.find_indices(the_line, 'fam_name', 'bseptin')[0]
    end = _pyaccel.lattice.find_indices(the_line, 'fam_name', 'eseptin')[0]
    for i in range(beg,end+1):
        the_line[i].hmin = -0.0110
        the_line[i].hmax = +0.0075
        the_line[i].vmin = -0.0080
        the_line[i].vmax = +0.0080

    # -- dipoles --
    bn = _pyaccel.lattice.find_indices(the_line, 'fam_name', 'bn')
    bp = _pyaccel.lattice.find_indices(the_line, 'fam_name', 'bp')
    for i in bn + bp:
        the_line[i].hmin = -0.0117
        the_line[i].hmax = +0.0117
        the_line[i].vmin = -0.0117
        the_line[i].vmax = +0.0117
