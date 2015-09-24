
import math as _math
import pyaccel as _pyaccel
import mathphys as _mp
from . import optics_mode_M0 as _optics_mode_M0

_default_optics_mode = _optics_mode_M0
_energy = 3e9 #[eV]
# _initial_twiss = _pyaccel.optics.Twiss.make_new(spos=0.0,
#                                                 fixed_point=[0,0,0,0,0,0], # nominal orbit of LI w.r.t. TB coord. sys.
#                                                 mu=[0.0,0.0],
#                                                 beta=[6.57, 15.30],
#                                                 alpha=[-2.155, 2.22],
#                                                 eta=[0.191,0],
#                                                 etal=[0.0689,0])


def create_lattice():

    # -- selection of optics mode --
    global _default_optics_mode
    _default_optics_mode = _optics_mode_M0

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
    l15  = drift('l15', 0.15)
    l16  = drift('l16', 0.16)
    l18  = drift('l18', 0.18)
    l20  = drift('l20', 0.20)
    l22  = drift('l22', 0.22)
    l24  = drift('l24', 0.24)
    l25  = drift('l25', 0.25)
    l40  = drift('l40', 0.40)
    la2p = drift('la2p', 0.13777)
    lb3p = drift('lb3p', 0.27883)
    lc3p = drift('lc3p', 0.13615)
    ld2p = drift('ld2p', 0.13933)

    l18c  = drift('l18c', 0.18 - c_length/2.0)
    l20c  = drift('l20c', 0.20 - c_length/2.0)
    l25c  = drift('l25c', 0.25 - c_length/2.0)
    l25cc = drift('l25cc', 0.25 - c_length)

    # -- lattice markers --
    start   = marker('start')
    end     = marker('end')

    # -- quadrupoles --
    qa1 = quadrupole('qf1a', 0.14, strengths['qf1a'])
    qa2 = quadrupole('qf1b', 0.14, strengths['qf1b'])
    qb1 = quadrupole('qd2',  0.14, strengths['qd2'])
    qb2 = quadrupole('qf2',  0.14, strengths['qf2'])
    qc1 = quadrupole('qd3',  0.14, strengths['qd3'])
    qc2 = quadrupole('qf3',  0.20, strengths['qf3'])
    qd1 = quadrupole('qd4a', 0.14, strengths['qd4a'])
    qd2 = quadrupole('qf4',  0.20, strengths['qf4'])
    qd3 = quadrupole('qd4b', 0.14, strengths['qd4b'])

    # -- bpms --
    bpm = marker('bpm')

    # -- correctors --
    ch = quadrupole('hcm', c_length, 0.0)
    cv = quadrupole('vcm', c_length, 0.0)

    # -- bending magnets --
    deg2rad = _math.pi/180.0

    # -- dipoles --
    mbend   = marker('mbend')   # marker at center of dipoles
    h1 = rbend_sirius('bend', 1.151658/2, 5.333333*deg2rad/2, 5.333333*deg2rad/2, 0, 0, 0, 0, [0, 0, 0], [0, 0, 0])
    h2 = rbend_sirius('bend', 1.151658/2, 5.333333*deg2rad/2, 0, 5.333333*deg2rad/2, 0, 0, 0, [0, 0, 0], [0, 0, 0])
    bend = [h1, mbend, h2]

    # -- BO extraction septa --
    bseptex = marker('bseptex') # marker at the beginning of extraction septum
    mseptex = marker('mseptex') # marker at center of extraction septa
    h1 = rbend_sirius('septex', 0.85/2, -3.6*deg2rad/2, -3.6*deg2rad/2, 0, 0, 0, 0, [0, 0, 0], [0, 0, 0])
    h2 = rbend_sirius('septex', 0.85/2, -3.6*deg2rad/2, 0, -3.6*deg2rad/2, 0, 0, 0, [0, 0, 0], [0, 0, 0])
    septum = [h1, mseptex, h2]
    septex = [bseptex, septum, l20, septum]

    # -- SI injection thick septum --
    mseptin_a  = marker('msepting') # marker at center of thick septum
    h1 = rbend_sirius('septing', 1.10/2, 6.2*deg2rad/2, 6.2*deg2rad/2, 0, 0, 0, 0, [0, 0, 0], [0, 0, 0])
    h2 = rbend_sirius('septing', 1.10/2, 6.2*deg2rad/2, 0, 6.2*deg2rad/2, 0, 0, 0, [0, 0, 0], [0, 0, 0])
    septgr  = [h1, mseptin_a, h2]

    # -- SI injection thin septum --
    mseptin_b = marker('mseptinf') # marker at center of thin si injection septum
    eseptin_b = marker('eseptinf') # marker at the end of thin si injection septum
    h1 = rbend_sirius('septinf', 0.925/2, 3.13*deg2rad/2, 3.13*deg2rad/2, 0, 0, 0, 0, [0, 0, 0], [0, 0, 0])
    h2 = rbend_sirius('septinf', 0.925/2, 3.13*deg2rad/2, 0, 3.13*deg2rad/2, 0, 0, 0, [0, 0, 0], [0, 0, 0])
    septfi = [h1, mseptin_b, h2, eseptin_b]

    # -- lines --
    la1   = [l20, l18c, cv, l20c, l40, l40]
    la2   = [la2p, l20, l40, l40, l40, l40, l40, bpm, l20c, ch, l25cc, cv, l20c]
    la3   = [l16, l16]
    lb1   = [l20, l40]
    lb2   = [l20, l40]
    lb3   = [lb3p, l40, l40, l40, l40, l40, l40, l40, l40, l40, bpm, l20c, ch, l25cc, cv, l25c]
    lc1   = [l15, l20, l40, l40]
    lc2   = [l22, l20, l40]
    lc3   = [lc3p, bpm, l20c, ch, l25cc, cv, l25c]
    ld1   = [l20, l40, l40, l15, l15]
    ld2   = [ld2p, l40, bpm, l20c, cv, l25cc, ch, l20c]
    ld3   = [l15, l15]
    ld4   = [l15, l20, l40, l40, l40, bpm, l20c, cv, l25c]
    linea = [septex, la1, qa1, la2, qa2, la3]
    lineb = [bend, lb1, qb1, lb2, qb2, lb3]
    linec = [bend, lc1, qc1, lc2, qc2, lc3]
    lined = [bend, ld1, qd1, ld2, qd2, ld3, qd3, ld4]
    linee = [septgr, l40, septfi]
    ltba  = [start, linea, lineb, linec, lined, linee, end]


    # line extension to PMM
    # l10      = drift('l10', 0.10)
    # lki      = drift('lki', 2.14)
    # lkipmm   = drift('lkipmm', 0.807)
    # MIA      = marker('MIA')
    # sept_in  = marker('sept_in')
    # kick_in  = marker('kick_in')
    # PMM      = marker('PMM')
    # AN_kipmm = [sept_in, l10, MIA, lki, lkipmm, PMM]
    # ltba_estendido  = [start, linea, lineb, linec, lined, linee, AN_kipmm, end]

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

    for i in range(len(the_line)):
        the_line[i].hmin = -0.016
        the_line[i].hmax = +0.016
        the_line[i].vmin = -0.016
        the_line[i].vmax = +0.016

        if the_line[i].fam_name == 'bseptex': # vacuum chamber at the beginning of extraction septum
            the_line[i].hmin = -0.0015

        if the_line[i].fam_name == 'eseptinf': # vacuum chamber at the end of injection septum
            the_line[i].hmax = 0.0015
