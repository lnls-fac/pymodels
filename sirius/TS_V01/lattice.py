
import math as _math
import pyaccel as _pyaccel
import mathphys as _mp
from . import optics_mode_M1 as _optics_mode_M1
from . import optics_mode_M2 as _optics_mode_M2

_default_optics_mode = _optics_mode_M1
_energy = 3e9 #[eV]

def create_lattice(optics_mode = _default_optics_mode.label):

    # -- selection of optics mode --
    if optics_mode == 'M1':
        strengths = _optics_mode_M1.strengths
    elif optics_mode == 'M2':
        strengths = _optics_mode_M2.strengths
    else:
        Exception('Invalid TS optics mode: ' + optics_mode)

    # -- shortcut symbols --
    marker = _pyaccel.elements.marker
    drift  = _pyaccel.elements.drift
    quadrupole   = _pyaccel.elements.quadrupole
    rbend_sirius = _pyaccel.elements.rbend
    hcorrector   = _pyaccel.elements.hcorrector
    vcorrector   = _pyaccel.elements.vcorrector
    strengths    = _default_optics_mode.strengths

    # --- drift spaces ---
    l15      = drift('l15', 0.15)
    l16      = drift('l16', 0.16)
    l17      = drift('l17', 0.18)
    l18      = drift('l18', 0.18)
    l20      = drift('l20', 0.20)
    l22      = drift('l22', 0.22)
    l24      = drift('l24', 0.24)
    l25      = drift('l25', 0.25)
    la2p     = drift('la2p', 0.13777)
    lb3p     = drift('lb3p', 0.24883)
    lc1p     = drift('lc1p', 0.23400)
    lc2p     = drift('lc1p', 0.21215)
    ld2p     = drift('ld2p', 0.13933)

    # --- markers ---

    mbend    = marker('mbend')
    start    = marker('start')
    fim      = marker('end')

    # --- quadrupoles ---

    qf1a    = quadrupole('qf1a', 0.14, strengths['qf1a']) # qf
    qf1b    = quadrupole('qf1b', 0.14, strengths['qf1b']) # qf
    qd2     = quadrupole('qd2',  0.14, strengths['qd2'])  # qd
    qf2     = quadrupole('qf2',  0.20, strengths['qf2'])  # qf
    qf3     = quadrupole('qf3',  0.20, strengths['qf3'])  # qf
    qd4a    = quadrupole('qd4a', 0.14, strengths['qd4a']) # qd
    qf4     = quadrupole('qf4',  0.20, strengths['qf4'])  # qf
    qd4b    = quadrupole('qd4b', 0.14, strengths['qd4b']) # qd

    # --- beam position monitors ---
    bpm    = marker('bpm')

    # --- correctors ---
    ch     = hcorrector('hcm',  0)
    cv     = vcorrector('vcm',  0)

    # --- bending magnets ---

    deg_2_rad = (_math.pi/180)

    # -- bend --
    dip_nam =  'bend'
    dip_len =  1.151658
    dip_ang =  5.333333 * deg_2_rad
    dip_K   =  -0.1526
    dip_S   =  0.00
    h1      = rbend_sirius(dip_nam, dip_len/2, dip_ang/2, 1*dip_ang/2, 0*dip_ang/2, 0,0,0, [0,0,0], [0,dip_K,dip_S])
    h2      = rbend_sirius(dip_nam, dip_len/2, dip_ang/2, 0*dip_ang/2, 1*dip_ang/2, 0,0,0, [0,0,0], [0,dip_K,dip_S])
    bend    = [h1, mbend, h2]


    # -- bo extraction septum --
    dip_nam =  'septex'
    dip_len =  0.85
    dip_ang =  -3.6 * deg_2_rad
    dip_K   =  0.0
    dip_S   =  0.00
    h1      = rbend_sirius(dip_nam, dip_len/2, dip_ang/2, 1*dip_ang/2, 0*dip_ang, 0,0,0, [0,0,0], [0,dip_K,dip_S])
    h2      = rbend_sirius(dip_nam, dip_len/2, dip_ang/2, 0*dip_ang/2, 1*dip_ang/2, 0,0,0, [0,0,0], [0,dip_K,dip_S])
    bseptex = marker('bseptex') # marker at the beginning of extraction septum
    mseptex = marker('mseptex') # marker at the center of extraction septum
    eseptex = marker('eseptex') # marker at the end of extraction septum
    septum  = [h1, mseptex, h2]
    septex  = [bseptex, septum, l20, ch, septum, eseptex]

    # -- thick si injection septum --
    dip_nam  =  'septing'
    dip_len  =  1.10
    dip_ang  =  6.2 * deg_2_rad
    dip_K    =  0.0
    dip_S    =  0.00
    h1       = rbend_sirius(dip_nam, dip_len/2, dip_ang/2, 1*dip_ang/2, 0*dip_ang, 0,0,0, [0,0,0], [0,dip_K,dip_S])
    h2       = rbend_sirius(dip_nam, dip_len/2, dip_ang/2, 0*dip_ang, 1*dip_ang/2, 0,0,0, [0,0,0], [0,dip_K,dip_S])
    bsepting = marker('bsepting') # marker at the center of thick septum
    msepting = marker('msepting') # marker at the center of thick septum
    esepting = marker('esepting') # marker at the center of thick septum
    septgr   = [bsepting, h1, msepting, h2, esepting]

    # -- thin si injection septum --
    dip_nam  =  'septinf'
    dip_len  =  0.925
    dip_ang  =  3.13 * deg_2_rad
    dip_K    =  0.00
    dip_S    =  0.00
    h1       = rbend_sirius(dip_nam, dip_len/2, dip_ang/2, 1*dip_ang/2, 0*dip_ang, 0,0,0, [0,0,0], [0,dip_K,dip_S])
    h2       = rbend_sirius(dip_nam, dip_len/2, dip_ang/2, 0*dip_ang, 1*dip_ang/2, 0,0,0, [0,0,0], [0,dip_K,dip_S])
    bseptinf = marker('bseptinf')   # marker at the end of thin septum
    mseptinf = marker('mseptinf')   # marker at the center of thin septum
    eseptinf = marker('eseptinf')   # marker at the end of thin septum
    septfi    = [bseptinf, h1, mseptinf, ch, h2, eseptinf]   # we excluded ch to make it consistent with other codes. the corrector can be implemented in the polynomB.


    # --- lines ---
    la1   = [l20, l18, cv, [l20]*5, l24]
    la2   = [la2p, [l20]*11, bpm, l20, ch, l25, cv, l20]
    la3   = [l16, l16]
    lb1   = [l20, l20, l17]
    lb2   = [l20, l20, l20]
    lb3   = [lb3p, [l20] * 18, bpm, l20, ch, l25, cv, l25]
    lc1   = [lc1p, [l20] * 9]
    lc2   = [lc2p, bpm, l20, ch, l25, cv, l25]
    ld1   = [[l20] * 5, l15, l15]
    ld2   = [ld2p, l20, l20, bpm, l20, cv, l25, ch, l20]
    ld3   = [l15, l15]
    ld4   = [l15, [l20]*7, bpm, l20, cv, l25]
    line1 = [septex, la1, qf1a, la2, qf1b, la3]
    line2 = [bend, lb1, qd2, lb2, qf2, lb3]
    line3 = [bend, lc1, qf3, lc2]
    line4 = [bend, ld1, qd4a, ld2, qf4, ld3, qd4b, ld4]
    line5 = [septgr, l20, l20, septfi, bpm]
    ltba  = [start, line1, line2, line3, line4, line5, fim]

    ## line extension to PMM
    # l10      = drift('l10', 0.10)
    # lki      = drift('lki', 2.14)
    # lkipmm   = drift('lkipmm', 0.807)
    # MIA      = marker('MIA', )
    # sept_in  = marker('sept_in', )
    # kick_in  = marker('kick_in', )
    # PMM      = marker('PMM', )
    # AN_kipmm = [sept_in, l10, MIA, lki, lkipmm, PMM]
    # ltba_estendido  = [inicio, linea, lineb, linec, lined, linee, AN_kipmm, fim]

    # finalization
    elist = ltba
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

    for i in range(len(the_line)):
        if the_line[i].angle:
            length = the_line[i].length
            the_line[i].nr_steps = int(_math.ceil(length/0.035))
        elif the_line[i].polynom_b[1]:
            the_line[i].nr_steps = 10
        elif the_line[i].polynom_b[2]:
            the_line[i].nr_steps = 5
        else:
            the_line[i].nr_steps = 1

def set_vacuum_chamber(the_line):

    # -- default physical apertures --
    for i in range(len(the_line)):
        the_line[i].hmin = -0.0120
        the_line[i].hmax = +0.0120
        the_line[i].vmin = -0.0120
        the_line[i].vmax = +0.0120

    # -- bo extraction septum --
    beg = _pyaccel.lattice.find_indices(the_line, 'fam_name', 'bseptex')[0]
    end = _pyaccel.lattice.find_indices(the_line, 'fam_name', 'eseptex')[0]
    for i in range(beg,end+1):
        the_line[i].hmin = -0.0015
        the_line[i].hmax = +0.0045
        the_line[i].vmin = -0.0040
        the_line[i].vmax = +0.0040

    # -- si thick injection septum
    beg = _pyaccel.lattice.find_indices(the_line, 'fam_name', 'bsepting')[0]
    end = _pyaccel.lattice.find_indices(the_line, 'fam_name', 'esepting')[0]
    for i in range(beg,end+1):
        the_line[i].hmin = -0.0045
        the_line[i].hmax = +0.0045
        the_line[i].vmin = -0.0035
        the_line[i].vmax = +0.0035

    # -- si thin injection septum
    beg = _pyaccel.lattice.find_indices(the_line, 'fam_name', 'bseptinf')[0]
    end = _pyaccel.lattice.find_indices(the_line, 'fam_name', 'eseptinf')[0]
    for i in range(beg,end+1):
        the_line[i].hmin = -0.0045
        the_line[i].hmax = +0.0015
        the_line[i].vmin = -0.0035
        the_line[i].vmax = +0.0035




_the_line=create_lattice()
