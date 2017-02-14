
import math as _math
import pyaccel as _pyaccel
import numpy as _np
import mathphys as _mp


class LatticeError(Exception):
    pass

energy = 0.15e9 #[eV]
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
    ldif   = 0.1442
    l015   = drift('l015', 0.1500)
    l020   = drift('l020', 0.2000)
    l025   = drift('l025', 0.2500)
    l040   = drift('l040', 0.4000)
    l060   = drift('l060', 0.6000)
    l080   = drift('l080', 0.8000)
    l090   = drift('l090', 0.9000)
    l130   = drift('l130', 1.3000)
    l220   = drift('l220', 2.2000)
    l280   = drift('l280', 2.8000)
    la2p   = drift('la2p', 0.08323)
    lb2p   = drift('lb2p', 0.1330)
    ld2p   = drift('ld2p', 0.1920)
    ld3p   = drift('ld3p', 0.1430)
    la3p   = drift('la3p', 0.2320 -ldif)
    lb1p   = drift('lb1p', 0.2200 -ldif)
    lb3p   = drift('lb3p', 0.19897-ldif)
    lc1p   = drift('lc1p', 0.18704-ldif)
    lc2p   = drift('lc2p', 0.2260 -ldif)
    ld1p   = drift('ld1p', 0.21409-ldif)

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
    qf1a   = quadrupole('QF1A',  0.14, strengths['qf1a'])
    qf1b   = quadrupole('QF1B',  0.14, strengths['qf1b'])
    qd2    = quadrupole('QD2',   0.14, strengths['qd2'])
    qf2    = quadrupole('QF2',   0.20, strengths['qf2'])
    qf3    = quadrupole('QF3',   0.20, strengths['qf3'])
    qd4a   = quadrupole('QD4A',  0.14, strengths['qd4a'])
    qf4    = quadrupole('QF4',   0.20, strengths['qf4'])
    qd4b   = quadrupole('QD4B',  0.14, strengths['qd4b'])

    # --- bending magnets ---
    d2r = (_math.pi/180)

    # -- b --
    f = 5.011542/5.333333;
    h1  = rbend_sirius('B', 0.196, d2r*0.8597*f, 0,0,0,0,0, [0, 0, 0], _np.array([0, -0.163, -1.443, 0])*f)
    h2  = rbend_sirius('B', 0.192, d2r*0.8467*f, 0,0,0,0,0, [0, 0, 0], _np.array([0, -0.154, -1.418, 0])*f)
    h3  = rbend_sirius('B', 0.182, d2r*0.8099*f, 0,0,0,0,0, [0, 0, 0], _np.array([0, -0.140, -1.403, 0])*f)
    h4  = rbend_sirius('B', 0.010, d2r*0.0379*f, 0,0,0,0,0, [0, 0, 0], _np.array([0, -0.175, -1.245, 0])*f)
    h5  = rbend_sirius('B', 0.010, d2r*0.0274*f, 0,0,0,0,0, [0, 0, 0], _np.array([0, -0.115, -0.902, 0])*f)
    h6  = rbend_sirius('B', 0.013, d2r*0.0244*f, 0,0,0,0,0, [0, 0, 0], _np.array([0, -0.042, -1.194, 0])*f)
    h7  = rbend_sirius('B', 0.017, d2r*0.0216*f, 0,0,0,0,0, [0, 0, 0], _np.array([0, -0.008, -1.408, 0])*f)
    h8  = rbend_sirius('B', 0.020, d2r*0.0166*f, 0,0,0,0,0, [0, 0, 0], _np.array([0,  0.004, -1.276, 0])*f)
    h9  = rbend_sirius('B', 0.030, d2r*0.0136*f, 0,0,0,0,0, [0, 0, 0], _np.array([0,  0.006, -0.858, 0])*f)
    h10 = rbend_sirius('B', 0.05,  d2r*0.0089*f, 0,0,0,0,0, [0, 0, 0], _np.array([0,  0.000, -0.050, 0])*f)
    mbend = marker('mB');

    bend = [h10, h9, h8, h7, h6, h5, h4, h3, h2, h1, mbend,
            h1, h2, h3, h4, h5, h6, h7, h8, h9, h10]

    # -- Thin Septum --
    dip_nam =  'EjeSF';
    dip_len =  0.5773;
    dip_ang =  -3.6 * d2r;
    dip_K   =  0.0;
    dip_S   =  0.00;
    h1      = rbend_sirius(dip_nam, dip_len/2, dip_ang/2, 1*dip_ang/2, 0*dip_ang,   0,0,0, [0,0,0], [0,dip_K,dip_S])
    h2      = rbend_sirius(dip_nam, dip_len/2, dip_ang/2, 0*dip_ang/2, 1*dip_ang/2, 0,0,0, [0,0,0], [0,dip_K,dip_S])
    bejesf = marker('bEjeSF') # marker at the beginning of thin septum
    mejesf = marker('mEjeSF') # marker at the center of thin septum
    eejesf = marker('eEjeSF') # marker at the end of thin septum
    ejesf = [bejesf, h1, mejesf, h2, eejesf];


    # -- bo thick ejection septum --
    dip_nam  =  'EjeSG';
    dip_len  =  0.5773;
    dip_ang  =  -3.6 * d2r;
    dip_K    =  0.0;
    dip_S    =  0.00;
    h1       = rbend_sirius(dip_nam, dip_len/2, dip_ang/2, 1*dip_ang/2, 0*dip_ang, 0,0,0, [0,0,0], [0,dip_K,dip_S])
    h2       = rbend_sirius(dip_nam, dip_len/2, dip_ang/2, 0*dip_ang, 1*dip_ang/2, 0,0,0, [0,0,0], [0,dip_K,dip_S])
    bejesg = marker('bEjeSG') # marker at the beginning of thick septum
    mejesg = marker('mEjeSG') # marker at the center of thick septum
    eejesg = marker('eEjeSG') # marker at the end of thick septum
    ejesg = [bejesg, h1, mejesg, h2, eejesg];

    # -- si thick injection septum (2 of these are used) --
    dip_nam  =  'InjSG';
    dip_len  =  0.5773;
    dip_ang  =  +3.6 * d2r;
    dip_K    =  0.0;
    dip_S    =  0.00;
    h1       = rbend_sirius(dip_nam, dip_len/2, dip_ang/2, 1*dip_ang/2, 0*dip_ang, 0,0,0, [0,0,0], [0,dip_K,dip_S])
    h2       = rbend_sirius(dip_nam, dip_len/2, dip_ang/2, 0*dip_ang, 1*dip_ang/2, 0,0,0, [0,0,0], [0,dip_K,dip_S])
    binjsg = marker('bInjSG') # marker at the beginning of thick septum
    minjsg = marker('mInjSG') # marker at the center of thick septum
    einjsg = marker('eInjSG') # marker at the end of thick septum
    injsg = [binjsg, h1, minjsg, h2, einjsg];

    # -- si thin injection septum --
    dip_nam  =  'InjSF';
    dip_len  =  0.5773;
    dip_ang  =  +3.118 * d2r;
    dip_K    =  0.0;
    dip_S    =  0.00;
    h1       = rbend_sirius(dip_nam, dip_len/2, dip_ang/2, 1*dip_ang/2, 0*dip_ang, 0,0,0, [0,0,0], [0,dip_K,dip_S])
    h2       = rbend_sirius(dip_nam, dip_len/2, dip_ang/2, 0*dip_ang, 1*dip_ang/2, 0,0,0, [0,0,0], [0,dip_K,dip_S])
    binjsf = marker('bInjSF') # marker at the beginning of thin septum
    minjsf = marker('mInjSF') # marker at the center of thin septum
    einjsf = marker('eInjSF') # marker at the end of thin septum
    injsf = [binjsf, h1, minjsf, h2, einjsf];


    # --- lines ---
    sec01 = [ejesf,l025,ejesg,l060,cv,l090,qf1a,la2p,ict,l280,scrn,bpm,
             l020,ch,l020,qf1b,l020,cv,l020,la3p,bend]
    sec02 = [l080,lb1p,qd2,lb2p,l080,scrn,bpm,l020,qf2,l020,ch,l025,cv,l015,lb3p,bend]
    sec03 = [lc1p,l220,qf3,l025,scrn,bpm,l020,ch,l025,cv,lc2p,bend]
    sec04 = [ld1p,l130,qd4a,ld2p,l060,scrn,bpm,l020,cv,l025,ch,l020,qf4,ld3p,
             l020,qd4b,l060,fct,l040,ict,l040,scrn,bpm,cv,l020,injsg,l025,injsg,l025,ch,injsf]

    ts  = [inicio,sec01,sec02,sec03,sec04,fim];

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
    beg = _pyaccel.lattice.find_indices(the_line, 'fam_name', 'bEjeSF')[0]
    end = _pyaccel.lattice.find_indices(the_line, 'fam_name', 'eEjeSG')[0]
    for i in range(beg,end+1):
        the_line[i].hmin = -0.0150
        the_line[i].hmax = +0.0150
        the_line[i].vmin = -0.0040
        the_line[i].vmax = +0.0040

    # -- si thick injection septum --
    beg = _pyaccel.lattice.find_indices(the_line, 'fam_name', 'bInjSG')[0]
    end = _pyaccel.lattice.find_indices(the_line, 'fam_name', 'eInjSG')[0]
    for i in range(beg,end+1):
        the_line[i].hmin = -0.0045
        the_line[i].hmax = +0.0045
        the_line[i].vmin = -0.0035
        the_line[i].vmax = +0.0035

    # -- si thin injection septum --
    beg = _pyaccel.lattice.find_indices(the_line, 'fam_name', 'bInjSF')[0]
    end = _pyaccel.lattice.find_indices(the_line, 'fam_name', 'eInjSF')[0]
    for i in range(beg,end+1):
        the_line[i].hmin = -0.0150
        the_line[i].hmax = +0.0150
        the_line[i].vmin = -0.0035
        the_line[i].vmax = +0.0035
