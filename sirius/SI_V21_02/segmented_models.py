import math as _math
import numpy as _np
import pyaccel as _pyaccel

def dipole_bc(m_accep_fam_name):

    segtypes = {
        'bc_hf'   : ('bc_hf', _pyaccel.elements.rbend),
        'bc_lf'   : ('bc_lf', _pyaccel.elements.rbend),
        'bc_edge' : ('bc_edge', _pyaccel.elements.marker),
        'mc'      : ('mc', _pyaccel.elements.marker),
        'm_accep' : (m_accep_fam_name, _pyaccel.elements.marker),
    }

    # dipole model 2016-01-13
    # =======================
    # this (half) model is based on fieldmap
    # /home/fac_files/data/sirius/si/magnet_modelling/si-bc/bc-model8
    # '2016-01-12_Dipolo_Anel_BC_Modelo8_gap_lateral_2.9mm_peca_3.7mm_-90_12mm_-2000_2000mm.txt'
    monomials = [0,1,2,3,4,5,6,7,8,10]
    segmodel = [
        #type       len[m]    angle[deg]  PolyB(n=0)   PolyB(n=1)   PolyB(n=2)   PolyB(n=3)   PolyB(n=4)   PolyB(n=5)   PolyB(n=6)   PolyB(n=7)   PolyB(n=8)   PolyB(n=10)
        ['bc_hf',   0.005  ,  +0.09110 ,  +0.00e+00 ,  +3.82e-03 ,  -3.54e+01 ,  -3.99e+02 ,  -1.34e+05 ,  +5.52e+06 ,  -9.09e+09 ,  -2.68e+10 ,  +6.08e+13 ,  -2.20e+17],
        ['bc_hf',   0.005  ,  +0.08089 ,  +0.00e+00 ,  -2.31e-02 ,  -2.21e+01 ,  +8.72e+01 ,  -2.76e+05 ,  -1.30e+06 ,  -1.92e+09 ,  +9.20e+09 ,  +1.70e+13 ,  -1.05e+17],
        ['bc_hf',   0.005  ,  +0.06850 ,  +0.00e+00 ,  -2.20e-02 ,  -1.75e+01 ,  -3.23e+02 ,  +9.27e+04 ,  +6.39e+06 ,  -6.36e+09 ,  -3.56e+10 ,  +7.06e+13 ,  -2.92e+17],
        ['bc_hf',   0.005  ,  +0.05892 ,  +0.00e+00 ,  -2.66e-02 ,  -1.08e+01 ,  -5.20e+01 ,  +3.55e+04 ,  +1.33e+06 ,  -2.88e+09 ,  -7.47e+09 ,  +3.38e+13 ,  -1.43e+17],
        ['bc_hf',   0.010  ,  +0.09662 ,  +0.00e+00 ,  -2.65e-02 ,  -6.72e+00 ,  -3.36e-01 ,  -8.34e+03 ,  +3.02e+05 ,  -5.12e+08 ,  -2.04e+09 ,  +5.98e+12 ,  -2.47e+16],
        ['bc_hf',   0.010  ,  +0.07443 ,  +0.00e+00 ,  -2.58e-02 ,  -4.19e+00 ,  -3.35e+01 ,  -9.69e+03 ,  +7.03e+05 ,  -8.59e+06 ,  -3.71e+09 ,  +3.18e+11 ,  -1.93e+15],
        ['bc_hf',   0.010  ,  +0.05612 ,  +0.00e+00 ,  -2.56e-02 ,  -2.46e+00 ,  +2.77e+01 ,  -9.37e+02 ,  -3.93e+05 ,  -2.75e+06 ,  +2.18e+09 ,  -4.79e+11 ,  +3.31e+15],
        ['bc_hf',   0.010  ,  +0.04318 ,  +0.00e+00 ,  -1.73e-02 ,  -2.57e-01 ,  +5.38e+01 ,  -3.12e+04 ,  -8.40e+05 ,  +7.89e+08 ,  +4.23e+09 ,  -8.42e+12 ,  +3.14e+16],
        ['m_accep', 0,0,0,0,0,0,0,0,0,0,0,0],
        ['bc_lf',   0.064  ,  +0.21752 ,  +0.00e+00 ,  -7.09e-02 ,  +6.39e-02 ,  +3.43e+00 ,  +3.65e+02 ,  +2.55e+04 ,  -5.12e+06 ,  -3.70e+07 ,  -7.58e+10 ,  +6.63e+14],
        ['m_accep', 0,0,0,0,0,0,0,0,0,0,0,0],
        ['bc_lf',   0.160  ,  +0.62805 ,  +0.00e+00 ,  -9.25e-01 ,  +3.00e-01 ,  +1.79e+01 ,  +1.94e+03 ,  +3.37e+04 ,  -3.75e+07 ,  -1.15e+08 ,  +3.71e+11 ,  -1.29e+15],
        ['m_accep', 0,0,0,0,0,0,0,0,0,0,0,0],
        ['bc_lf',   0.160  ,  +0.62913 ,  +0.00e+00 ,  -9.36e-01 ,  +2.18e-02 ,  +1.57e+01 ,  -6.03e+02 ,  +1.76e+04 ,  +3.02e+07 ,  -4.16e+07 ,  -3.71e+11 ,  +1.57e+15],
        ['bc_lf',   0.012  ,  +0.03774 ,  +0.00e+00 ,  -4.86e-01 ,  -6.29e+00 ,  -1.72e+01 ,  +2.01e+04 ,  +1.96e+05 ,  -5.15e+08 ,  -1.10e+09 ,  +5.40e+12 ,  -1.96e+16],
        ['bc_edge', 0,0,0,0,0,0,0,0,0,0,0,0],
        ['bc_lf',   0.014  ,  +0.02843 ,  +0.00e+00 ,  -1.41e-01 ,  -4.21e+00 ,  -4.95e+01 ,  -7.83e+02 ,  +2.41e+04 ,  -9.98e+06 ,  +8.96e+07 ,  +2.20e+11 ,  -1.08e+15],
        ['bc_lf',   0.016  ,  +0.01811 ,  +0.00e+00 ,  -4.29e-02 ,  -2.02e+00 ,  -1.23e+01 ,  +1.33e+03 ,  +2.72e+03 ,  -4.91e+07 ,  -6.36e+07 ,  +5.63e+11 ,  -2.25e+15],
        ['bc_lf',   0.035  ,  +0.01956 ,  -3.56e-04*0, -8.49e-03 ,  -1.21e+00 ,  +2.30e+00 ,  +8.79e+02 ,  -2.03e+04 ,  -1.57e+07 ,  +4.30e+07 ,  +1.30e+11 ,  -4.24e+14],
    ]

    model = []

    # --- creates half model ---
    d2r = _math.pi/180.0
    PolyB = _np.zeros(1+max(monomials))
    for i in range(len(segmodel)):
        fam_name, element_type = segtypes[segmodel[i][0]]
        if element_type == _pyaccel.elements.rbend:
            for j in range(len(monomials)):
                PolyB[monomials[j]] = segmodel[i][j+3]
            PolyA = 0 * PolyB
            element = element_type(fam_name=fam_name, length=segmodel[i][1], angle=d2r * segmodel[i][2],
                         angle_in=0, angle_out=0,
                         gap=0, fint_in=0, fint_out=0,
                         polynom_a=PolyA, polynom_b=PolyB)
        else:
            element = element_type(fam_name)
        model.append(element)

    # --- adds additional markers ---
    mc     = segtypes['mc'][1](segtypes['mc'][0])
    maccep = segtypes['m_accep'][1](segtypes['m_accep'][0])
    model = model[::-1] + [mc,maccep] + model

    return model

def dipole_b1(m_accep_fam_name):

    segtypes = {
        'b1'      : ('b1', _pyaccel.elements.rbend),
        'b1_edge' : ('b1_edge', _pyaccel.elements.marker),
        'mb1'     : ('mb1', _pyaccel.elements.marker),
        'm_accep' : (m_accep_fam_name, _pyaccel.elements.marker),
    }

    # dipole model 2016-01-04
    # =======================
    # this (half) model is based on fieldmap
    # /home/fac_files/data/sirius/si/magnet_modelling/si-b1/b1-model2
    # '2015-11-19_Dipolo_Anel_B1_Modelo2_-32_15mm_-1000_1000mm.txt'

    monomials = [0,1,2,3,6]
    segmodel = [
        #type        len[m]    angle[deg]  PolyB(n=0)   PolyB(n=1)   PolyB(n=2)   PolyB(n=3)   PolyB(n=6)
        ['b1',       0.002  ,  +0.00621 ,  +0.00e+00 ,  -5.36e-01 ,  -6.82e+00 ,  +1.55e+01 ,  +1.39e+07],
        ['b1',       0.003  ,  +0.00935 ,  +0.00e+00 ,  -5.57e-01 ,  -6.27e+00 ,  +1.89e+01 ,  +1.22e+07],
        ['b1',       0.005  ,  +0.01580 ,  +0.00e+00 ,  -6.23e-01 ,  -4.47e+00 ,  +2.17e+01 ,  +7.91e+06],
        ['b1',       0.005  ,  +0.01609 ,  +0.00e+00 ,  -7.09e-01 ,  -1.96e+00 ,  +1.35e+01 ,  +4.05e+06],
        ['b1',       0.005  ,  +0.01629 ,  +0.00e+00 ,  -7.64e-01 ,  -4.46e-01 ,  +6.80e+00 ,  +2.71e+06],
        ['b1',       0.010  ,  +0.03280 ,  +0.00e+00 ,  -7.92e-01 ,  +1.69e-01 ,  +8.17e+00 ,  +2.06e+06],
        ['b1',       0.040  ,  +0.13116 ,  +0.00e+00 ,  -8.00e-01 ,  +2.64e-01 ,  +1.11e+01 ,  +2.08e+06],
        ['b1',       0.150  ,  +0.48795 ,  +0.00e+00 ,  -7.99e-01 ,  +2.91e-01 ,  +1.22e+01 ,  +2.34e+06],
        ['b1',       0.100  ,  +0.32489 ,  +0.00e+00 ,  -7.99e-01 ,  +3.01e-01 ,  +1.26e+01 ,  +2.37e+06],
        ['b1',       0.050  ,  +0.16324 ,  +0.00e+00 ,  -8.00e-01 ,  +2.52e-01 ,  +1.13e+01 ,  +2.21e+06],
        ['b1',       0.034  ,  +0.10495 ,  +0.00e+00 ,  -7.27e-01 ,  -1.67e+00 ,  +1.05e+01 ,  +4.45e+06],
        ['b1_edge',  0,0,0,0,0,0,0],
        ['b1',       0.016  ,  +0.02994 ,  +0.00e+00 ,  -2.28e-01 ,  -5.20e+00 ,  -1.95e+01 ,  +6.31e+06],
        ['b1',       0.040  ,  +0.02774 ,  +0.00e+00 ,  -3.65e-02 ,  -1.70e+00 ,  -1.12e+00 ,  +2.09e+04],
        ['b1',       0.040  ,  +0.00689 ,  +0.00e+00 ,  -2.47e-03 ,  -3.48e-01 ,  +6.84e-01 ,  +8.05e+04],
        ['b1',       0.050  ,  +0.00435 ,  -9.57e-06*0, +7.77e-04 ,  -8.91e-02 ,  +8.48e-02 ,  +3.92e+04],
        ['m_accep',  0,0,0,0,0,0,0],
    ]

    model = []

    # --- creates half model ---
    d2r = _math.pi/180.0
    PolyB = _np.zeros(1+max(monomials))
    for i in range(len(segmodel)):
        fam_name, element_type = segtypes[segmodel[i][0]]
        if element_type == _pyaccel.elements.rbend:
            for j in range(len(monomials)):
                PolyB[monomials[j]] = segmodel[i][j+3]
            PolyA = 0 * PolyB
            element = element_type(fam_name=fam_name, length=segmodel[i][1], angle=d2r * segmodel[i][2],
                         angle_in=0, angle_out=0,
                         gap=0, fint_in=0, fint_out=0,
                         polynom_a=PolyA, polynom_b=PolyB)
        else:
            element = element_type(fam_name)
        model.append(element)

    # --- adds additional markers ---
    mb1    = segtypes['mb1'][1](segtypes['mb1'][0])
    maccep = segtypes['m_accep'][1](segtypes['m_accep'][0])
    model = model[::-1] + [mb1,maccep] + model

    return model

def dipole_b2(m_accep_fam_name):

    segtypes = {
        'b2'      : ('b2', _pyaccel.elements.rbend),
        'b2_edge' : ('b2_edge', _pyaccel.elements.marker),
        'mb2'     : ('mb2', _pyaccel.elements.marker),
        'm_accep' : (m_accep_fam_name, _pyaccel.elements.marker),
    }

    # dipole model 2016-02-23
    # =======================
    # this (half) model is based on fieldmap
    # /home/fac_files/data/sirius/si/magnet_modelling/si-b2/b2-model3
    # '2015-12-01_Dipolo_Anel_B2_Modelo3_-63_17mm_-1500_1500mm.txt'
    # added one more segment to fieldmap model: so that it will be multiple of 3
    monomials = [0,1,2,3,6]
    segmodel = [
        #type        len[m]    angle[deg]  PolyB(n=0)   PolyB(n=1)   PolyB(n=2)   PolyB(n=3)   PolyB(n=6)
        ['b2',          0.125  ,  +0.40935 ,  +0.00e+00 ,  -8.00e-01 ,  +2.79e-01 ,  +1.18e+01 ,  +2.18e+06],
        ['b2',          0.055  ,  +0.18129 ,  +0.00e+00 ,  -7.99e-01 ,  +2.75e-01 ,  +1.09e+01 ,  +1.92e+06],
        ['b2',          0.010  ,  +0.03253 ,  +0.00e+00 ,  -7.55e-01 ,  -1.05e-01 ,  +1.30e+00 ,  +1.41e+06],
        ['b2',          0.005  ,  +0.01580 ,  +0.00e+00 ,  -6.49e-01 ,  -2.02e+00 ,  -3.88e+00 ,  +2.65e+06],
        ['b2',          0.005  ,  +0.01539 ,  +0.00e+00 ,  -5.52e-01 ,  -3.87e+00 ,  -1.14e+01 ,  +3.71e+06],
        ['b2',          0.005  ,  +0.01520 ,  +0.00e+00 ,  -5.05e-01 ,  -4.69e+00 ,  -1.85e+01 ,  +4.77e+06],
        ['m_accep',     0,0,0,0,0,0,0],
        ['b2',          0.005  ,  +0.01537 ,  +0.00e+00 ,  -5.46e-01 ,  -3.98e+00 ,  -1.14e+01 ,  +4.13e+06],
        ['b2',          0.010  ,  +0.03193 ,  +0.00e+00 ,  -6.85e-01 ,  -1.33e+00 ,  -2.74e+00 ,  +2.24e+06],
        ['b2',          0.010  ,  +0.03285 ,  +0.00e+00 ,  -7.84e-01 ,  +2.59e-01 ,  +5.69e+00 ,  +1.52e+06],
        ['b2',          0.175  ,  +0.57500 ,  +0.00e+00 ,  -7.99e-01 ,  +2.85e-01 ,  +1.20e+01 ,  +2.19e+06],
        ['b2_edge',     0,0,0,0,0,0,0],
        ['b2',          0.175  ,  +0.57546 ,  +0.00e+00 ,  -8.00e-01 ,  +2.79e-01 ,  +1.22e+01 ,  +2.23e+06],
        ['b2',          0.020  ,  +0.06320 ,  +0.00e+00 ,  -7.53e-01 ,  -5.68e-01 ,  +1.05e+00 ,  +2.38e+06],
        ['b2',          0.010  ,  +0.02489 ,  +0.00e+00 ,  -4.29e-01 ,  -3.77e+00 ,  -1.84e+01 ,  +2.64e+06],
        ['b2',          0.015  ,  +0.02434 ,  +0.00e+00 ,  -1.63e-01 ,  -3.23e+00 ,  -2.19e+01 ,  -1.16e+06],
        ['b2',          0.020  ,  +0.01685 ,  +0.00e+00 ,  -4.53e-02 ,  -1.77e+00 ,  -1.74e+00 ,  -1.02e+06],
        ['b2',          0.030  ,  +0.01055 ,  +0.00e+00 ,  -9.48e-03 ,  -7.41e-01 ,  +1.48e+00 ,  -4.57e+04],
        ['b2',          0.032  ,  +0.00415 ,  +0.00e+00 ,  -1.14e-03 ,  -2.29e-01 ,  +3.96e-01 ,  +5.05e+04],
        ['b2',          0.0325 ,  +0.00405 ,  +1.12e-04*0, +9.97e-04 ,  -1.16e-01 ,  +8.07e-02 ,  +3.53e+04],
        ['m_accep',     0,0,0,0,0,0,0],
    ]

    model = []

    # --- creates half model ---
    d2r = _math.pi/180.0
    PolyB = _np.zeros(1+max(monomials))
    for i in range(len(segmodel)):
        fam_name, element_type = segtypes[segmodel[i][0]]
        if element_type == _pyaccel.elements.rbend:
            for j in range(len(monomials)):
                PolyB[monomials[j]] = segmodel[i][j+3]
            PolyA = 0 * PolyB
            element = element_type(fam_name=fam_name, length=segmodel[i][1], angle=d2r * segmodel[i][2],
                         angle_in=0, angle_out=0,
                         gap=0, fint_in=0, fint_out=0,
                         polynom_a=PolyA, polynom_b=PolyB)
        else:
            element = element_type(fam_name)
        model.append(element)

    # --- adds additional markers ---
    mb2    = segtypes['mb2'][1](segtypes['mb2'][0])
    maccep = segtypes['m_accep'][1](segtypes['m_accep'][0])
    model = model[::-1] + [mb2,maccep] + model

    return model

def quadrupole_q14(fam_name, strength):

    segtypes = {
        fam_name      : (fam_name, _pyaccel.elements.quadrupole),
    }

    # Q14 model 2016-01-04
    # ====================
    # this (half) model is based on fieldmap
    # /home/fac_files/data/sirius/si/magnet_modelling/si-q14/model3/
    # '11-05-2015 Quadrupolo_Anel_Q14_Modelo 3_-14_14mm_-500_500mm.txt'
    monomials = [1,5,9,13]
    segmodel = [
        #type      len[m]     angle[deg]  PolyB(n=1)   PolyB(n=5)   PolyB(n=9)   PolyB(n=13)
        [fam_name, 0.070  ,  +0.00000 ,  -4.09e+00 ,  +5.37e+04 ,  -1.47e+13 ,  +2.91e+20],
    ];

    # rescale fieldmap data to strength argument
    quadidx = monomials.index(1)
    seg_lens = [segmodel[i][1] for i in range(len(segmodel))]
    model_length = 2 * sum(seg_lens)
    fmap_strength = [2*segmodel[i][3+quadidx]*seg_lens[i]/model_length for i in range(len(segmodel))]
    rescale = [strength / fmap_strength[i] for i in range(len(segmodel))]

    # --- hard-edge 1-segment model ---
    model = []
    i = 0
    fam_name, element_type = segtypes[segmodel[i][0]]
    PolyB = _np.zeros(1+max(monomials))
    for j in range(len(monomials)):
        PolyB[monomials[j]] = segmodel[i][j+3] * rescale[i]
    PolyA = 0 * PolyB
    element = element_type(fam_name=fam_name, length=2*segmodel[i][1], K=PolyB[1])
    element.polynom_a = PolyA
    element.polynom_b = PolyB
    model.append(element)

    return model

def quadrupole_q20(fam_name, strength):

    segtypes = {
        fam_name      : (fam_name, _pyaccel.elements.quadrupole),
    }

    # Q20 model 2016-01-04
    # ====================
    # this (half) model is based on fieldmap
    # /home/fac_files/data/sirius/si/magnet_modelling/si-q20/model4/
    # '11-05-2015 Quadrupolo_Anel_Q20_Modelo 4_-14_14mm_-500_500mm.txt'
    monomials = [1,5,9,13]
    segmodel = [
        #type      len[m]     angle[deg]  PolyB(n=1)   PolyB(n=5)   PolyB(n=9)   PolyB(n=13)
        [fam_name, 0.100  ,  +0.00000 ,  -4.80e+00 ,  +7.37e+04 ,  -1.87e+13 ,  +3.52e+20],
    ];

    # rescale fieldmap data to strength argument
    quadidx = monomials.index(1)
    seg_lens = [segmodel[i][1] for i in range(len(segmodel))]
    model_length = 2 * sum(seg_lens)
    fmap_strength = [2*segmodel[i][3+quadidx]*seg_lens[i]/model_length for i in range(len(segmodel))]
    rescale = [strength / fmap_strength[i] for i in range(len(segmodel))]

    # --- hard-edge 1-segment model ---
    model = []
    i = 0
    fam_name, element_type = segtypes[segmodel[i][0]]
    PolyB = _np.zeros(1+max(monomials))
    for j in range(len(monomials)):
        PolyB[monomials[j]] = segmodel[i][j+3] * rescale[i]
    PolyA = 0 * PolyB
    element = element_type(fam_name=fam_name, length=2*segmodel[i][1], K=PolyB[1])
    element.polynom_a = PolyA
    element.polynom_b = PolyB
    model.append(element)

    return model

def quadrupole_q30(fam_name, strength):

    segtypes = {
        fam_name      : (fam_name, _pyaccel.elements.quadrupole),
    }

    # Q30 model 2016-01-04
    # ====================
    # this (half) model is based on fieldmap
    # /home/fac_files/data/sirius/si/magnet_modelling/si-q30/model5/
    # '11-05-2015 Quadrupolo_Anel_Q30_Modelo 5_-14_14mm_-500_500mm.txt'
    monomials = [1,5,9,13]
    segmodel = [
        #type      len[m]     angle[deg]  PolyB(n=1)   PolyB(n=5)   PolyB(n=9)   PolyB(n=13)
        [fam_name, 0.150  ,  +0.00000 ,  -4.81e+00 ,  +1.03e+05 ,  -1.98e+13 ,  +3.62e+20],
    ];

    # rescale fieldmap data to strength argument
    quadidx = monomials.index(1)
    seg_lens = [segmodel[i][1] for i in range(len(segmodel))]
    model_length = 2 * sum(seg_lens)
    fmap_strength = [2*segmodel[i][3+quadidx]*seg_lens[i]/model_length for i in range(len(segmodel))]
    rescale = [strength / fmap_strength[i] for i in range(len(segmodel))]

    # --- hard-edge 1-segment model ---
    model = []
    i = 0
    fam_name, element_type = segtypes[segmodel[i][0]]
    PolyB = _np.zeros(1+max(monomials))
    for j in range(len(monomials)):
        PolyB[monomials[j]] = segmodel[i][j+3] * rescale[i]
    PolyA = 0 * PolyB
    element = element_type(fam_name=fam_name, length=2*segmodel[i][1], K=PolyB[1])
    element.polynom_a = PolyA
    element.polynom_b = PolyB
    model.append(element)

    return model
