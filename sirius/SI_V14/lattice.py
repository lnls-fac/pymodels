
import math as _math
import pyaccel as _pyaccel
import mathphys as _mp
from . import optics_mode_C03 as _optics_mode_C03
from . import segmented_models as _segmented_models

_default_optics_mode = _optics_mode_C03
_lattice_symmetry = 10
_harmonic_number  = 864
_energy = 3e9 #[eV]

def create_lattice():
    # -- selection of optics mode --
    global _default_optics_mode
    _default_optics_mode = _optics_mode_C03

    # -- shortcut symbols --
    marker = _pyaccel.elements.marker
    drift = _pyaccel.elements.drift
    quadrupole = _pyaccel.elements.quadrupole
    sextupole = _pyaccel.elements.sextupole
    rbend_sirius = _pyaccel.elements.rbend
    rfcavity = _pyaccel.elements.rfcavity
    strengths = _default_optics_mode.strengths

    # -- drifts --
    LKK   = drift('lkk',  1.7630)
    LPMU  = drift('lpmu', 0.3220)
    LPMD  = drift('lpmd', 0.4629)
    LIA   = drift('lia2', 1.5179)
    LIB   = drift('lib2', 1.0879)
    L035  = drift('l035', 0.035)
    L050  = drift('l050', 0.050)
    L061  = drift('l061', 0.061)
    L066  = drift('l066', 0.066)
    L074  = drift('l074', 0.074)
    L077  = drift('l077', 0.077)
    L081  = drift('l081', 0.081)
    L083  = drift('l083', 0.083)
    L105  = drift('l105', 0.105)
    L112  = drift('l112', 0.112)
    L125  = drift('l125', 0.125)
    L134  = drift('l134', 0.134)
    L135  = drift('l135', 0.135)
    L140  = drift('l140', 0.140)
    L150  = drift('l150', 0.150)
    L155  = drift('l155', 0.155)
    L170  = drift('l170', 0.170)
    L216  = drift('l216', 0.216)
    L230  = drift('l230', 0.230)
    L240  = drift('l240', 0.240)
    L267  = drift('l267', 0.267)
    L270  = drift('l270', 0.270)
    L275  = drift('l275', 0.275)
    L336  = drift('l336', 0.336)
    L419  = drift('l419', 0.419)
    L474  = drift('l474', 0.474)
    L500  = drift('l500', 0.500)
    L537  = drift('l537', 0.537)
    L715  = drift('l715', 0.715)

    # -- lattice markers --
    m_accep_fam_name = 'calc_mom_accep';

    #START    = marker('start')          # start of the model
    #END      = marker('end')            # end of the model
    #MIA      = marker('mia')            # center of long straight sections (even-numbered)
    #MIB      = marker('mib')            # center of short straight sections (odd-numbered)
    #MIDA     = marker('id_enda')        # marker for the extremities of IDs in long straight sections
    #MIDB     = marker('id_endb')        # marker for the extremities of IDs in short straight sections
    #MOMACCEP = marker('calc_mom_accep') # marker to define points where momentum acceptance will be calculated
    #SEPT_IN  = marker('eseptinf')       # end of thin injection septum

    # -- dipoles --
    BC = _segmented_models.dipole_bc(m_accep_fam_name)
    B1 = _segmented_models.dipole_b1(m_accep_fam_name)
    B2 = _segmented_models.dipole_b2(m_accep_fam_name)

    # -- quadrupoles --
    QDA  = _segmented_models.quadrupole_q14('qda',  strengths['qda'])
    QDB2 = _segmented_models.quadrupole_q14('qdb2', strengths['qdb2'])
    QDB1 = _segmented_models.quadrupole_q14('qdb1', strengths['qdb1'])
    QFA  = _segmented_models.quadrupole_q20('qfa',  strengths['qfa'])
    QF1  = _segmented_models.quadrupole_q20('qf1',  strengths['qf1'])
    QF2  = _segmented_models.quadrupole_q20('qf2',  strengths['qf2'])
    QF3  = _segmented_models.quadrupole_q20('qf3',  strengths['qf3'])
    QF4  = _segmented_models.quadrupole_q20('qf4',  strengths['qf4'])
    QFB  = _segmented_models.quadrupole_q30('qfb',  strengths['qfb'])

    # -- sextupoles --
    SFA  = sextupole('sfa',   0.150, strengths['sfa'])  # CH-CV
    SDA  = sextupole('sda',   0.150, strengths['sda'])  # QS
    SD1J = sextupole('sd1j',  0.150, strengths['sd1j']) # CH-CV
    SF1J = sextupole('sf1j',  0.150, strengths['sf1j']) # QS
    SD2J = sextupole('sd2j',  0.150, strengths['sd2j']) # --
    SD3J = sextupole('sd3j',  0.150, strengths['sd3j']) # CV
    SF2J = sextupole('sf2j',  0.150, strengths['sf2j']) # CH
    SF2K = sextupole('sf2k',  0.150, strengths['sf2k']) # CH-CV
    SD3K = sextupole('sd3k',  0.150, strengths['sd3k']) # CV
    SD2K = sextupole('sd2k',  0.150, strengths['sd2k']) # --
    SF1K = sextupole('sf1k',  0.150, strengths['sf1k']) # QS
    SD1K = sextupole('sd1k',  0.150, strengths['sd1k']) # CH-CV
    SDB  = sextupole('sdb',   0.150, strengths['sdb'])  # QS
    SFB  = sextupole('sfb',   0.150, strengths['sfb'])  # CH-CV

    # -- slow vertical corrector --
    CV   = sextupole('cv',    0.150, 0.0)

    # -- pulsed magnets --
    KICKIN = sextupole('kick_in', 0.500, S=0.0) # injection kicker
    PMM    = sextupole('pmm',     0.470, S=0.0) # pulsed multipole magnet

    # -- bpms and fast correctors --
    BPM    = marker('bpm')
    FC     = sextupole('fc', 0.100, S=0.0)
    RBPM   = marker('rbpm')

    # -- rf cavities --
    RFC = rfcavity('cav', 0, 3.0e6, 500e6)

    # -- lattice markers --
    START  = marker('start')    # start of the model
    END    = marker('end')      # end of the model
    MIA    = marker('mia')      # center of long straight sections (even-numbered)
    MIB    = marker('mib')      # center of short straight sections (odd-numbered)
    GIR    = marker('girder')   # marker used to delimitate girders. one marker at begin and another at end of girder.
    MIDA   = marker('id_enda')  # marker for the extremities of IDs in long straight sections
    MIDB   = marker('id_endb')  # marker for the extremities of IDs in short straight sections
    SEPTIN = marker('eseptinf') # end of injection septum
    DCCT1  = marker('dcct1')    # dcct1 to measure beam current
    DCCT2  = marker('dcct2')    # dcct2 to measure beam current

    # -- transport lines --
    M2A    = [GIR,BPM,RBPM,L135,SFA,L150,QFA,L074,FC,L066,SDA,L150,QDA,GIR,L134,GIR];                                  # high beta xxM2 girder (with fasc corrector)
    M1A    = M2A[::-1]                                                                                                 # high beta xxM1 girder (with fast correctors)
    IDA    = [L500,LIA,L500,MIDA,L500,L500,MIA,L500,L500,MIDA,L500,LIA,L500];                                          # high beta ID straight section
    CAV    = [L500,LIA,L500,L500,L500,MIA,RFC,L500,L500,L500,LIA,L500];                                                # high beta RF cavity straight section
    INJ    = [L500,LIA,L419,SEPTIN,L500,L500,L081,END,START,MIA, LKK, KICKIN, LPMU, PMM, LPMD];                        # high beta INJ straight section
    M1B    = [GIR,L134,GIR,QDB1,L150,SDB,L240,QFB,L150,SFB,L050,FC,L035,QDB2,L140,BPM,RBPM,GIR];                       # low beta xxM1 girder
    M2B    = M1B[::-1]                                                                                                 # low beta xxM2 girder
    IDB    = [L500,LIB,L500,MIDB,L500,L500,MIB,L500,L500,MIDB,L500,LIB,L500];                                          # low beta ID straight section

    C1A      = [GIR,L474,GIR,SD1J,L170,QF1,L135,BPM,L125,SF1J,L230,QF2,L170,SD2J,GIR,L155,GIR,BPM,L061];                 # arc sector in between B1-B2 (high beta odd-numbered straight sections)
    C1B      = [GIR,L474,GIR,SD1K,L170,QF1,L135,BPM,L125,SF1K,L230,QF2,L170,SD2K,GIR,L155,GIR,BPM,L061];                 # arc sector in between B1-B2 (low beta even-numbered straight sections)
    C2A      = [GIR,L336,GIR,SD3J,L170,QF3,L230,SF2J,L077,FC,L083,QF4,GIR,L537,GIR,CV,L105,BPM,RBPM,L035];               # arc sector in between B2-BC (high beta odd-numbered straight sections)
    C2B      = [GIR,L336,GIR,SD3K,L170,QF3,L230,SF2K,L077,FC,L083,QF4,GIR,L537,GIR,CV,L105,BPM,RBPM,L035];               # arc sector in between B2-BC (low beta even-numbered straight sections)
    C2A_DCCT = [GIR,L336,GIR,SD3J,L170,QF3,L230,SF2J,L077,FC,L083,QF4,GIR,L270,DCCT1,L267,GIR,CV,L105,BPM,RBPM,L035];    # arc sector in between B2-BC with DCCT1 (high beta odd-numbered straight sections)
    C2B_DCCT = [GIR,L336,GIR,SD3K,L170,QF3,L230,SF2K,L077,FC,L083,QF4,GIR,L270,DCCT2,L267,GIR,CV,L105,BPM,RBPM,L035];    # arc sector in between B2-BC with DCCT2 (low beta even-numbered straight sections)
    C3A      = [GIR,L715,GIR,BPM,RBPM,L112,QF4,L083,FC,L077,SF2K,L230,QF3,L170,SD3K,GIR,L275,GIR,BPM,L061];              # arc sector in between BC-B2 (high beta odd-numbered straight sections)
    C3B      = [GIR,L715,GIR,BPM,RBPM,L112,QF4,L083,FC,L077,SF2J,L230,QF3,L170,SD3J,GIR,L275,GIR,BPM,L061];              # arc sector in between BC-B2 (low beta even-numbered straight sections)
    C4A      = [GIR,L216,GIR,SD2K,L170,QF2,L230,SF1K,L125,BPM,L135,QF1,L170,SD1K,GIR,L474,GIR];                          # arc sector in between B2-B1 (high beta odd-numbered straight sections)
    C4B      = [GIR,L216,GIR,SD2J,L170,QF2,L230,SF1J,L125,BPM,L135,QF1,L170,SD1J,GIR,L474,GIR];                          # arc sector in between B2-B1 (low beta even-numbered straight sections)

    # -- girders --

    # straight sections
    SS_S01 = INJ; SS_S02 = IDB;
    SS_S03 = CAV; SS_S04 = IDB;
    SS_S05 = IDA; SS_S06 = IDB;
    SS_S07 = IDA; SS_S08 = IDB;
    SS_S09 = IDA; SS_S10 = IDB;
    SS_S11 = IDA; SS_S12 = IDB;
    SS_S13 = IDA; SS_S14 = IDB;
    SS_S15 = IDA; SS_S16 = IDB;
    SS_S17 = IDA; SS_S18 = IDB;
    SS_S19 = IDA; SS_S20 = IDB;

    # down and upstream straight sections
    M1_S01 = M1A; M2_S01 = M2A; M1_S02 = M1B; M2_S02 = M2B;
    M1_S03 = M1A; M2_S03 = M2A; M1_S04 = M1B; M2_S04 = M2B;
    M1_S05 = M1A; M2_S05 = M2A; M1_S06 = M1B; M2_S06 = M2B;
    M1_S07 = M1A; M2_S07 = M2A; M1_S08 = M1B; M2_S08 = M2B;
    M1_S09 = M1A; M2_S09 = M2A; M1_S10 = M1B; M2_S10 = M2B;
    M1_S11 = M1A; M2_S11 = M2A; M1_S12 = M1B; M2_S12 = M2B;
    M1_S13 = M1A; M2_S13 = M2A; M1_S14 = M1B; M2_S14 = M2B;
    M1_S15 = M1A; M2_S15 = M2A; M1_S16 = M1B; M2_S16 = M2B;
    M1_S17 = M1A; M2_S17 = M2A; M1_S18 = M1B; M2_S18 = M2B;
    M1_S19 = M1A; M2_S19 = M2A; M1_S20 = M1B; M2_S20 = M2B;

    # dispersive arcs
    C1_S01 = C1A; C2_S01 = C2A; C3_S01 = C3A; C4_S01 = C4A;
    C1_S02 = C1B; C2_S02 = C2B; C3_S02 = C3B; C4_S02 = C4B;
    C1_S03 = C1A; C2_S03 = C2A; C3_S03 = C3A; C4_S03 = C4A;
    C1_S04 = C1B; C2_S04 = C2B; C3_S04 = C3B; C4_S04 = C4B;
    C1_S05 = C1A; C2_S05 = C2A; C3_S05 = C3A; C4_S05 = C4A;
    C1_S06 = C1B; C2_S06 = C2B; C3_S06 = C3B; C4_S06 = C4B;
    C1_S07 = C1A; C2_S07 = C2A; C3_S07 = C3A; C4_S07 = C4A;
    C1_S08 = C1B; C2_S08 = C2B; C3_S08 = C3B; C4_S08 = C4B;
    C1_S09 = C1A; C2_S09 = C2A; C3_S09 = C3A; C4_S09 = C4A;
    C1_S10 = C1B; C2_S10 = C2B; C3_S10 = C3B; C4_S10 = C4B;
    C1_S11 = C1A; C2_S11 = C2A; C3_S11 = C3A; C4_S11 = C4A;
    C1_S12 = C1B; C2_S12 = C2B; C3_S12 = C3B; C4_S12 = C4B;
    C1_S13 = C1A; C2_S13 = C2A_DCCT; C3_S13 = C3A; C4_S13 = C4A;
    C1_S14 = C1B; C2_S14 = C2B_DCCT; C3_S14 = C3B; C4_S14 = C4B;
    C1_S15 = C1A; C2_S15 = C2A; C3_S15 = C3A; C4_S15 = C4A;
    C1_S16 = C1B; C2_S16 = C2B; C3_S16 = C3B; C4_S16 = C4B;
    C1_S17 = C1A; C2_S17 = C2A; C3_S17 = C3A; C4_S17 = C4A;
    C1_S18 = C1B; C2_S18 = C2B; C3_S18 = C3B; C4_S18 = C4B;
    C1_S19 = C1A; C2_S19 = C2A; C3_S19 = C3A; C4_S19 = C4A;
    C1_S20 = C1B; C2_S20 = C2B; C3_S20 = C3B; C4_S20 = C4B;

    ## SECTORS # 01..20

    S01 = [M1_S01, SS_S01, M2_S01, B1, C1_S01, B2, C2_S01, BC, C3_S01, B2, C4_S01, B1]
    S02 = [M1_S02, SS_S02, M2_S02, B1, C1_S02, B2, C2_S02, BC, C3_S02, B2, C4_S02, B1]
    S03 = [M1_S03, SS_S03, M2_S03, B1, C1_S03, B2, C2_S03, BC, C3_S03, B2, C4_S03, B1]
    S04 = [M1_S04, SS_S04, M2_S04, B1, C1_S04, B2, C2_S04, BC, C3_S04, B2, C4_S04, B1]
    S05 = [M1_S05, SS_S05, M2_S05, B1, C1_S05, B2, C2_S05, BC, C3_S05, B2, C4_S05, B1]
    S06 = [M1_S06, SS_S06, M2_S06, B1, C1_S06, B2, C2_S06, BC, C3_S06, B2, C4_S06, B1]
    S07 = [M1_S07, SS_S07, M2_S07, B1, C1_S07, B2, C2_S07, BC, C3_S07, B2, C4_S07, B1]
    S08 = [M1_S08, SS_S08, M2_S08, B1, C1_S08, B2, C2_S08, BC, C3_S08, B2, C4_S08, B1]
    S09 = [M1_S09, SS_S09, M2_S09, B1, C1_S09, B2, C2_S09, BC, C3_S09, B2, C4_S09, B1]
    S10 = [M1_S10, SS_S10, M2_S10, B1, C1_S10, B2, C2_S10, BC, C3_S10, B2, C4_S10, B1]
    S11 = [M1_S11, SS_S11, M2_S11, B1, C1_S11, B2, C2_S11, BC, C3_S11, B2, C4_S11, B1]
    S12 = [M1_S12, SS_S12, M2_S12, B1, C1_S12, B2, C2_S12, BC, C3_S12, B2, C4_S12, B1]
    S13 = [M1_S13, SS_S13, M2_S13, B1, C1_S13, B2, C2_S13, BC, C3_S13, B2, C4_S13, B1]
    S14 = [M1_S14, SS_S14, M2_S14, B1, C1_S14, B2, C2_S14, BC, C3_S14, B2, C4_S14, B1]
    S15 = [M1_S15, SS_S15, M2_S15, B1, C1_S15, B2, C2_S15, BC, C3_S15, B2, C4_S15, B1]
    S16 = [M1_S16, SS_S16, M2_S16, B1, C1_S16, B2, C2_S16, BC, C3_S16, B2, C4_S16, B1]
    S17 = [M1_S17, SS_S17, M2_S17, B1, C1_S17, B2, C2_S17, BC, C3_S17, B2, C4_S17, B1]
    S18 = [M1_S18, SS_S18, M2_S18, B1, C1_S18, B2, C2_S18, BC, C3_S18, B2, C4_S18, B1]
    S19 = [M1_S19, SS_S19, M2_S19, B1, C1_S19, B2, C2_S19, BC, C3_S19, B2, C4_S19, B1]
    S20 = [M1_S20, SS_S20, M2_S20, B1, C1_S20, B2, C2_S20, BC, C3_S20, B2, C4_S20, B1]

    anel = [S01,S02,S03,S04,S05,S06,S07,S08,S09,S10,S11,S12,S13,S14,S15,S16,S17,S18,S19,S20]
    anel = _mp.utils.flatten(anel)

    the_ring = _pyaccel.lattice.build(anel)

    # -- shifts model to marker 'start'
    idx = _pyaccel.lattice.find_indices(the_ring, 'fam_name', 'start')
    the_ring = _pyaccel.lattice.shift(the_ring, idx[0])

    # -- sets rf frequency
    set_rf_frequency(the_ring)

    # -- sets number of integration steps
    set_num_integ_steps(the_ring)

    # -- define vacuum chamber for all elements
    set_vacuum_chamber(the_ring)

    return the_ring


def set_rf_frequency(the_ring):
    circumference = _pyaccel.lattice.length(the_ring)

    #_, beam_velocity, _, _, _ = _mp.beam_optics.beam_rigidity(energy=_energy)
    #velocity = beam_velocity
    velocity = _mp.constants.light_speed
    rev_frequency = velocity / circumference
    rf_frequency  = _harmonic_number * rev_frequency
    idx = _pyaccel.lattice.find_indices(the_ring, 'fam_name', 'cav')
    for i in idx:
        the_ring[i].frequency = rf_frequency


def set_num_integ_steps(the_ring):
    len_bends = 0.050
    len_quads = 0.015
    len_sexts = 0.015
    for i in range(len(the_ring)):
        if the_ring[i].angle:
            nr_steps = int(_math.ceil(the_ring[i].length/len_bends))
            the_ring[i].nr_steps = nr_steps
        elif the_ring[i].polynom_b[2]:
            nr_steps = int(_math.ceil(the_ring[i].length/len_sexts))
            the_ring[i].nr_steps = nr_steps
        elif the_ring[i].polynom_b[1] or the_ring[i].fam_name in ['fc','kick_in','pmm']:
            nr_steps = int(_math.ceil(the_ring[i].length/len_quads))
            #if the_ring[i].fam_name == 'kick_in':
            #    print(nr_steps)
            the_ring[i].nr_steps = nr_steps



def set_vacuum_chamber(the_ring):

    # vchamber = [hmin, hmax, vmin, vmax] (meter)
    bc_chamber     = [-0.012, 0.012, -0.00400, 0.00400]
    other_vchamber = [-0.012, 0.012, -0.01200, 0.01200]
    ivu_vchamber   = [-0.012, 0.012, -0.00225, 0.00225]
    ovu_vchamber   = [-0.012, 0.012, -0.00400, 0.00400]
    inj_vchamber   = [-0.030, 0.012, -0.01200, 0.01200]

    # sets default value
    for i in range(len(the_ring)):
        e = the_ring[i]
        e.hmin, e.hmax, e.vmin, e.vmax = other_vchamber

    # -- physical limit at Low Beta Sections--
    ivu = _pyaccel.lattice.find_indices(the_ring, 'fam_name', 'id_endb')
    ivu_list = []; [ivu_list.extend(list(range(ivu[2*i],ivu[2*i+1]+1))) for i in range(len(ivu)//2)]
    for i in ivu_list:
        e = the_ring[i]
        e.hmin, e.hmax, e.vmin, e.vmax = ivu_vchamber

    # -- physical limit at High Beta Sections --
    ovu = _pyaccel.lattice.find_indices(the_ring, 'fam_name', 'id_enda')
    ovu_list = []; [ovu_list.extend(list(range(ovu[2*i],ovu[2*i+1]+1))) for i in range(len(ovu)//2)]
    for i in ovu_list:
        e = the_ring[i]
        e.hmin, e.hmax, e.vmin, e.vmax = ovu_vchamber

    # -- physical limit at injection section --
    sept_in  = _pyaccel.lattice.find_indices(the_ring, 'fam_name', 'eseptinf')[-1] # physics end of thin septum
    kick_in  = _pyaccel.lattice.find_indices(the_ring, 'fam_name', 'kick_in')[0]  # start of kicker
    inj_list = list(range(sept_in,len(the_ring))) + list(range(0,kick_in+1))
    for i in inj_list:
        e = the_ring[i]
        e.hmin, e.hmax, e.vmin, e.vmax = inj_vchamber
