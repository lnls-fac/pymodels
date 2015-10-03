
import math as _math
import pyaccel as _pyaccel
import mathphys as _mp
from . import optics_mode_C01 as _optics_mode_C01

_default_optics_mode = _optics_mode_C01
_lattice_symmetry = 10
_harmonic_number  = 864
_energy = 3e9 #[eV]

def create_lattice():
    # -- selection of optics mode --
    global _default_optics_mode
    _default_optics_mode = _optics_mode_C01

    # -- shortcut symbols --
    marker = _pyaccel.elements.marker
    drift = _pyaccel.elements.drift
    quadrupole = _pyaccel.elements.quadrupole
    sextupole = _pyaccel.elements.sextupole
    rbend_sirius = _pyaccel.elements.rbend
    rfcavity = _pyaccel.elements.rfcavity
    strengths = _default_optics_mode.strengths

    # -- drifts --
    LIA  = drift('lia2', 1.6179)
    LIB  = drift('lib2', 1.1879)
    L035 = drift('l035', 0.0350)
    L050 = drift('l050', 0.0500)
    L066 = drift('l066', 0.0660)
    L074 = drift('l074', 0.0740)
    L077 = drift('l077', 0.0770)
    L083 = drift('l083', 0.0830)
    L085 = drift('l085', 0.0850)
    L100 = drift('l100', 0.1000)
    L105 = drift('l105', 0.1050)
    L112 = drift('l112', 0.1120)
    L116 = drift('l116', 0.1160)
    L118 = drift('l118', 0.1180)
    L124 = drift('l124', 0.1240)
    L125 = drift('l125', 0.1250)
    L127 = drift('l127', 0.1270)
    L133 = drift('l133', 0.1330)
    L135 = drift('l135', 0.1350)
    L140 = drift('l140', 0.1400)
    L150 = drift('l150', 0.1500)
    L155 = drift('l155', 0.1550)
    L170 = drift('l170', 0.1700)
    L180 = drift('l180', 0.1800)
    L185 = drift('l185', 0.1850)
    L200 = drift('l200', 0.2000)
    L230 = drift('l230', 0.2300)
    L240 = drift('l240', 0.2400)
    L229 = drift('l229', 0.2290)
    L275 = drift('l275', 0.2750)
    L260 = drift('l260', 0.2600)
    L304 = drift('l304', 0.3040)
    L340 = drift('l340', 0.3400)
    L460 = drift('l460', 0.4600)
    L488 = drift('l488', 0.4880)
    L500 = drift('l500', 0.5000)
    L533 = drift('l533', 0.5330)
    L608 = drift('l608', 0.6080)
    L610 = drift('l610', 0.6100)
    L776 = drift('l776', 0.7760)
    L788 = drift('l788', 0.7880)
    L800 = drift('l800', 0.8000)
    L888 = drift('l888', 0.8880)
    LKK  = drift('lkk',  2.0250)
    LPMU = drift('lpmu', 0.3070)
    LPMD = drift('lpmd', 0.2859)

    # -- lattice markers --
    START    = marker('start')          # start of the model
    END      = marker('end')            # end of the model
    MIA      = marker('mia')            # center of long straight sections (even-numbered)
    MIB      = marker('mib')            # center of short straight sections (odd-numbered)
    GIRDER   = marker('girder')         # marker used to delimit girders. one marker at begin and another at end of girder
    MIDA     = marker('id_enda')        # marker for the extremities of IDs in long straight sections
    MIDB     = marker('id_endb')        # marker for the extremities of IDs in short straight sections
    MOMACCEP = marker('calc_mom_accep') # marker to define points where momentum acceptance will be calculated
    SEPT_IN  = marker('eseptinf')       # end of thin injection septum

    # -- dipoles --
    deg2rad = _math.pi/180.0

    B1E = rbend_sirius('b1', 0.828/2,  2.7553*deg2rad/2, 1.4143*deg2rad/2, 0,   0, 0, 0, [0, 0, 0], [0, -0.78, 0])
    MB1 = marker('mb1')
    B1S = rbend_sirius('b1', 0.828/2,  2.7553*deg2rad/2, 0, 1.4143*deg2rad/2,   0, 0, 0, [0, 0, 0], [0, -0.78, 0])
    B1  = [MOMACCEP,B1E,MOMACCEP,MB1,B1S,MOMACCEP]

    B2E = rbend_sirius('b2', 1.231/3, 4.0964*deg2rad/3, 1.4143*deg2rad/2, 0,   0, 0, 0, [0, 0, 0], [0, -0.78, 0])
    B2M = rbend_sirius('b2', 1.231/3, 4.0964*deg2rad/3, 0, 0,   0, 0, 0, [0, 0, 0], [0, -0.78, 0])
    B2S = rbend_sirius('b2', 1.231/3, 4.0964*deg2rad/3, 0, 1.4143*deg2rad/2,   0, 0, 0, [0, 0, 0], [0, -0.78, 0])
    B2  = [MOMACCEP,B2E,MOMACCEP,B2M,MOMACCEP,B2S,MOMACCEP]

    B3E = rbend_sirius('b3', 0.425/2, 1.4143*deg2rad/2, 1.4143*deg2rad/2, 0,   0, 0, 0, [0, 0, 0], [0, -0.78, 0])
    MB3 = marker('mb3')
    B3S = rbend_sirius('b3', 0.425/2, 1.4143*deg2rad/2, 0, 1.4143*deg2rad/2,   0, 0, 0, [0, 0, 0], [0, -0.78, 0])
    B3  = [MOMACCEP,B3E,MOMACCEP,MB3,B3S,MOMACCEP]

    BC1  = rbend_sirius('bc_hf', 0.015, 0.2800*deg2rad, 0, 0, 0, 0, 0, [0,0,0], [0,-0.005,0])
    BC2  = rbend_sirius('bc_hf', 0.005, 0.0900*deg2rad, 0, 0, 0, 0, 0, [0,0,0], [0,-0.057,0])
    BC3  = rbend_sirius('bc_hf', 0.005, 0.0780*deg2rad, 0, 0, 0, 0, 0, [0,0,0], [0,-0.112,0])
    BC4  = rbend_sirius('bc_hf', 0.005, 0.0590*deg2rad, 0, 0, 0, 0, 0, [0,0,0], [0,-0.103,0])
    BC5  = rbend_sirius('bc_hf', 0.010, 0.0850*deg2rad, 0, 0, 0, 0, 0, [0,0,0], [0,-0.066,0])
    BC6  = rbend_sirius('bc_hf', 0.010, 0.0590*deg2rad, 0, 0, 0, 0, 0, [0,0,0], [0,-0.047,0])
    BC7  = rbend_sirius('bc_hf', 0.015, 0.0640*deg2rad, 0, 0, 0, 0, 0, [0,0,0], [0,-0.080,0])
    BC8  = rbend_sirius('bc_lf', 0.020, 0.0720*deg2rad, 0, 0, 0, 0, 0, [0,0,0], [0,-0.388,0])
    BC9  = rbend_sirius('bc_lf', 0.325/2, 1.2700/2*deg2rad, 0, 0, 0, 0, 0, [0,0,0], [0,-0.891,0])
    BC10 = rbend_sirius('bc_lf', 0.325/2, 1.2700/2*deg2rad, 0, 0, 0, 0, 0, [0,0,0], [0,-0.891,0])
    BC11 = rbend_sirius('bc_lf', 0.010, 0.0310*deg2rad, 0, 0, 0, 0, 0, [0,0,0], [0,-0.689,0])
    BC12 = rbend_sirius('bc_lf', 0.010, 0.0220*deg2rad, 0, 0, 0, 0, 0, [0,0,0], [0,-0.325,0])
    BC13 = rbend_sirius('bc_lf', 0.010, 0.0150*deg2rad, 0, 0, 0, 0, 0, [0,0,0], [0,-0.128,0])
    BC14 = rbend_sirius('bc_lf', 0.020, 0.0233*deg2rad, 0, 0, 0, 0, 0, [0,0,0], [0, 0.009,0])

    MC = marker('mc')
    BCE = [BC14, BC13, BC12, BC11, MOMACCEP, BC10, MOMACCEP, BC9, \
            MOMACCEP, BC8, BC7, BC6, BC5, BC4, BC3, BC2, BC1]
    BCS = [BC1, BC2, BC3, BC4, BC5, BC6, BC7, BC8, MOMACCEP,\
            BC9, MOMACCEP, BC10, MOMACCEP, BC11, BC12, BC13, BC14]
    BC  = [BCE,MC, MOMACCEP,BCS]

    # -- quadrupoles --
    QFA  = quadrupole('qfa',  0.200, strengths['qfa'])
    QDA  = quadrupole('qda',  0.140, strengths['qda'])
    QDB2 = quadrupole('qdb2', 0.140, strengths['qdb2'])
    QFB  = quadrupole('qfb',  0.300, strengths['qfb'])
    QDB1 = quadrupole('qdb1', 0.140, strengths['qdb1'])
    QF1  = quadrupole('qf1',  0.200, strengths['qf1'])
    QF2  = quadrupole('qf2',  0.200, strengths['qf2'])
    QF3  = quadrupole('qf3',  0.200, strengths['qf3'])
    QF4  = quadrupole('qf4',  0.200, strengths['qf4'])

    # -- sextupoles and slow correctors --
    SDA  = sextupole('sda', 0.150, strengths['sda'])   #
    SFA  = sextupole('sfa', 0.150, strengths['sfa'])   # chs/cvs
    SDB  = sextupole('sdb', 0.150, strengths['sdb'])   #
    SFB  = sextupole('sfb', 0.150, strengths['sfb'])   # chs/cvs
    SD1J = sextupole('sd1j', 0.150, strengths['sd1j']) # chs/cvs
    SF1J = sextupole('sf1j', 0.150, strengths['sf1j']) #
    SD2J = sextupole('sd2j', 0.150, strengths['sd2j']) # chs
    SD3J = sextupole('sd3j', 0.150, strengths['sd3j']) # cvs
    SF2J = sextupole('sf2j', 0.150, strengths['sf2j']) # chs
    SD1K = sextupole('sd1k', 0.150, strengths['sd1k']) # chs/cvs
    SF1K = sextupole('sf1k', 0.150, strengths['sf1k']) #
    SD2K = sextupole('sd2k', 0.150, strengths['sd2k']) # chs
    SD3K = sextupole('sd3k', 0.150, strengths['sd3k']) # cvs
    SF2K = sextupole('sf2k', 0.150, strengths['sf2k']) # chs

    # -- slow vertical corrector --
    CV = sextupole('cv', 0.150, 0.0)

    # -- pulsed magnets --

    KICKIN = sextupole('kick_in', 0.5, S=0.0) # injection kicker
    PMM    = sextupole('pmm',     0.5, S=0.0) # pulsed multipole magnet

    # -- bpms and fast correctors --

    BPM    = marker('bpm')
    CF     = sextupole('cf', 0.100, S=0.0)
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

    M2A = [GIR,BPM,RBPM,L135,SFA,L150,QFA,L074,CF,L066,SDA,L150,QDA,GIR,L170,GIR]                      # high beta xxM2 girder
    M1A = M2A[::-1]                                                                                    # high beta xxM1 girder
    IDA = [L500,LIA,L500,MIDA,L500,L500,MIA,L500,L500,MIDA,L500,LIA,L500]                              # high beta ID straight section
    CAV = [L500,LIA,L500,L500,L500,MIA,RFC,L500,L500,L500,LIA,L500]                                    # high beta RF cavity straight section
    INJ = [L500,LIA,L500,L200,SEPTIN,L800,END,START,MIA, LKK, KICKIN, LPMU, PMM, LPMD]                 # high beta INJ straight section
    M1B = [GIR,L170,GIR,QDB1,L150,SDB,L240,QFB,L150,SFB,L050,CF,L035,QDB2,L140,BPM,RBPM,GIR]           # low beta xxM1 girder
    M2B = M1B[::-1]                                                                                    # low beta xxM2 girder
    IDB = [L500,LIB,L500,MIDB,L500,L500,MIB,L500,L500,MIDB,L500,LIB,L500]                              # low beta ID straight section
    C1A = [GIR,L610,GIR,SD1J,L170,QF1,L135,BPM,L125,SF1J,L230,QF2,L170,SD2J,GIR,L155,GIR,BPM,L185]     # arc sector in between B1-B2 (high beta odd-numbered straight sections)
    C2A = [GIR,L460,GIR,SD3J,L170,QF3,L230,SF2J,L260,QF4,GIR,L533,GIR,CV,L105,BPM,RBPM,L100]           # arc sector in between B2-BC (high beta odd-numbered straight sections)
    C3A = [GIR,L776,GIR,BPM,RBPM,L112,QF4,L083,CF,L077,SF2K,L230,QF3,L170,SD3K,GIR,L275,GIR,BPM,L185]  # arc sector in between BC-B2 (high beta odd-numbered straight sections)
    C4A = [GIR,L340,GIR,SD2K,L170,QF2,L230,SF1K,L125,BPM,L135,QF1,L170,SD1K,GIR,L610,GIR]              # arc sector in between B2-B1 (high beta odd-numbered straight sections)
    C1B = [GIR,L610,GIR,SD1K,L170,QF1,L135, BPM,L125,SF1K,L230,QF2,L170,SD2K,GIR,L155,GIR,BPM,L185]    # arc sector in between B1-B2 (low beta even-numbered straight sections)
    C2B = [GIR,L460,GIR,SD3K,L170,QF3,L230,SF2K,L260,QF4,GIR,L533,GIR,CV,L105,BPM,RBPM,L100]           # arc sector in between B2-BC (low beta even-numbered straight sections)
    C3B = [GIR,L776,GIR,BPM,RBPM,L112,QF4,L083,CF,L077,SF2J,L230,QF3,L170,SD3J,GIR,L275,GIR,BPM,L185]  # arc sector in between BC-B2 (low beta even-numbered straight sections)
    C4B = [GIR,L340,GIR,SD2J,L170,QF2,L230,SF1J,L125,BPM,L135,QF1,L170,SD1J,GIR,L610,GIR]              # arc sector in between B2-B1 (low beta even-numbered straight sections)

    C2A_DCCT = [GIR,L460,GIR,SD3J,L170,QF3,L230,SF2J,L260,QF4,GIR,L304,DCCT1,L229,GIR,CV,L105,BPM,RBPM,L100]  # arc sector in between B2-BC with DCCT1 (high beta odd-numbered straight sections)
    C2B_DCCT = [GIR,L460,GIR,SD3K,L170,QF3,L230,SF2K,L260,QF4,GIR,L304,DCCT2,L229,GIR,CV,L105,BPM,RBPM,L100]  # arc sector in between B2-BC with DCCT2 (low beta even-numbered straight sections)

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

    # -- remove girder
    anel = set_girders(anel)

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
        elif the_ring[i].polynom_b[1] or the_ring[i].fam_name in ['cf','kick_in']:
            nr_steps = int(_math.ceil(the_ring[i].length/len_quads))
            #if the_ring[i].fam_name == 'kick_in':
            #    print(nr_steps)
            the_ring[i].nr_steps = nr_steps



def set_vacuum_chamber(the_ring):

    # vchamber = [hmin, hmax, vmin, vmax] (meter)
    bc_chamber     = [-0.012, 0.012, -0.00450, 0.00450]
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

def set_girders(the_ring):
    the_ring = _mp.utils.flatten(the_ring)
    new_ring = []
    for elem in the_ring:
        if elem.fam_name != 'girder':
            new_ring.append(elem)
    return new_ring
