
import math as _math
import pyaccel as _pyaccel
import mathphys as _mp


class LatticeError(Exception):
    pass

energy = 0.15e9 #[eV]
default_optics_mode = 'M1'

def create_lattice(optics_mode = default_optics_mode):

    strengths = get_optics_mode(optics_mode)

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
    l060   = drift('l060', 0.6000)
    l080   = drift('l080', 0.8000)
    l090   = drift('l090', 0.9000)
    l130   = drift('l130', 1.3000)
    l140   = drift('l140', 1.4000)
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
    deg_2_rad = (_math.pi/180)

    # -- b --
    f = 5.011542/5.333333;
    h1  = rbend_sirius('B', 0.196, d2r*0.8597*f, 0,0,0,0,0,_np.array([0, 0, 0]), _np.array([0, -0.163, -1.443, 0])*f)
    h2  = rbend_sirius('B', 0.192, d2r*0.8467*f, 0,0,0,0,0,_np.array([0, 0, 0]), _np.array([0, -0.154, -1.418, 0])*f)
    h3  = rbend_sirius('B', 0.182, d2r*0.8099*f, 0,0,0,0,0,_np.array([0, 0, 0]), _np.array([0, -0.140, -1.403, 0])*f)
    h4  = rbend_sirius('B', 0.010, d2r*0.0379*f, 0,0,0,0,0,_np.array([0, 0, 0]), _np.array([0, -0.175, -1.245, 0])*f)
    h5  = rbend_sirius('B', 0.010, d2r*0.0274*f, 0,0,0,0,0,_np.array([0, 0, 0]), _np.array([0, -0.115, -0.902, 0])*f)
    h6  = rbend_sirius('B', 0.013, d2r*0.0244*f, 0,0,0,0,0,_np.array([0, 0, 0]), _np.array([0, -0.042, -1.194, 0])*f)
    h7  = rbend_sirius('B', 0.017, d2r*0.0216*f, 0,0,0,0,0,_np.array([0, 0, 0]), _np.array([0, -0.008, -1.408, 0])*f)
    h8  = rbend_sirius('B', 0.020, d2r*0.0166*f, 0,0,0,0,0,_np.array([0, 0, 0]), _np.array([0,  0.004, -1.276, 0])*f)
    h9  = rbend_sirius('B', 0.030, d2r*0.0136*f, 0,0,0,0,0,_np.array([0, 0, 0]), _np.array([0,  0.006, -0.858, 0])*f)
    h10 = rbend_sirius('B', 0.05,  d2r*0.0089*f, 0,0,0,0,0,_np.array([0, 0, 0]), _np.array([0,  0.000, -0.050, 0])*f)
    mbend = marker('mB');

    bend = [h10 h9 h8 h7 h6 h5 h4 h3 h2 h1 mbend h1 h2 h3 h4 h5 h6 h7 h8 h9 h10]

    # -- sep --
    dip_nam =  'InjS'
    dip_len =  0.50
    dip_ang =  21.75 * deg_2_rad
    dip_K   =  0.0
    dip_S   =  0.00
    septine = rbend_sirius(dip_nam, dip_len/2, dip_ang/2, 1*dip_ang/2, 0*dip_ang, 0,0,0, [0,0,0], [0,dip_K,dip_S])
    septins = rbend_sirius(dip_nam, dip_len/2, dip_ang/2, 0*dip_ang, 1*dip_ang/2, 0,0,0, [0,0,0], [0,dip_K,dip_S])
    bseptin = marker('bInjS')
    eseptin = marker('eInjS')
    septin  = [bseptin, septine, septins, eseptin]

    # --- lines ---
    s01_1   = [lb1p, l200, l200, scrn, bpm, l150c, ch, l100cc, cv, l150c]
    s01_2   = [lb2p, l200]
    s01_3   = [l200, l200, l200, l200, l200, l200, hslit, scrn, bpm, l150c, cv, l100cc, ch, l200c, vslit, l200, lb3p]
    s02_1   = [l200, l200, ict, l200, l200, l100]
    s02_2   = [l200, scrn, bpm, l150c, ch, l100cc, cv, l200c] + 25*[l200] + [lc3p]
    s02_3   = [l150, l150, l150, scrn, bpm, l150c, ch, l100cc, cv, l200c]
    ld1     = [ld1p] + 10*[l200]
    s03_1   = [ld3p, scrn, bpm, l150c, ch, l200c]
    s04_1   = [l200c, cv, l200c, l200, l200, l200, l200, l200, ict, le1p]
    s04_2   = [l150, scrn, bpm, l150c, cv, l100c]

    sector01 = [s01_1, qd1, s01_2, qf1, s01_3, bn]
    sector02 = [s02_1, qd2a, lc2, qf2a, s02_2, qf2b, lc4, qd2b, s02_3, bp]
    sector03 = [ld1, qf3, ld2, qd3, s03_1, bp]
    sector04 = [s04_1, qf4, le2, qd4, s04_2, septin]

    ## TB beamline beginning with end of linac
    ltlb  = [inicio, sector01, sector02, sector03, sector04, fim]

    #ltlb  = [inicio, sector01, sector02, sector03, sector04, fim]

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


def get_optics_mode(optics_mode):
    # -- selection of optics mode --
    if optics_mode == 'M1':
        strengths = {
            'qd1'  : -8.420879613851,
            'qf1'  : 13.146671512202,
            'qd2a' : -5.003211465479,
            'qf2a' :  6.783244529016,
            'qf2b' :  2.895212566505,
            'qd2b' : -2.984706731539,
            'qf3'  :  7.963034094957,
            'qd3'  : -2.013774809345,
            'qf4'  : 11.529185003262,
            'qd4'  : -7.084093211983,
        }
    elif optics_mode == 'M2':
        strengths = {
            'qd1'  :   -8.420884154134,
            'qf1'  :   13.146672851601,
            'qd2a' :   -5.786996070251,
            'qf2a' :   7.48800218842,
            'qf2b' :   3.444273863854,
            'qd2b' :   -4.370692899919,
            'qf3'  :   9.275556378041,
            'qd3'  :   -3.831727343173,
            'qf4'  :   11.774551301802,
            'qd4'  :   -7.239923812237,
        }
    elif optics_mode == 'M3':
        strengths = {
            'qd1'  :   -8.4202421458,
            'qf1'  :   13.146512110234,
            'qd2a' :   -4.742318522445,
            'qf2a' :   6.865529327161,
            'qf2b' :   3.644627263975,
            'qd2b' :   -3.640344975066,
            'qf3'  :   6.882094963212,
            'qd3'  :   -0.650373210524,
            'qf4'  :   11.456881278596,
            'qd4'  :   -7.183997114808,
        }
    elif optics_mode == 'M4':
        strengths = {
            'qd1'  :   -8.420952075727,
            'qf1'  :   13.146690356394,
            'qd2a' :   -6.698085523725,
            'qf2a' :   7.789621927907,
            'qf2b' :   2.77064582429,
            'qd2b' :   -3.328855564917,
            'qf3'  :   8.734105391772,
            'qd3'  :   -3.014211757657,
            'qf4'  :   11.424069037719,
            'qd4'  :   -6.740424372291,
        }
    elif optics_mode == 'M5':
        strengths = {
            'qd1'  :   -8.420850561756,
            'qf1'  :   13.146666514846,
            'qd2a' :   -5.621149037043,
            'qf2a' :   8.967988594169,
            'qf2b' :   2.958960220371,
            'qd2b' :   -3.210342770435,
            'qf3'  :   8.311858252882,
            'qd3'  :   -2.442934101437,
            'qf4'  :   11.391698651189,
            'qd4'  :   -6.772341213215,
        }
    elif optics_mode == 'M6':
        strengths = {
            'qd1'  :   -8.420886991042,
            'qf1'  :   13.146673683891,
            'qd2a' :   -5.452694879372,
            'qf2a' :   7.345924165318,
            'qf2b' :   3.605078182875,
            'qd2b' :   -4.255957305622,
            'qf3'  :   8.858246721391,
            'qd3'  :   -3.243238337219,
            'qf4'  :   11.728866700839,
            'qd4'  :   -7.246970930681,
        }
    else:
        Exception('Invalid TS optics mode: ' + optics_mode)

    return strengths


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

    ch_indices = _pyaccel.lattice.find_indices(the_line, 'fam_name', 'CH')
    cv_indices = _pyaccel.lattice.find_indices(the_line, 'fam_name', 'CV')
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
    beg = _pyaccel.lattice.find_indices(the_line, 'fam_name', 'bInjS')[0]
    end = _pyaccel.lattice.find_indices(the_line, 'fam_name', 'eInjS')[0]
    for i in range(beg,end+1):
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
