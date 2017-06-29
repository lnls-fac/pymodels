import math as _math
import numpy as _np
import pyaccel as _pyaccel

def dipole_bc(m_accep_fam_name, simplified=False):

    segtypes = {
        'BC'      : ('BC', _pyaccel.elements.rbend),
        'BC_EDGE' : ('BC_EDGE', _pyaccel.elements.marker),
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
        ['BC',   0.005  ,  +0.09110 ,  +0.00e+00 ,  +3.82e-03 ,  -3.54e+01 ,  -3.99e+02 ,  -1.34e+05 ,  +5.52e+06 ,  -9.09e+09 ,  -2.68e+10 ,  +6.08e+13 ,  -2.20e+17],
        ['BC',   0.005  ,  +0.08089 ,  +0.00e+00 ,  -2.31e-02 ,  -2.21e+01 ,  +8.72e+01 ,  -2.76e+05 ,  -1.30e+06 ,  -1.92e+09 ,  +9.20e+09 ,  +1.70e+13 ,  -1.05e+17],
        ['BC',   0.005  ,  +0.06850 ,  +0.00e+00 ,  -2.20e-02 ,  -1.75e+01 ,  -3.23e+02 ,  +9.27e+04 ,  +6.39e+06 ,  -6.36e+09 ,  -3.56e+10 ,  +7.06e+13 ,  -2.92e+17],
        ['BC',   0.005  ,  +0.05892 ,  +0.00e+00 ,  -2.66e-02 ,  -1.08e+01 ,  -5.20e+01 ,  +3.55e+04 ,  +1.33e+06 ,  -2.88e+09 ,  -7.47e+09 ,  +3.38e+13 ,  -1.43e+17],
        ['BC',   0.010  ,  +0.09662 ,  +0.00e+00 ,  -2.65e-02 ,  -6.72e+00 ,  -3.36e-01 ,  -8.34e+03 ,  +3.02e+05 ,  -5.12e+08 ,  -2.04e+09 ,  +5.98e+12 ,  -2.47e+16],
        ['BC',   0.010  ,  +0.07443 ,  +0.00e+00 ,  -2.58e-02 ,  -4.19e+00 ,  -3.35e+01 ,  -9.69e+03 ,  +7.03e+05 ,  -8.59e+06 ,  -3.71e+09 ,  +3.18e+11 ,  -1.93e+15],
        ['BC',   0.010  ,  +0.05612 ,  +0.00e+00 ,  -2.56e-02 ,  -2.46e+00 ,  +2.77e+01 ,  -9.37e+02 ,  -3.93e+05 ,  -2.75e+06 ,  +2.18e+09 ,  -4.79e+11 ,  +3.31e+15],
        ['BC',   0.010  ,  +0.04318 ,  +0.00e+00 ,  -1.73e-02 ,  -2.57e-01 ,  +5.38e+01 ,  -3.12e+04 ,  -8.40e+05 ,  +7.89e+08 ,  +4.23e+09 ,  -8.42e+12 ,  +3.14e+16],
        ['m_accep', 0,0,0,0,0,0,0,0,0,0,0,0],
        ['BC',   0.064  ,  +0.21752 ,  +0.00e+00 ,  -7.09e-02 ,  +6.39e-02 ,  +3.43e+00 ,  +3.65e+02 ,  +2.55e+04 ,  -5.12e+06 ,  -3.70e+07 ,  -7.58e+10 ,  +6.63e+14],
        ['m_accep', 0,0,0,0,0,0,0,0,0,0,0,0],
        ['BC',   0.160  ,  +0.62805 ,  +0.00e+00 ,  -9.25e-01 ,  +3.00e-01 ,  +1.79e+01 ,  +1.94e+03 ,  +3.37e+04 ,  -3.75e+07 ,  -1.15e+08 ,  +3.71e+11 ,  -1.29e+15],
        ['m_accep', 0,0,0,0,0,0,0,0,0,0,0,0],
        ['BC',   0.160  ,  +0.62913 ,  +0.00e+00 ,  -9.36e-01 ,  +2.18e-02 ,  +1.57e+01 ,  -6.03e+02 ,  +1.76e+04 ,  +3.02e+07 ,  -4.16e+07 ,  -3.71e+11 ,  +1.57e+15],
        ['BC',   0.012  ,  +0.03774 ,  +0.00e+00 ,  -4.86e-01 ,  -6.29e+00 ,  -1.72e+01 ,  +2.01e+04 ,  +1.96e+05 ,  -5.15e+08 ,  -1.10e+09 ,  +5.40e+12 ,  -1.96e+16],
        ['BC_EDGE', 0,0,0,0,0,0,0,0,0,0,0,0],
        ['BC',   0.014  ,  +0.02843 ,  +0.00e+00 ,  -1.41e-01 ,  -4.21e+00 ,  -4.95e+01 ,  -7.83e+02 ,  +2.41e+04 ,  -9.98e+06 ,  +8.96e+07 ,  +2.20e+11 ,  -1.08e+15],
        ['BC',   0.016  ,  +0.01811 ,  +0.00e+00 ,  -4.29e-02 ,  -2.02e+00 ,  -1.23e+01 ,  +1.33e+03 ,  +2.72e+03 ,  -4.91e+07 ,  -6.36e+07 ,  +5.63e+11 ,  -2.25e+15],
        ['BC',   0.035  ,  +0.01956 ,  -3.56e-04 , -8.49e-03 ,  -1.21e+00 ,  +2.30e+00 ,  +8.79e+02 ,  -2.03e+04 ,  -1.57e+07 ,  +4.30e+07 ,  +1.30e+11 ,  -4.24e+14],
    ]

    # turns deflection angle error off (convenient for having a nominal model with zero 4d closed orbit)
    for i in range(len(segmodel)): segmodel[i][3] = 0.0

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

    if simplified:
        m_accep = _pyaccel.elements.marker(m_accep_fam_name)
        l = sum([s[1] for s in segmodel[:8]])
        ang1 = sum([s[2] for s in segmodel[:8]]) * d2r
        k = sum([s[4]*s[1] for s in segmodel[:8]])/l
        s = sum([s[5]*s[1] for s in segmodel[:8]])/l
        el = _pyaccel.elements.rbend(fam_name='BC', length=2*l, angle=2*ang1,
                     angle_in=0, angle_out=0,
                     gap=0, fint_in=0, fint_out=0,
                     polynom_a=[0,0,0], polynom_b=[0,k,s])
        l = sum([s[1] for s in segmodel[9:14]])
        ang2 = sum([s[2] for s in segmodel[9:]]) * d2r
        k = sum([s[4]*s[1] for s in segmodel[9:]])/l
        s = sum([s[5]*s[1] for s in segmodel[9:]])/l
        el_e = _pyaccel.elements.rbend(fam_name='BC', length=l, angle=ang2,
                     angle_in=0, angle_out=0*ang2,
                     gap=0, fint_in=0, fint_out=0,
                     polynom_a=[0,0,0], polynom_b=[0,k,s])
        el_b = _pyaccel.elements.rbend(fam_name='BC', length=l, angle=ang2,
                     angle_in=0*ang2, angle_out=0,
                     gap=0, fint_in=0, fint_out=0,
                     polynom_a=[0,0,0], polynom_b=[0,k,s])
        l2 = sum([s[1] for s in segmodel[14:]])
        dr = _pyaccel.elements.drift('LBC',l2)
        model = [dr,el_b,m_accep,el,m_accep,el_e,dr]

    return model

def dipole_b1(m_accep_fam_name, simplified=False):

    segtypes = {
        'B1'      : ('B1', _pyaccel.elements.rbend),
        'B1_EDGE' : ('B1_EDGE', _pyaccel.elements.marker),
        'mb1'     : ('mb1', _pyaccel.elements.marker),
        'm_accep' : (m_accep_fam_name, _pyaccel.elements.marker),
    }

    # FIELDMAP
    # *** interpolation of fields is now cubic ***
    # *** more refined segmented model.
    # *** dipole angle is now in units of degrees
    #--- model polynom_b (rz > 0). units: [m] for length, [rad] for angle and [m],[T] for polynom_b ---

    # B1 model 2017-02-01 (3GeV)
    # ===========================
    # dipole model-08
    # filename: 2017-02-01_B1_Model08_Sim_X=-32_32mm_Z=-1000_1000mm_Imc=451.8A.txt
    # trajectory centered in good-field region.
    # init_rx is set to  4.86 mm at s=0

    monomials = [0,1,2,3,4,5,6]
    segmodel = [
    #type     len[m]   angle[deg]  PolyB(n=0)   PolyB(n=1)   PolyB(n=2)   PolyB(n=3)   PolyB(n=4)   PolyB(n=5)   PolyB(n=6)
    ['B1',       0.0020 ,  +0.00646 ,  +0.00e+00 ,  -7.60e-01 ,  +1.94e-02 ,  +1.59e+00 ,  +4.18e+02 ,  -5.77e+03 ,  +3.91e+05],
    ['B1',       0.0030 ,  +0.00970 ,  +0.00e+00 ,  -7.61e-01 ,  +5.64e-02 ,  +1.24e+00 ,  +4.30e+02 ,  -5.59e+03 ,  +2.95e+05],
    ['B1',       0.0050 ,  +0.01619 ,  +0.00e+00 ,  -7.66e-01 ,  +1.47e-01 ,  +8.22e-01 ,  +4.16e+02 ,  -4.97e+03 ,  +2.83e+05],
    ['B1',       0.0050 ,  +0.01623 ,  +0.00e+00 ,  -7.72e-01 ,  +2.14e-01 ,  +1.28e+00 ,  +3.85e+02 ,  -5.43e+03 ,  +3.77e+05],
    ['B1',       0.0050 ,  +0.01625 ,  +0.00e+00 ,  -7.75e-01 ,  +2.19e-01 ,  +1.87e+00 ,  +3.76e+02 ,  -5.91e+03 ,  +4.08e+05],
    ['B1',       0.0100 ,  +0.03252 ,  +0.00e+00 ,  -7.75e-01 ,  +2.04e-01 ,  +1.95e+00 ,  +3.79e+02 ,  -5.95e+03 ,  +4.17e+05],
    ['B1',       0.0400 ,  +0.12981 ,  +0.00e+00 ,  -7.75e-01 ,  +2.07e-01 ,  +1.99e+00 ,  +3.78e+02 ,  -5.56e+03 ,  +4.12e+05],
    ['B1',       0.1500 ,  +0.48333 ,  +0.00e+00 ,  -7.74e-01 ,  +2.26e-01 ,  +3.09e+00 ,  +3.75e+02 ,  -4.32e+03 ,  +3.81e+05],
    ['B1',       0.1000 ,  +0.32210 ,  +0.00e+00 ,  -7.74e-01 ,  +2.37e-01 ,  +3.49e+00 ,  +3.81e+02 ,  -4.30e+03 ,  +3.79e+05],
    ['B1',       0.0500 ,  +0.16184 ,  +0.00e+00 ,  -7.76e-01 ,  +1.63e-01 ,  +1.91e+00 ,  +3.84e+02 ,  -4.74e+03 ,  +4.05e+05],
    ['B1',       0.0340 ,  +0.10488 ,  +0.00e+00 ,  -7.75e-01 ,  +4.45e-02 ,  +7.00e+00 ,  +3.51e+02 ,  -3.50e+02 ,  +2.17e+05],
    ['B1_EDGE', 0,0,0,0,0,0,0,0,0],
    ['B1',       0.0160 ,  +0.03288 ,  +0.00e+00 ,  -4.15e-01 ,  -1.96e+00 ,  +1.77e+01 ,  -9.80e+00 ,  +1.27e+04 ,  -2.71e+05],
    ['B1',       0.0400 ,  +0.03230 ,  +0.00e+00 ,  -7.58e-02 ,  -1.74e+00 ,  +8.17e+00 ,  -5.62e+01 ,  +3.68e+03 ,  -5.11e+03],
    ['B1',       0.0400 ,  +0.00813 ,  +0.00e+00 ,  -6.80e-03 ,  -4.05e-01 ,  +1.29e+00 ,  +1.35e+01 ,  -1.77e+01 ,  +5.25e+03],
    ['B1',       0.0500 ,  +0.00503 ,  -7.69e-05 ,  -3.07e-04 ,  -1.04e-01 ,  +1.64e-01 ,  +4.20e+00 ,  -1.00e+01 ,  -4.61e+02],
    ['B1_EDGE', 0,0,0,0,0,0,0,0,0],
    ]

    # # B1 model 2017-01-19 (3GeV)
    # # ===========================
    # # dipole model-07
    # # filename: 2017-01-19_B1_Model07_Sim_X=-32_32mm_Z=-1000_1000mm_Imc=452.4A.txt
    # # trajectory centered in good-field region.
    # # init_rx is set to  4.86 mm at s=0

    # monomials = [0,1,2,3,4,5,6];
    # segmodel = [ ...
    # #type     len[m]   angle[deg]  PolyB(n=0)   PolyB(n=1)   PolyB(n=2)   PolyB(n=3)   PolyB(n=4)   PolyB(n=5)   PolyB(n=6)
    # ['B1',       0.0020 ,  +0.00647 ,  +0.00e+00 ,  -7.64e-01 ,  +3.43e-01 ,  +2.06e+01 ,  +4.80e+02 ,  +8.81e+02 ,  -4.76e+05],
    # ['B1',       0.0030 ,  +0.00970 ,  +0.00e+00 ,  -7.65e-01 ,  +3.84e-01 ,  +2.02e+01 ,  +4.78e+02 ,  +1.67e+03 ,  -5.29e+05],
    # ['B1',       0.0050 ,  +0.01620 ,  +0.00e+00 ,  -7.71e-01 ,  +4.85e-01 ,  +1.96e+01 ,  +4.24e+02 ,  +2.99e+03 ,  -4.06e+05],
    # ['B1',       0.0050 ,  +0.01624 ,  +0.00e+00 ,  -7.76e-01 ,  +5.63e-01 ,  +2.00e+01 ,  +3.57e+02 ,  +3.20e+03 ,  -2.41e+05],
    # ['B1',       0.0050 ,  +0.01626 ,  +0.00e+00 ,  -7.79e-01 ,  +5.73e-01 ,  +2.07e+01 ,  +3.36e+02 ,  +2.76e+03 ,  -1.89e+05],
    # ['B1',       0.0100 ,  +0.03254 ,  +0.00e+00 ,  -7.80e-01 ,  +5.61e-01 ,  +2.09e+01 ,  +3.34e+02 ,  +2.44e+03 ,  -1.51e+05],
    # ['B1',       0.0400 ,  +0.12987 ,  +0.00e+00 ,  -7.79e-01 ,  +5.76e-01 ,  +2.09e+01 ,  +3.39e+02 ,  +2.08e+03 ,  -1.41e+05],
    # ['B1',       0.1500 ,  +0.48351 ,  +0.00e+00 ,  -7.78e-01 ,  +6.25e-01 ,  +2.19e+01 ,  +3.49e+02 ,  +1.54e+03 ,  -1.41e+05],
    # ['B1',       0.1000 ,  +0.32223 ,  +0.00e+00 ,  -7.78e-01 ,  +6.35e-01 ,  +2.23e+01 ,  +3.56e+02 ,  +1.56e+03 ,  -1.48e+05],
    # ['B1',       0.0500 ,  +0.16192 ,  +0.00e+00 ,  -7.80e-01 ,  +5.38e-01 ,  +2.07e+01 ,  +3.51e+02 ,  +2.38e+03 ,  -1.37e+05],
    # ['B1',       0.0340 ,  +0.10467 ,  +0.00e+00 ,  -7.64e-01 ,  -5.08e-01 ,  +4.78e+01 ,  +3.39e+02 ,  -1.26e+04 ,  -3.87e+03],
    # ['B1_EDGE', 0,0,0,0,0,0,0,0,0],
    # ['B1',       0.0160 ,  +0.03259 ,  +0.00e+00 ,  -3.74e-01 ,  -3.93e+00 ,  +7.91e+01 ,  +2.28e+02 ,  -3.59e+04 ,  +3.05e+05],
    # ['B1',       0.0400 ,  +0.03217 ,  +0.00e+00 ,  -6.65e-02 ,  -1.89e+00 ,  +1.05e+01 ,  +3.74e+01 ,  +7.56e+02 ,  -2.56e+04],
    # ['B1',       0.0400 ,  +0.00817 ,  +0.00e+00 ,  -5.77e-03 ,  -4.01e-01 ,  +1.17e+00 ,  +1.35e+01 ,  -1.75e+01 ,  +6.05e+03],
    # ['B1',       0.0500 ,  +0.00511 ,  -1.86e-05 ,  -3.84e-06 ,  -1.04e-01 ,  +1.43e-01 ,  +4.09e+00 ,  -9.02e+00 ,  -3.67e+02],
    # ['m_accep', 0,0,0,0,0,0,0,0,0],
    # ]

    # turns deflection angle error off (convenient for having a nominal model with zero 4d closed orbit)
    for i in range(len(segmodel)): segmodel[i][3] = 0.0

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

    if simplified:
        l = sum([s[1] for s in segmodel[:12]])
        ang = sum([s[2] for s in segmodel]) * d2r
        k = sum([s[4]*s[1] for s in segmodel])/l
        s = sum([s[5]*s[1] for s in segmodel])/l
        el = _pyaccel.elements.rbend(fam_name='B1', length=2*l, angle=2*ang,
                     angle_in=0*ang, angle_out=0*ang,
                     gap=0, fint_in=0, fint_out=0,
                     polynom_a=[0,0,0], polynom_b=[0,k,s])
        l2 = sum([s[1] for s in segmodel[12:]])
        dr = _pyaccel.elements.drift('LB1',l2)
        model = [dr,el,dr]


    return model

def dipole_b2(m_accep_fam_name, simplified=False):

    segtypes = {
        'B2'      : ('B2', _pyaccel.elements.rbend),
        'B2_EDGE' : ('B2_EDGE', _pyaccel.elements.marker),
        'mb2'     : ('mb2', _pyaccel.elements.marker),
        'm_accep' : (m_accep_fam_name, _pyaccel.elements.marker),
    }

    # FIELDMAP
    # *** interpolation of fields is now cubic ***
    # *** more refined segmented model.
    # *** dipole angle is now in units of degrees
    #--- model polynom_b (rz > 0). units: [m] for length, [rad] for angle and [m],[T] for polynom_b ---

    # B2 model 2017-02-01 (3GeV)
    # ===========================
    # dipole model-07
    # filename: 2017-02-01_B2_Model07_Sim_X=-63_27mm_Z=-1000_1000mm_Imc=451.8A.txt
    # trajectory centered in good-field region.
    # init_rx is set to  5.444 mm at s=0

    monomials = [0,1,2,3,4,5,6]
    segmodel = [
    #type     len[m]   angle[deg]  PolyB(n=0)   PolyB(n=1)   PolyB(n=2)   PolyB(n=3)   PolyB(n=4)   PolyB(n=5)   PolyB(n=6)
    ['B2',       0.1250 ,  +0.40617 ,  +0.00e+00 ,  -7.76e-01 ,  +1.52e-01 ,  -1.02e-01 ,  +3.47e+02 ,  -5.76e+03 ,  +4.30e+05],
    ['B2',       0.0550 ,  +0.17994 ,  +0.00e+00 ,  -7.76e-01 ,  +1.48e-01 ,  -7.59e-01 ,  +3.59e+02 ,  -7.09e+03 ,  +4.59e+05],
    ['B2',       0.0100 ,  +0.03277 ,  +0.00e+00 ,  -7.76e-01 ,  +1.67e-01 ,  -8.58e-01 ,  +3.50e+02 ,  -7.32e+03 ,  +4.82e+05],
    ['B2',       0.0050 ,  +0.01634 ,  +0.00e+00 ,  -7.71e-01 ,  +1.56e-01 ,  -1.80e+00 ,  +3.44e+02 ,  -6.44e+03 ,  +4.83e+05],
    ['B2',       0.0050 ,  +0.01631 ,  +0.00e+00 ,  -7.65e-01 ,  +6.84e-02 ,  -2.08e+00 ,  +3.65e+02 ,  -5.66e+03 ,  +3.89e+05],
    ['B2',       0.0050 ,  +0.01628 ,  +0.00e+00 ,  -7.61e-01 ,  -7.30e-03 ,  -1.62e+00 ,  +3.76e+02 ,  -6.32e+03 ,  +3.92e+05],
    ['m_accep',  0,0,0,0,0,0,0,0,0],
    ['B2',       0.0050 ,  +0.01630 ,  +0.00e+00 ,  -7.64e-01 ,  +5.10e-02 ,  -2.01e+00 ,  +3.73e+02 ,  -5.84e+03 ,  +3.90e+05],
    ['B2',       0.0100 ,  +0.03270 ,  +0.00e+00 ,  -7.72e-01 ,  +1.63e-01 ,  -1.44e+00 ,  +3.52e+02 ,  -6.74e+03 ,  +4.55e+05],
    ['B2',       0.0100 ,  +0.03277 ,  +0.00e+00 ,  -7.76e-01 ,  +1.61e-01 ,  -5.35e-01 ,  +3.60e+02 ,  -7.41e+03 ,  +4.73e+05],
    ['B2',       0.1750 ,  +0.56934 ,  +0.00e+00 ,  -7.75e-01 ,  +1.80e-01 ,  +7.06e-01 ,  +3.65e+02 ,  -6.08e+03 ,  +4.35e+05],
    ['B2',       0.1750 ,  +0.56881 ,  +0.00e+00 ,  -7.75e-01 ,  +1.84e-01 ,  +1.58e+00 ,  +3.84e+02 ,  -5.75e+03 ,  +4.27e+05],
    ['B2',       0.0200 ,  +0.06327 ,  +0.00e+00 ,  -7.96e-01 ,  +2.40e-02 ,  +6.47e+00 ,  +3.92e+02 ,  -3.96e+03 ,  +3.36e+05],
    ['B2',       0.0100 ,  +0.02704 ,  +0.00e+00 ,  -6.73e-01 ,  -2.43e-01 ,  +1.29e+01 ,  +7.85e+01 ,  +6.80e+03 ,  +1.98e+05],
    ['B2_EDGE', 0,0,0,0,0,0,0,0,0],
    ['B2',       0.0150 ,  +0.02831 ,  +0.00e+00 ,  -3.48e-01 ,  -2.36e+00 ,  +1.83e+01 ,  -1.03e+02 ,  +1.34e+04 ,  -6.97e+04],
    ['B2',       0.0200 ,  +0.01996 ,  +0.00e+00 ,  -1.02e-01 ,  -2.16e+00 ,  +1.07e+01 ,  -1.02e+02 ,  +5.84e+03 ,  -3.09e+04],
    ['B2',       0.0300 ,  +0.01244 ,  +0.00e+00 ,  -2.21e-02 ,  -9.29e-01 ,  +3.84e+00 ,  +4.06e+00 ,  +3.46e+02 ,  +4.58e+03],
    ['B2',       0.0320 ,  +0.00487 ,  +0.00e+00 ,  -3.89e-03 ,  -2.80e-01 ,  +8.00e-01 ,  +1.18e+01 ,  -2.70e+01 ,  +8.66e+01],
    ['B2',       0.0325 ,  +0.00458 ,  -1.14e-04 ,  -7.17e-05 ,  -1.39e-01 ,  +1.99e-01 ,  +5.42e+00 ,  -1.25e+01 ,  -2.30e+02],
    ['m_accep',  0,0,0,0,0,0,0,0,0],
    ];

    # # B2 model 2017-01-19 (3GeV)
    # # ===========================
    # # dipole model-06
    # # filename: 2017-01-19_B2_Model06_Sim_X=-63_27mm_Z=-1000_1000mm_Imc=452.4A.txt
    # # trajectory centered in good-field region.
    # # init_rx is set to  5.444 mm at s=0
    #
    # monomials = [0,1,2,3,4,5,6];
    # segmodel = [ ...
    # #type     len[m]   angle[deg]  PolyB(n=0)   PolyB(n=1)   PolyB(n=2)   PolyB(n=3)   PolyB(n=4)   PolyB(n=5)   PolyB(n=6)
    # ['B1',       0.1250 ,  +0.40641 ,  +0.00e+00 ,  -7.81e-01 ,  +5.25e-01 ,  +1.91e+01 ,  +3.09e+02 ,  +2.07e+03 ,  -1.29e+05],
    # ['B1',       0.0550 ,  +0.18003 ,  +0.00e+00 ,  -7.81e-01 ,  +4.73e-01 ,  +1.83e+01 ,  +3.07e+02 ,  +2.54e+03 ,  -1.32e+05],
    # ['B1',       0.0100 ,  +0.03273 ,  +0.00e+00 ,  -7.71e-01 ,  -2.68e-02 ,  +2.62e+01 ,  +4.24e+02 ,  -3.04e+03 ,  -2.08e+05],
    # ['B1',       0.0050 ,  +0.01629 ,  +0.00e+00 ,  -7.49e-01 ,  -1.10e+00 ,  +5.44e+01 ,  +4.73e+02 ,  -2.07e+04 ,  -2.98e+05],
    # ['B1',       0.0050 ,  +0.01623 ,  +0.00e+00 ,  -7.27e-01 ,  -2.25e+00 ,  +8.90e+01 ,  +4.10e+02 ,  -4.39e+04 ,  -3.11e+05],
    # ['B1',       0.0050 ,  +0.01619 ,  +0.00e+00 ,  -7.15e-01 ,  -2.91e+00 ,  +1.10e+02 ,  +3.40e+02 ,  -6.12e+04 ,  -5.94e+04],
    # ['m_accep',  0,0,0,0,0,0,0,0,0],
    # ['B1',       0.0050 ,  +0.01621 ,  +0.00e+00 ,  -7.24e-01 ,  -2.41e+00 ,  +9.44e+01 ,  +3.77e+02 ,  -4.89e+04 ,  -1.44e+05],
    # ['B1',       0.0100 ,  +0.03261 ,  +0.00e+00 ,  -7.54e-01 ,  -8.11e-01 ,  +4.69e+01 ,  +4.70e+02 ,  -1.68e+04 ,  -2.89e+05],
    # ['B1',       0.0100 ,  +0.03276 ,  +0.00e+00 ,  -7.76e-01 ,  +2.51e-01 ,  +2.07e+01 ,  +3.79e+02 ,  +8.97e+02 ,  -2.07e+05],
    # ['B1',       0.1750 ,  +0.56967 ,  +0.00e+00 ,  -7.80e-01 ,  +5.40e-01 ,  +1.97e+01 ,  +3.22e+02 ,  +2.16e+03 ,  -1.32e+05],
    # ['B1',       0.1750 ,  +0.56914 ,  +0.00e+00 ,  -7.80e-01 ,  +5.44e-01 ,  +2.05e+01 ,  +3.42e+02 ,  +2.35e+03 ,  -1.36e+05],
    # ['B1',       0.0200 ,  +0.06318 ,  +0.00e+00 ,  -7.88e-01 ,  -3.06e-01 ,  +3.82e+01 ,  +4.79e+02 ,  -7.84e+03 ,  -1.62e+05],
    # ['B1',       0.0100 ,  +0.02685 ,  +0.00e+00 ,  -6.30e-01 ,  -2.81e+00 ,  +1.08e+02 ,  +1.29e+02 ,  -5.80e+04 ,  +5.56e+05],
    # ['B1_EDGE', 0,0,0,0,0,0,0,0,0],
    # ['B1',       0.0150 ,  +0.02805 ,  +0.00e+00 ,  -3.10e-01 ,  -4.08e+00 ,  +6.51e+01 ,  +3.98e+02 ,  -2.71e+04 ,  -6.68e+04],
    # ['B1',       0.0200 ,  +0.01985 ,  +0.00e+00 ,  -8.89e-02 ,  -2.39e+00 ,  +1.37e+01 ,  +4.48e+01 ,  +1.83e+03 ,  -6.34e+04],
    # ['B1',       0.0300 ,  +0.01245 ,  +0.00e+00 ,  -1.92e-02 ,  -9.29e-01 ,  +3.56e+00 ,  +1.29e+01 ,  +1.85e+02 ,  -1.43e+03],
    # ['B1',       0.0320 ,  +0.00490 ,  +0.00e+00 ,  -3.20e-03 ,  -2.77e-01 ,  +7.22e-01 ,  +1.16e+01 ,  -2.70e+01 ,  -2.25e+02],
    # ['B1',       0.0325 ,  +0.00465 ,  -7.71e-05 ,  +3.45e-04 ,  -1.39e-01 ,  +1.73e-01 ,  +5.30e+00 ,  -1.21e+01 ,  -2.16e+02],
    # ['m_accep',  0,0,0,0,0,0,0,0,0],
    # ];

    # turns deflection angle error off (convenient for having a nominal model with zero 4d closed orbit)
    for i in range(len(segmodel)): segmodel[i][3] = 0.0

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

    if simplified:
        l = sum([s[1] for s in segmodel[:15]])
        ang = sum([s[2] for s in segmodel]) * d2r
        k = sum([s[4]*s[1] for s in segmodel])/l
        s = sum([s[5]*s[1] for s in segmodel])/l
        el = _pyaccel.elements.rbend(fam_name='B2', length=2*l, angle=2*ang,
                     angle_in=0*ang, angle_out=0*ang,
                     gap=0, fint_in=0, fint_out=0,
                     polynom_a=[0,0,0], polynom_b=[0,k,s])
        l2 = sum([s[1] for s in segmodel[15:]])
        dr = _pyaccel.elements.drift('LB2',l2)
        model = [dr,el,dr]

    return model

def quadrupole_q14(fam_name, strength, simplified=False):

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

    if simplified:
        model[0].polynom_a = model[0].polynom_a[:3]
        model[0].polynom_b = model[0].polynom_b[:3]

    return model

def quadrupole_q20(fam_name, strength, simplified=False):

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

    if simplified:
        model[0].polynom_a = model[0].polynom_a[:3]
        model[0].polynom_b = model[0].polynom_b[:3]

    return model

def quadrupole_q30(fam_name, strength, simplified=False):

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

    if simplified:
        model[0].polynom_a = model[0].polynom_a[:3]
        model[0].polynom_b = model[0].polynom_b[:3]

    return model
