#!/usr/bin/env python3

import math as _math
import pyaccel as _pyaccel
import mathphys as _mp
from . import optics_mode_M2 as _optics_mode_M2

_energy = 0.15e9 #[eV]
_default_optics_mode = _optics_mode_M2
_initial_twiss = _pyaccel.optics.Twiss.make_new(spos=0.0,
                                                fixed_point=[0,0,0,0,0,0], # nominal orbit of LI w.r.t. TB coord. sys.
                                                mu=[0.0,0.0],
                                                beta=[7.0,7.0],
                                                alpha=[-1.0,-1.0],
                                                eta=[0,0],
                                                etal=[0,0])
_ejection_fixed_point  = (-0.030,0.0143,0,0,0,0) # nominal orbit of TB w.r.t. BO coord. sys.


def create_lattice():

    # -- selection of optics mode --
    global _default_optics_mode
    _default_optics_mode = _optics_mode_M2

    # -- shortcut symbols --
    marker = _pyaccel.elements.marker
    drift  = _pyaccel.elements.drift
    quadrupole   = _pyaccel.elements.quadrupole
    rbend_sirius = _pyaccel.elements.rbend
    hcorrector   = _pyaccel.elements.hcorrector
    vcorrector   = _pyaccel.elements.vcorrector
    strengths    = _default_optics_mode.strengths

    #correctors length
    c_length = 0.1 #Verificar tamanho real

    # -- drifts --
    l100 = drift('l100', 0.10)
    l150 = drift('l150', 0.15)
    l175 = drift('l175', 0.175)
    l200 = drift('l200', 0.20)
    l250 = drift('l250', 0.25)

    l150c  = drift('l150c',  0.15 - c_length/2.0)
    l250c  = drift('l250c',  0.25 - c_length/2.0)
    l175c  = drift('l175c',  0.175 - c_length/2.0)
    le1pc  = drift('le1pc',  0.261 - c_length/2.0)
    lc2pcc = drift('lc2pcc', 0.281 - c_length)

    la1  = drift('la1', 0.115)
    la2p = drift('la2p', 0.3338)

    lb1p = drift('lb1p', 0.21)
    lb2p = drift('lb2p', 0.184)
    lb3p = drift('lb3p', 0.3575)

    lc1p = drift('lc1p', 0.23)
    lc2p = drift('lc2p', 0.281)
    lc3p = drift('lc3p', 0.2758)
    lc4p = drift('lc4p', 0.342)

    ld1p = drift('ld1p', 0.268)
    ld2p = drift('ld2p', 0.402)
    ld3p = drift('ld3p', 0.2192)

    le1p = drift('le1p', 0.261)
    le2p = drift('le2p', 0.194)
    le3p = drift('le3p', 0.1716)

    # -- lattice markers --
    mbspec = marker('mbspec')
    mbn    = marker('mbn')
    mbp    = marker('mbp')
    msep   = marker('msep')
    esep   = marker('esep')
    start  = marker('start')
    end    = marker('end')
    fenda  = marker('fenda')

    # -- bpms --
    bpm = marker('bpm')

    # -- correctors --
    ch = quadrupole('ch', c_length, 0.0)
    cv = quadrupole('cv', c_length, 0.0)

    # -- quadrupoles --
    qa1 = quadrupole('qa1', 0.05, strengths['qa1'])
    qa2 = quadrupole('qa2', 0.1,  strengths['qa2'])
    qa3 = quadrupole('qa3', 0.05, strengths['qa3'])
    qb1 = quadrupole('qb1', 0.1, strengths['qb1'])
    qb2 = quadrupole('qb2', 0.1, strengths['qb2'])
    qc1 = quadrupole('qc1', 0.1, strengths['qc1'])
    qc2 = quadrupole('qc2', 0.1, strengths['qc2'])
    qc3 = quadrupole('qc3', 0.1, strengths['qc3'])
    qd1 = quadrupole('qd1', 0.1, strengths['qd1'])
    qd2 = quadrupole('qd2', 0.1, strengths['qd2'])
    qe1 = quadrupole('qe1', 0.1, strengths['qe1'])
    qe2 = quadrupole('qe2', 0.1, strengths['qe2'])

    # -- bending magnets --
    deg2rad = _math.pi/180.0

    # -- bspec --
    bspech = rbend_sirius('bspec', 0.45003/2, -15*deg2rad/2, 0, 0, 0, 0, 0, [0, 0, 0], [0, 0, 0])
    bspec  = [bspech, mbspec, bspech]

    # -- bn --
    bne = rbend_sirius('bn', 0.300858/2, -15*deg2rad/2, -15*deg2rad/2, 0, 0, 0, 0, [0, 0, 0], [0, 0, 0])
    bns = rbend_sirius('bn', 0.300858/2, -15*deg2rad/2, 0, -15*deg2rad/2, 0, 0, 0, [0, 0, 0], [0, 0, 0])
    bn  = [bne, mbn, bns]

    # -- bp --
    bpe = rbend_sirius('bp', 0.300858/2, 15*deg2rad/2, 15*deg2rad/2, 0, 0, 0, 0, [0, 0, 0], [0, 0, 0])
    bps = rbend_sirius('bp', 0.300858/2, 15*deg2rad/2, 0, 15*deg2rad/2, 0, 0, 0, [0, 0, 0], [0, 0, 0])
    bp  = [bpe, mbp, bps]

    # -- sep --
    sepe = rbend_sirius('sep', 0.50/2, 21.75*deg2rad/2, 21.75*deg2rad/2, 0, 0, 0, 0, [0, 0, 0], [0, 0, 0])
    seps = rbend_sirius('sep', 0.50/2, 21.75*deg2rad/2, 0, 21.75*deg2rad/2, 0, 0, 0, [0, 0, 0], [0, 0, 0])
    sep  = [sepe, msep, seps, esep]

    #booster
    l800    = drift('l800', 0.80)
    l600    = drift('l600', 0.60)
    qf      = quadrupole('qf', 0.1, 1.8821)
    kick_in = marker('kick_in')
    lbooster = [l800, l250, qf, qf, l600, kick_in]

    # -- lines --
    la2   = [ la2p, l250c, cv, l175c]
    lb1   = [ l200, l200, l200, lb1p]
    lb2   = [ l200, l200, lb2p]
    lb3   = [ l250, l250, l250, l250, fenda, l100, bpm, l175c, cv, l250c, l250, lb3p]
    lc1   = [ l200, l200, l200, lc1p]
    lc2   = [ l150, bpm, l175c, ch, lc2pcc, cv, l150c]
    lc3   = [l250]*13 + [lc3p]
    lc4   = [ lc4p] + [l250]*10 + [bpm, l175c, cv, l175c]
    ld1   = [ l250, l250, l250, l250, ld1p]
    ld2   = [ l250, l250, l250, l250, ld2p]
    ld3   = [ l150, bpm, ld3p]
    le1   = [ l175c, cv, le1pc]
    le2   = [ l200, l200, l200, l200, le2p]
    le3   = [ le3p, l250, bpm, l175c, cv, l175c]
    line1 = [ la1, qa1, l100, qa2, l100, qa1, l100, qa3, la2]
    arc1  = [ bspec, lb1, qb1, lb2, qb2, lb3, bn]
    line2 = [ lc1, qc1, lc2, qc2, lc3, qc3, lc4]
    arc2  = [ bp, ld1, qd1, ld2, qd2, ld3, bp, le1, qe1, le2, qe2, le3, sep]
    ltlb  = [start, line1, arc1, line2, arc2, bpm, end]

    # finalization
    elist = ltlb

    the_line = _pyaccel.lattice.build(elist)

    # shifts model to marker 'start'
    idx = _pyaccel.lattice.find_indices(the_line, 'fam_name', 'start')
    the_line = _pyaccel.lattice.shift(the_line, idx[0])

    # sets number of integration steps
    set_num_integ_steps(the_line)

    # -- define vacuum chamber for all elements
    set_vacuum_chamber(the_line)

    return the_line


def set_num_integ_steps(the_line):

    bends = []
    for i in range(len(the_line)):
        if the_line[i].angle:
            bends.append(i)

    dl = 0.035

    for i in range(len(the_line)):
        if the_line[i].angle:
            bend_nis = int( _math.ceil(the_line[i].length/dl))
            if bend_nis <= 10:
                the_line[i].nr_steps = 10
            else:
                the_line[i].nr_steps = bend_nis
        elif any(the_line[i].polynom_b) and i not in bends:
            the_line[i].nr_steps = 10


def set_vacuum_chamber(the_line):
    #vchamber = [hmin, hmax, vmin, vmax]
    vchamber = [-0.014, 0.014, -0.014, 0.014]

    for i in range(len(the_line)):
        the_line[i].hmin = vchamber[0]
        the_line[i].hmax = vchamber[1]
        the_line[i].vmin = vchamber[2]
        the_line[i].vmax = vchamber[3]

        if the_line[i].fam_name == 'esep': # vacuum chamber at the end of injection septum
            the_line[i].hmax = 0.0075


_the_line = create_lattice()
