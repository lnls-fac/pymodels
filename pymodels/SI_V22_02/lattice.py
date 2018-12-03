"""Lattice module.

In this module the lattice of the corresponding accelerator is defined.
"""

import math as _math
import lnls as _lnls
import pyaccel as _pyaccel
import mathphys as _mp
from . import segmented_models as _segmented_models

default_optics_mode = 'S05.01'
lattice_symmetry = 5
harmonic_number = 864
energy = 3e9  # [eV]


def create_lattice(mode=default_optics_mode, simplified=False):
    """Return lattice object."""
    # -- selection of optics mode --
    strengths = get_optics_mode(mode=mode)

    # -- shortcut symbols --
    marker = _pyaccel.elements.marker
    drift = _pyaccel.elements.drift
    sextupole = _pyaccel.elements.sextupole
    rfcavity = _pyaccel.elements.rfcavity

    # -- drifts --
    LKK = drift('lkk', 1.9150)
    LPMU = drift('lpmu', 0.0600)
    LPMD = drift('lpmd', 0.4929)
    LIA = drift('lia', 1.5179)
    LIB = drift('lib', 1.0879)
    LIP = drift('lip', 1.0879)

    L011 = drift('l011', 0.011)
    L041 = drift('l041', 0.041)
    L044 = drift('l044', 0.044)
    L048 = drift('l048', 0.048)
    L066 = drift('l066', 0.066)
    L074 = drift('l074', 0.074)
    L075 = drift('l075', 0.075)
    L081 = drift('l081', 0.081)
    L082 = drift('l082', 0.082)
    L100 = drift('l100', 0.100)
    L110 = drift('l110', 0.110)
    L112 = drift('l112', 0.112)
    L120 = drift('l120', 0.120)
    L125 = drift('l125', 0.125)
    L127 = drift('l127', 0.127)
    L133 = drift('l133', 0.133)
    L134 = drift('l134', 0.134)
    L135 = drift('l135', 0.135)
    L140 = drift('l140', 0.140)
    L150 = drift('l150', 0.150)
    L170 = drift('l170', 0.170)
    L192 = drift('l192', 0.192)
    L200 = drift('l200', 0.200)
    L205 = drift('l205', 0.205)
    L216 = drift('l216', 0.216)
    L230 = drift('l230', 0.230)
    L237 = drift('l237', 0.237)
    L240 = drift('l240', 0.240)
    L260 = drift('l260', 0.260)
    L325 = drift('l325', 0.325)
    L336 = drift('l336', 0.336)
    L419 = drift('l419', 0.419)
    L474 = drift('l474', 0.474)
    L500 = drift('l500', 0.500)
    L715 = drift('l715', 0.715)

    # -- lattice markers --
    m_accep_fam_name = 'calc_mom_accep'

    # -- dipoles --
    BC = _segmented_models.dipole_bc(m_accep_fam_name, simplified)
    B1 = _segmented_models.dipole_b1(m_accep_fam_name, simplified)
    B2 = _segmented_models.dipole_b2(m_accep_fam_name, simplified)

    # -- quadrupoles --
    QFA = _segmented_models.quadrupole_q20('QFA', strengths['QFA'], simplified)
    QDA = _segmented_models.quadrupole_q14('QDA', strengths['QDA'], simplified)
    QDB2 = _segmented_models.quadrupole_q14('QDB2', strengths['QDB2'],
                                            simplified)
    QFB = _segmented_models.quadrupole_q30('QFB', strengths['QFB'], simplified)
    QDB1 = _segmented_models.quadrupole_q14('QDB1', strengths['QDB1'],
                                            simplified)
    QDP2 = _segmented_models.quadrupole_q14('QDP2', strengths['QDP2'],
                                            simplified)
    QFP = _segmented_models.quadrupole_q30('QFP', strengths['QFP'], simplified)
    QDP1 = _segmented_models.quadrupole_q14('QDP1', strengths['QDP1'],
                                            simplified)
    Q1 = _segmented_models.quadrupole_q20('Q1',   strengths['Q1'], simplified)
    Q2 = _segmented_models.quadrupole_q20('Q2',   strengths['Q2'], simplified)
    Q3 = _segmented_models.quadrupole_q20('Q3',   strengths['Q3'], simplified)
    Q4 = _segmented_models.quadrupole_q20('Q4',   strengths['Q4'], simplified)

    # -- sextupoles --
    SDA0 = sextupole('SDA0', 0.150, strengths['SDA0'])  # CH-CV
    SDB0 = sextupole('SDB0', 0.150, strengths['SDB0'])  # CH-CV
    SDP0 = sextupole('SDP0', 0.150, strengths['SDP0'])  # CH-CV
    SDA1 = sextupole('SDA1', 0.150, strengths['SDA1'])  # QS
    SDB1 = sextupole('SDB1', 0.150, strengths['SDB1'])  # QS
    SDP1 = sextupole('SDP1', 0.150, strengths['SDP1'])  # QS
    SDA2 = sextupole('SDA2', 0.150, strengths['SDA2'])  # CH-CV
    SDB2 = sextupole('SDB2', 0.150, strengths['SDB2'])  # CH-CV
    SDP2 = sextupole('SDP2', 0.150, strengths['SDP2'])  # CH-CV
    SDA3 = sextupole('SDA3', 0.150, strengths['SDA3'])  # --
    SDB3 = sextupole('SDB3', 0.150, strengths['SDB3'])  # --
    SDP3 = sextupole('SDP3', 0.150, strengths['SDP3'])  # --
    SFA0 = sextupole('SFA0', 0.150, strengths['SFA0'])  # CV
    SFB0 = sextupole('SFB0', 0.150, strengths['SFB0'])  # CV
    SFP0 = sextupole('SFP0', 0.150, strengths['SFP0'])  # CV
    SFA1 = sextupole('SFA1', 0.150, strengths['SFA1'])  # QS
    SFB1 = sextupole('SFB1', 0.150, strengths['SFB1'])  # QS
    SFP1 = sextupole('SFP1', 0.150, strengths['SFP1'])  # QS
    SFA2 = sextupole('SFA2', 0.150, strengths['SFA2'])  # CH
    SFB2 = sextupole('SFB2', 0.150, strengths['SFB2'])  # CH-CV
    SFP2 = sextupole('SFP2', 0.150, strengths['SFP2'])  # CH-CV

    # -- slow vertical corrector --
    CV = sextupole('CV', 0.150, 0.0)

    # -- pulsed magnets --
    InjDpKckr = sextupole('InjDpKckr', 0.400, S=0.0)  # injection kicker
    InjNLKckr = sextupole('InjNLKckr', 0.450, S=0.0)  # pulsed multipole magnet
    PingV = marker('PingV')  # Vertical Pinger

    # -- fast correctors --
    FC = sextupole('FC', 0.100, S=0.0)
    # uses fast corrector magnet with skew quad coil:
    FCQ = sextupole('FCQ', 0.100, S=0.0)

    # -- rf cavities --
    RFC = rfcavity('SRFCav', 0, 3.0e6, 500e6)

    # -- lattice markers --
    START = marker('start')  # start of the model
    END = marker('end')  # end of the model
    MIA = marker('mia')  # center of long straight sections (even-numbered)
    MIB = marker('mib')  # center of short straight sections (odd-numbered)
    MIP = marker('mip')  # center of short straight sections (odd-numbered)
    # marker used to delimitate girders.
    # one marker at begin and another at end of girder:
    GIR = marker('girder')
    # marker for the extremities of IDs in long straight sections
    MIDA = marker('id_enda')
    # marker for the extremities of IDs in short straight sections
    MIDB = marker('id_endb')
    # marker for the extremities of IDs in short straight sections
    MIDP = marker('id_endp')
    # end of injection septum
    InjSeptF = marker('InjSeptF')

    # --- Diagnostic Components ---
    BPM = marker('BPM')
    DCCT = marker('DCCT')    # dcct to measure beam current
    ScrapH = marker('ScrapH')  # horizontal scraper
    ScrapV = marker('ScrapV')  # vertical scraper
    GSL15 = marker('GSL15')   # Generic Stripline (lambda/4)
    GSL07 = marker('GSL07')   # Generic Stripline (lambda/8)
    BPME = marker('BPME')    # Extra BPM
    BbBPkup = marker('BbBPkup')    # Bunch-by-Bunch Pickup
    BbBKckrH = marker('BbBKckrH')   # Horizontal Bunch-by-Bunch Shaker
    BbBKckrV = marker('BbBKckrV')   # Vertical Bunch-by-Bunch Shaker
    TuneShkrH = marker('TuneShkrH')  # Horizontal Tune Shaker
    TunePkupH = marker('TunePkupH')  # Horizontal Tune Pickup
    TuneShkrV = marker('TuneShkrV')  # Vertical Tune Shaker
    TunePkupV = marker('TunePkupV')  # Vertical Tune Pickup

    # -- transport lines --
    M1A = [
        GIR, L134, GIR, QDA, L150, SDA0, L066, FC, L074, QFA, L150, SFA0,
        L135, BPM, GIR]  # high beta xxM1 girder (with fasc corrector)
    M1B = [
        GIR, L134, GIR, QDB1, L150, SDB0, L240, QFB, L150, SFB0, L041, FC,
        L044, QDB2, L140, BPM, GIR]  # low beta xxM1 girder
    M1P = [
        GIR, L134, GIR, QDP1, L150, SDP0, L240, QFP, L150, SFP0, L041, FC,
        L044, QDP2, L140, BPM, GIR]  # low beta xxM1 girder
    M2A = M1A[::-1]  # high beta xxM2 girder (with fast correctors)
    M2B = M1B[::-1]  # low beta xxM2 girder
    M2P = M1P[::-1]  # low beta xxM2 girder

    # low beta xxM1 girder for straight section 12 (with BbBPkup)
    M1B_BbBPkup = [
        GIR, L134, GIR, QDB1, L150, SDB0, L120, BbBPkup, L120,
        QFB, L150, SFB0, L041, FC, L044, QDB2, L140, BPM, GIR]

    IDA = [
        L500, LIA, L500, MIDA, L500, L500, MIA, L500, L500, MIDA, L500,
        LIA, L500]  # high beta ID straight section
    IDA_INJ = [
        L500, TuneShkrH, LIA, L419, InjSeptF, L081, L500, L500, END, START,
        MIA, LKK, InjDpKckr, LPMU, ScrapH, L100, ScrapV, L100, InjNLKckr,
        LPMD]  # high beta INJ straight section and Scrapers
    IDA_BbBKckrH = [
        L500, BbBKckrH, LIA, L500, MIDA, L500, L500, MIA, L500, L500,
        MIDA, L500, LIA, L500]  # high beta ID straight section
    IDA_TunePkupH = [
        L500, TunePkupH, LIA, L500, MIDA, L500, L500, MIA, L500, L500,
        MIDA, L500, LIA, L500]  # high beta ID straight section

    IDB = [
        L500, LIB, L500, MIDB, L500, L500, MIB, L500, L500, MIDB, L500,
        LIB, L500]  # low beta ID straight section
    IDB_GSL07 = [
        L500, GSL07, LIB, L500, MIDB, L500, L500, MIB, L500, L500,
        MIDB, L500, LIB, L500]  # low beta ID straight section

    IDP = [
        L500, LIP, L500, MIDP, L500, L500, MIP, L500, L500, MIDP, L500,
        LIP, L500]  # low beta ID straight section
    IDP_CAV = [
        L500, LIP, L500, L500, L500, MIP, RFC, L500, L500, L500, LIP,
        L500]  # low beta RF cavity straight section
    IDP_GSL15 = [
        L500, GSL15, LIP, L500, MIDP, L500, L500, MIP, L500, L500,
        MIDP, L500, LIP, L500]  # low beta ID straight section

    # arc sector in between B1-B2 (high beta odd-numbered straight sections)
    C1A = [
        GIR, L474, GIR, SDA1, L170, Q1, L135, BPM, L125, SFA1, L230, Q2,
        L170, SDA2, GIR, L205, GIR, BPM, L011]
    # arc sector in between B1-B2 (low beta even-numbered straight sections)
    C1B = [
        GIR, L474, GIR, SDB1, L170, Q1, L135, BPM, L125, SFB1, L230, Q2,
        L170, SDB2, GIR, L205, GIR, BPM, L011]
    # arc sector in between B1-B2 (low beta even-numbered straight sections)
    C1P = [
        GIR, L474, GIR, SDP1, L170, Q1, L135, BPM, L125, SFP1, L230, Q2,
        L170, SDP2, GIR, L205, GIR, BPM, L011]
    # arc sector in between B2-BC (high beta odd-numbered straight sections)
    C2A = [
        GIR, L336, GIR, SDA3, L170, Q3, L230, SFA2, L260, Q4, L200, CV,
        GIR, L192, GIR, FCQ, L110, BPM, L075]
    # arc sector in between B2-BC (low beta even-numbered straight sections)
    C2B = [
        GIR, L336, GIR, SDB3, L170, Q3, L230, SFB2, L260, Q4, L200, CV,
        GIR, L192, GIR, FCQ, L110, BPM, L075]
    # arc sector in between B2-BC (low beta even-numbered straight sections)
    C2P = [
        GIR, L336, GIR, SDP3, L170, Q3, L230, SFP2, L260, Q4, L200, CV,
        GIR, L192, GIR, FCQ, L110, BPM, L075]
    # arc sector in between BC-B2 (high beta odd-numbered straight sections)
    C3A = [
        GIR, L715, GIR, L112, Q4, L133, BPM, L127, SFA2, L048, FC, L082,
        Q3, L170, SDA3, GIR, L325, GIR, BPM, L011]
    # arc sector in between BC-B2 (low beta even-numbered straight sections)
    C3B = [
        GIR, L715, GIR, L112, Q4, L133, BPM, L127, SFB2, L048, FC, L082,
        Q3, L170, SDB3, GIR, L325, GIR, BPM, L011]
    # arc sector in between BC-B2 (low beta even-numbered straight sections)
    C3P = [
        GIR, L715, GIR, L112, Q4, L133, BPM, L127, SFP2, L048, FC, L082,
        Q3, L170, SDP3, GIR, L325, GIR, BPM, L011]
    # arc sector in between B2-B1 (high beta odd-numbered straight sections)
    C4A = [
        GIR, L216, GIR, SDA2, L170, Q2, L230, SFA1, L125, BPM, L135, Q1,
        L170, SDA1, GIR, L474, GIR]
    # arc sector in between B2-B1 (high beta odd-numbered straight sections)
    C4A_BbBKckrV = [
        GIR, L216, GIR, SDA2, L170, Q2, L230, SFA1, L125, BPM, L135,
        Q1, L170, SDA1, L237, BbBKckrV, GIR, L237, GIR]
    # arc sector in between B2-B1 (high beta odd-numbered straight sections)
    C4A_BPME = [
        GIR, L216, GIR, SDA2, L170, Q2, L230, SFA1, L125, BPM, L135,
        Q1, L170, SDA1, L237, BPME, GIR, L237, GIR]
    # arc sector in between B2-B1 (low beta even-numbered straight sections)
    C4B = [
        GIR, L216, GIR, SDB2, L170, Q2, L230, SFB1, L125, BPM, L135, Q1,
        L170, SDB1, GIR, L474, GIR]
    # arc sector in between B2-B1 (low beta even-numbered straight sections)
    C4B_DCCT = [
        GIR, L216, GIR, SDB2, L170, Q2, L230, SFB1, L125, BPM, L135,
        Q1, L170, SDB1, L237, DCCT, GIR, L237, GIR]
    # arc sector in between B2-B1 (low beta even-numbered straight sections)
    C4B_TunePkupV = [
        GIR, L216, GIR, SDB2, L170, Q2, L230, SFB1, L125, BPM, L135,
        Q1, L170, SDB1, L237, TunePkupV, GIR, L237, GIR]
    # arc sector in between B2-B1 (low beta even-numbered straight sections)
    C4B_PingV = [
        GIR, L216, GIR, SDB2, L170, Q2, L230, SFB1, L125, BPM, L135,
        Q1, L170, SDB1, L237, PingV, GIR, L237, GIR]
    # arc sector in between B2-B1 (low beta even-numbered straight sections)
    C4P = [
        GIR, L216, GIR, SDP2, L170, Q2, L230, SFP1, L125, BPM, L135, Q1,
        L170, SDP1, GIR, L474, GIR]
    # arc sector in between B2-B1 (low beta even-numbered straight sections)
    C4P_DCCT = [
        GIR, L216, GIR, SDP2, L170, Q2, L230, SFP1, L125, BPM, L135,
        Q1, L170, SDP1, L237, DCCT, GIR, L237, GIR]
    # arc sector in between B2-B1 (low beta even-numbered straight sections)
    C4P_TuneShkrV = [
        GIR, L216, GIR, SDP2, L170, Q2, L230, SFP1, L125, BPM, L135,
        Q1, L170, SDP1, L237, TuneShkrV, GIR, L237, GIR]

    # -- girders --

    # straight sections
    SS_S01 = IDA_INJ
    SS_S02 = IDB
    SS_S03 = IDP_CAV
    SS_S04 = IDB
    SS_S05 = IDA
    SS_S06 = IDB
    SS_S07 = IDP
    SS_S08 = IDB
    SS_S09 = IDA
    SS_S10 = IDB
    SS_S11 = IDP
    SS_S12 = IDB
    SS_S13 = IDA_BbBKckrH
    SS_S14 = IDB
    SS_S15 = IDP
    SS_S16 = IDB
    SS_S17 = IDA_TunePkupH
    SS_S18 = IDB
    SS_S19 = IDP_GSL15
    SS_S20 = IDB_GSL07

    # down and upstream straight sections
    M1_S01 = M1A
    M2_S01 = M2A
    M1_S02 = M1B
    M2_S02 = M2B
    M1_S03 = M1P
    M2_S03 = M2P
    M1_S04 = M1B
    M2_S04 = M2B
    M1_S05 = M1A
    M2_S05 = M2A
    M1_S06 = M1B
    M2_S06 = M2B
    M1_S07 = M1P
    M2_S07 = M2P
    M1_S08 = M1B
    M2_S08 = M2B
    M1_S09 = M1A
    M2_S09 = M2A
    M1_S10 = M1B
    M2_S10 = M2B
    M1_S11 = M1P
    M2_S11 = M2P
    M1_S12 = M1B_BbBPkup
    M2_S12 = M2B
    M1_S13 = M1A
    M2_S13 = M2A
    M1_S14 = M1B
    M2_S14 = M2B
    M1_S15 = M1P
    M2_S15 = M2P
    M1_S16 = M1B
    M2_S16 = M2B
    M1_S17 = M1A
    M2_S17 = M2A
    M1_S18 = M1B
    M2_S18 = M2B
    M1_S19 = M1P
    M2_S19 = M2P
    M1_S20 = M1B
    M2_S20 = M2B

    # dispersive arcs
    C1_S01 = C1A
    C2_S01 = C2A
    C3_S01 = C3B
    C4_S01 = C4B
    C1_S02 = C1B
    C2_S02 = C2B
    C3_S02 = C3P
    C4_S02 = C4P
    C1_S03 = C1P
    C2_S03 = C2P
    C3_S03 = C3B
    C4_S03 = C4B
    C1_S04 = C1B
    C2_S04 = C2B
    C3_S04 = C3A
    C4_S04 = C4A
    C1_S05 = C1A
    C2_S05 = C2A
    C3_S05 = C3B
    C4_S05 = C4B
    C1_S06 = C1B
    C2_S06 = C2B
    C3_S06 = C3P
    C4_S06 = C4P
    C1_S07 = C1P
    C2_S07 = C2P
    C3_S07 = C3B
    C4_S07 = C4B
    C1_S08 = C1B
    C2_S08 = C2B
    C3_S08 = C3A
    C4_S08 = C4A
    C1_S09 = C1A
    C2_S09 = C2A
    C3_S09 = C3B
    C4_S09 = C4B
    C1_S10 = C1B
    C2_S10 = C2B
    C3_S10 = C3P
    C4_S10 = C4P
    C1_S11 = C1P
    C2_S11 = C2P
    C3_S11 = C3B
    C4_S11 = C4B
    C1_S12 = C1B
    C2_S12 = C2B
    C3_S12 = C3A
    C4_S12 = C4A_BbBKckrV
    C1_S13 = C1A
    C2_S13 = C2A
    C3_S13 = C3B
    C4_S13 = C4B_DCCT
    C1_S14 = C1B
    C2_S14 = C2B
    C3_S14 = C3P
    C4_S14 = C4P_DCCT
    C1_S15 = C1P
    C2_S15 = C2P
    C3_S15 = C3B
    C4_S15 = C4B
    C1_S16 = C1B
    C2_S16 = C2B
    C3_S16 = C3A
    C4_S16 = C4A_BPME
    C1_S17 = C1A
    C2_S17 = C2A
    C3_S17 = C3B
    C4_S17 = C4B_TunePkupV
    C1_S18 = C1B
    C2_S18 = C2B
    C3_S18 = C3P
    C4_S18 = C4P_TuneShkrV
    C1_S19 = C1P
    C2_S19 = C2P
    C3_S19 = C3B
    C4_S19 = C4B_PingV
    C1_S20 = C1B
    C2_S20 = C2B
    C3_S20 = C3A
    C4_S20 = C4A

    # SECTORS # 01..20
    S01 = [M1_S01, SS_S01, M2_S01, B1, C1_S01, B2, C2_S01, BC, C3_S01,
           B2, C4_S01, B1]
    S02 = [M1_S02, SS_S02, M2_S02, B1, C1_S02, B2, C2_S02, BC, C3_S02,
           B2, C4_S02, B1]
    S03 = [M1_S03, SS_S03, M2_S03, B1, C1_S03, B2, C2_S03, BC, C3_S03,
           B2, C4_S03, B1]
    S04 = [M1_S04, SS_S04, M2_S04, B1, C1_S04, B2, C2_S04, BC, C3_S04,
           B2, C4_S04, B1]
    S05 = [M1_S05, SS_S05, M2_S05, B1, C1_S05, B2, C2_S05, BC, C3_S05,
           B2, C4_S05, B1]
    S06 = [M1_S06, SS_S06, M2_S06, B1, C1_S06, B2, C2_S06, BC, C3_S06,
           B2, C4_S06, B1]
    S07 = [M1_S07, SS_S07, M2_S07, B1, C1_S07, B2, C2_S07, BC, C3_S07,
           B2, C4_S07, B1]
    S08 = [M1_S08, SS_S08, M2_S08, B1, C1_S08, B2, C2_S08, BC, C3_S08,
           B2, C4_S08, B1]
    S09 = [M1_S09, SS_S09, M2_S09, B1, C1_S09, B2, C2_S09, BC, C3_S09,
           B2, C4_S09, B1]
    S10 = [M1_S10, SS_S10, M2_S10, B1, C1_S10, B2, C2_S10, BC, C3_S10,
           B2, C4_S10, B1]
    S11 = [M1_S11, SS_S11, M2_S11, B1, C1_S11, B2, C2_S11, BC, C3_S11,
           B2, C4_S11, B1]
    S12 = [M1_S12, SS_S12, M2_S12, B1, C1_S12, B2, C2_S12, BC, C3_S12,
           B2, C4_S12, B1]
    S13 = [M1_S13, SS_S13, M2_S13, B1, C1_S13, B2, C2_S13, BC, C3_S13,
           B2, C4_S13, B1]
    S14 = [M1_S14, SS_S14, M2_S14, B1, C1_S14, B2, C2_S14, BC, C3_S14,
           B2, C4_S14, B1]
    S15 = [M1_S15, SS_S15, M2_S15, B1, C1_S15, B2, C2_S15, BC, C3_S15,
           B2, C4_S15, B1]
    S16 = [M1_S16, SS_S16, M2_S16, B1, C1_S16, B2, C2_S16, BC, C3_S16,
           B2, C4_S16, B1]
    S17 = [M1_S17, SS_S17, M2_S17, B1, C1_S17, B2, C2_S17, BC, C3_S17,
           B2, C4_S17, B1]
    S18 = [M1_S18, SS_S18, M2_S18, B1, C1_S18, B2, C2_S18, BC, C3_S18,
           B2, C4_S18, B1]
    S19 = [M1_S19, SS_S19, M2_S19, B1, C1_S19, B2, C2_S19, BC, C3_S19,
           B2, C4_S19, B1]
    S20 = [M1_S20, SS_S20, M2_S20, B1, C1_S20, B2, C2_S20, BC, C3_S20,
           B2, C4_S20, B1]

    anel = [S01, S02, S03, S04, S05, S06, S07, S08, S09, S10,
            S11, S12, S13, S14, S15, S16, S17, S18, S19, S20]
    anel = _lnls.utils.flatten(anel)

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
    """Set RF frequency of the lattice."""
    circumference = _pyaccel.lattice.length(the_ring)
    # _, beam_velocity, _, _, _ = _mp.beam_optics.beam_rigidity(energy=energy)
    # velocity = beam_velocity
    velocity = _mp.constants.light_speed
    rev_frequency = velocity / circumference
    rf_frequency = harmonic_number * rev_frequency
    idx = _pyaccel.lattice.find_indices(the_ring, 'fam_name', 'SRFCav')
    for i in idx:
        the_ring[i].frequency = rf_frequency


def set_num_integ_steps(the_ring):
    """Set number of integration steps in each lattice element."""
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
        elif the_ring[i].polynom_b[1] or the_ring[i].fam_name in \
                ['FC', 'FCQ', 'InjDpKckr', 'InjNLKckr']:
            nr_steps = int(_math.ceil(the_ring[i].length/len_quads))
            the_ring[i].nr_steps = nr_steps


def set_vacuum_chamber(the_ring, mode=default_optics_mode):
    """Set vacuum chamber for all elements."""
    # vchamber = [hmin, hmax, vmin, vmax] (meter)
    bc_vchamber = [-0.012, 0.012, -0.004, 0.004]
    other_vchamber = [-0.012, 0.012, -0.012, 0.012]
    idb_vchamber = [-0.004, 0.004, -0.00225, 0.00225]
    ida_vchamber = [-0.012, 0.012, -0.004, 0.004]
    if mode.startswith('S05'):
        idp_vchamber = idb_vchamber
    else:
        idp_vchamber = ida_vchamber
    inj_vchamber = [-0.030, 0.030, -0.012, 0.012]

    # Set ordinary Vacuum Chamber
    for i in range(len(the_ring)):
        e = the_ring[i]
        e.hmin, e.hmax, e.vmin, e.vmax = other_vchamber

    # Shift the ring to do not begin between id markers
    bpm = _pyaccel.lattice.find_indices(the_ring, 'fam_name', 'BPM')
    the_ring = _pyaccel.lattice.shift(the_ring, bpm[0])

    # Set bc vacuum chamber
    bcs = _pyaccel.lattice.find_indices(the_ring, 'fam_name', 'mc')
    for i in bcs:
        for j in range(i-8, i+9):
            e = the_ring[j]
            e.hmin, e.hmax, e.vmin, e.vmax = bc_vchamber

    # Set in-vacuum ids vacuum chamber
    idb = _pyaccel.lattice.find_indices(the_ring, 'fam_name', 'id_endb')
    idb_list = []
    [idb_list.extend(list(range(idb[2*i], idb[2*i+1]+1))) for i in
        range(len(idb)//2)]
    for i in idb_list:
        e = the_ring[i]
        e.hmin, e.hmax, e.vmin, e.vmax = idb_vchamber

    # Set other ids vacuum chamber
    ida = _pyaccel.lattice.find_indices(the_ring, 'fam_name', 'id_enda')
    ida_list = []
    [ida_list.extend(list(range(ida[2*i], ida[2*i+1]+1))) for i in
        range(len(ida)//2)]
    for i in ida_list:
        e = the_ring[i]
        e.hmin, e.hmax, e.vmin, e.vmax = ida_vchamber

    # Set other ids vacuum chamber
    idp = _pyaccel.lattice.find_indices(the_ring, 'fam_name', 'id_endp')
    idp_list = []
    [idp_list.extend(list(range(idp[2*i], idp[2*i+1]+1))) for i in
        range(len(idp)//2)]
    for i in idp_list:
        e = the_ring[i]
        e.hmin, e.hmax, e.vmin, e.vmax = idp_vchamber

    # Shift the ring back.
    the_ring = _pyaccel.lattice.shift(the_ring, len(the_ring)-bpm[0])

    # Set injection vacuum chamber
    sept_in = _pyaccel.lattice.find_indices(
                                    the_ring, 'fam_name', 'InjSeptF')[-1]
    kick_in = _pyaccel.lattice.find_indices(
                                    the_ring, 'fam_name', 'InjDpKckr')[0]
    inj_list = list(range(sept_in, len(the_ring))) + list(range(0, kick_in+1))
    for i in inj_list:
        e = the_ring[i]
        e.hmin, e.hmax, e.vmin, e.vmax = inj_vchamber


def get_optics_mode(mode=default_optics_mode):
    """Return magnet strengths fora given optics mode."""
    mode, version = mode.split('.')

    if mode == 'S05':
        if version == '01':
            # Version SI.V22.01-S05.01
            # ========================
            # The BPM upstream of dipole B2 was moved by 50mm (closer to B2)
            # to fit in the girder. Modification in sectors C1 and C3.
            # This change was requested by the Mechanical Design Group.
            # Optics asymmetries introduced by new B1 and B2 models in
            # previous version were corrected using MAD.
            strengths = {
                # Macthing done by Liu on MAD.
                #  QUADRUPOLOS
                #  ===========
                'QFA': +3.573152846456,
                'QFB': +4.114808227974,
                'QFP': +4.114808227974,
                'QDA': -1.621537177175,
                'QDB1': -2.00636151367,
                'QDB2': -3.416409380519,
                'QDP1': -2.00636151367,
                'QDP2': -3.416409380519,
                'Q1': +2.81580602167,
                'Q2': +4.342314688125,
                'Q3': +3.235627121213,
                'Q4': +3.933913571031,

                # same sextupoles as si.v14.c03
                #  SEXTUPOLOS
                #  ===========
                'SDA0': -80.833699999999993,
                'SDB0': -64.942200000000000,
                'SDP0': -64.942200000000000,
                'SFA0': +52.569600000000001,
                'SFB0': +73.740099999999998,
                'SFP0': +73.740099999999998,
                'SDA1': -162.9865,
                'SDA2': -88.8540,
                'SDA3': -139.9408,
                'SFA1':  191.8284,
                'SFA2':  150.7692,
                'SDB1': -141.6359,
                'SDB2': -122.2281,
                'SDB3': -173.8124,
                'SFB1':  227.8813,
                'SFB2':  197.8206,
                'SDP1': -142.3060,
                'SDP2': -122.2810,
                'SDP3': -174.1574,
                'SFP1':  229.2493,
                'SFP2':  198.5034,
            }
        else:
            raise _pyaccel.AcceleratorException('Version not Implemented')
    else:
        raise _pyaccel.AcceleratorException('Mode not Implemented.')

    return strengths
