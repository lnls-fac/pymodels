"""Segmented models of the lattice."""

import math as _math
import numpy as _np
import pyaccel as _pyaccel


def dipole_bc(m_accep_fam_name, simplified=False):
    """Segmented BC dipole model."""
    segtypes = {
        'BC': ('BC', _pyaccel.elements.rbend),
        'BC_EDGE': ('BC_EDGE', _pyaccel.elements.marker),
        'mc': ('mc', _pyaccel.elements.marker),
        'm_accep': (m_accep_fam_name, _pyaccel.elements.marker),
    }

    # dipole model 2017-08-21
    # =======================
    # this (half) model is based on fieldmap
    # /home/fac_files/lnls-ima/si-dipoles-bc/model-12/analysis/fieldmap/3gev
    # '2017-08-21_bc_model12_X=-90_12mm_Z=-1000_1000mm.txt'
    monomials = [0, 1, 2, 3, 4, 5, 6, 7, 8, 10]
    segmodel = [
        # --- model polynom_b (rz > 0). units: [m] for length, [rad] for angle
        #     and [m^(n-1)] for polynom_b ---
        # type    len[m]    angle[deg]  PolyB(n=0)   PolyB(n=1)   PolyB(n=2)
        # PolyB(n=3)   PolyB(n=4)   PolyB(n=5)   PolyB(n=6)   PolyB(n=7)
        # PolyB(n=8)   PolyB(n=10)
        ['BC', 0.0010, +0.01811, +0.00e+00, -7.24e-04, -3.47e+01, +1.43e+01,
            -4.22e+05, -2.54e+05, -1.85e+09, +1.30e+09, -2.14e+13, +1.12e+17],
        ['BC', 0.0040, +0.07079, +0.00e+00, -4.37e-03, -3.17e+01, -6.82e+01,
            -4.36e+05, +1.73e+06, -5.58e+08, -1.01e+10, -2.76e+13, +1.22e+17],
        ['BC', 0.0050, +0.07926, +0.00e+00, -1.89e-02, -2.33e+01, -3.04e+01,
            -2.85e+05, +1.13e+06, -2.61e+08, -5.05e+09, -1.24e+13, +5.76e+16],
        ['BC', 0.0050, +0.06748, +0.00e+00, -2.55e-02, -1.46e+01, +6.07e+00,
            -1.19e+05, +3.42e+05, -5.11e+08, -1.07e+09, +2.60e+12, -8.18e+15],
        ['BC', 0.0050, +0.05823, +0.00e+00, -2.57e-02, -9.80e+00, +8.44e+00,
            -5.66e+04, +1.68e+05, -1.97e+08, -5.98e+08, +1.66e+12, -6.58e+15],
        ['BC', 0.0100, +0.09572, +0.00e+00, -2.51e-02, -6.65e+00, +7.74e+00,
            -2.29e+04, +6.06e+04, -6.27e+07, -2.20e+08, +6.40e+11, -2.67e+15],
        ['BC', 0.0100, +0.07398, +0.00e+00, -2.47e-02, -4.32e+00, +5.52e+00,
            -8.13e+03, +1.98e+04, -9.65e+06, -7.09e+07, +1.11e+11, -5.05e+14],
        ['BC', 0.0100, +0.05634, +0.00e+00, -2.27e-02, -2.55e+00, +3.46e+00,
            -3.93e+03, +1.24e+04, +2.05e+07, -3.75e+07, -2.37e+11, +9.31e+14],
        ['BC', 0.0100, +0.04442, +0.00e+00, -1.32e-02, -1.09e+00, +2.67e+00,
            -2.80e+02, -4.69e+03, -2.38e+07, +3.19e+07, +2.80e+11, -1.14e+15],
        ['m_accep', 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        ['BC', 0.0320, +0.11599, +0.00e+00, -9.09e-03, +9.07e-01, +1.48e+00,
            -4.07e+02, +6.66e+03, -7.84e+06, -6.52e+06, +7.39e+10, -3.00e+14],
        ['BC', 0.0320, +0.09680, +0.00e+00, -1.38e-01, +3.20e-01, +1.07e+01,
            +1.76e+02, -9.07e+03, -1.64e+07, +6.54e+07, +1.97e+11, -8.16e+14],
        ['m_accep', 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        ['BC', 0.1600, +0.62773, +0.00e+00, -8.90e-01, +3.19e-01, +1.26e+01,
            +1.06e+02, +1.00e+04, +3.95e+06, -3.64e+06, -4.71e+10, +1.88e+14],
        ['m_accep', 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        ['BC', 0.1600, +0.63145, +0.00e+00, -9.06e-01, +1.55e-01, +9.63e+00,
            +2.87e+02, +8.14e+03, -6.01e+05, +1.20e+07, +5.81e+09, -2.47e+13],
        ['BC', 0.0120, +0.04291, +0.00e+00, -8.77e-01, +4.85e-02, +1.80e+01,
            +8.37e+02, -2.17e+04, -1.87e+07, +2.00e+08, +2.16e+11, -8.81e+14],
        ['BC_EDGE', 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        ['BC', 0.0140, +0.03356, +0.00e+00, -4.36e-01, -2.13e+00, +9.42e+00,
            -1.20e+03, +6.79e+04, +2.39e+07, -2.85e+08, -2.50e+11, +9.60e+14],
        ['BC', 0.0160, +0.01936, +0.00e+00, -1.08e-01, -2.06e+00, +3.12e+00,
            +1.91e+02, +2.03e+04, -1.06e+07, -5.57e+07, +1.06e+11, -3.64e+14],
        ['BC', 0.0350, +0.01617, -1.59e-04, -1.89e-02, -1.18e+00, +2.57e+00,
            +8.67e+01, +3.56e+03, -3.67e+06, -1.78e+07, +4.03e+10, -1.49e+14],
    ]

    # turns deflection angle error off (convenient for having a nominal model
    # with zero 4d closed orbit)
    for i in range(len(segmodel)):
        segmodel[i][3] = 0.0

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
            element = element_type(fam_name=fam_name, length=segmodel[i][1],
                                   angle=d2r * segmodel[i][2],
                                   angle_in=0, angle_out=0,
                                   gap=0, fint_in=0, fint_out=0,
                                   polynom_a=PolyA, polynom_b=PolyB)
        else:
            element = element_type(fam_name)
        model.append(element)

    # --- adds additional markers ---
    mc = segtypes['mc'][1](segtypes['mc'][0])
    maccep = segtypes['m_accep'][1](segtypes['m_accep'][0])
    model = model[::-1] + [mc, maccep] + model

    if simplified:
        m_accep = _pyaccel.elements.marker(m_accep_fam_name)
        le = sum([s[1] for s in segmodel[:8]])
        ang1 = sum([s[2] for s in segmodel[:8]]) * d2r
        k = sum([s[4]*s[1] for s in segmodel[:8]])/le
        s = sum([s[5]*s[1] for s in segmodel[:8]])/le
        el = _pyaccel.elements.rbend(fam_name='BC', length=2*le, angle=2*ang1,
                                     angle_in=0, angle_out=0,
                                     gap=0, fint_in=0, fint_out=0,
                                     polynom_a=[0, 0, 0], polynom_b=[0, k, s])
        le = sum([s[1] for s in segmodel[9:14]])
        ang2 = sum([s[2] for s in segmodel[9:]]) * d2r
        k = sum([s[4]*s[1] for s in segmodel[9:]])/le
        s = sum([s[5]*s[1] for s in segmodel[9:]])/le
        el_e = _pyaccel.elements.rbend(
            fam_name='BC', length=le, angle=ang2,
            angle_in=0, angle_out=0*ang2,
            gap=0, fint_in=0, fint_out=0,
            polynom_a=[0, 0, 0], polynom_b=[0, k, s])
        el_b = _pyaccel.elements.rbend(
            fam_name='BC', length=le, angle=ang2,
            angle_in=0*ang2, angle_out=0,
            gap=0, fint_in=0, fint_out=0,
            polynom_a=[0, 0, 0], polynom_b=[0, k, s])
        l2 = sum([s[1] for s in segmodel[14:]])
        dr = _pyaccel.elements.drift('LBC', l2)
        model = [dr, el_b, m_accep, el, m_accep, el_e, dr]

    return model


def dipole_b1(m_accep_fam_name, simplified=False):
    """Segmented B1 dipole model."""
    segtypes = {
        'B1': ('B1', _pyaccel.elements.rbend),
        'B1_EDGE': ('B1_EDGE', _pyaccel.elements.marker),
        'mb1': ('mb1', _pyaccel.elements.marker),
        'm_accep': (m_accep_fam_name, _pyaccel.elements.marker),
    }

    # FIELDMAP
    # *** interpolation of fields is now cubic ***
    # *** more refined segmented model.
    # *** dipole angle is now in units of degrees
    # -- model polynom_b (rz > 0). units: [m] for length, [rad] for angle and
    #   [m],[T] for polynom_b ---
    #  B1 model 09 (3 GeV)
    # ========================
    # filename:
    #   2017-05-17_B1_Model09_Sim_X=-32_32mm_Z=-1000_1000mm_Imc=394.1A.txt
    # trajectory centered in good-field region.
    # init_rx is set to +8.285 mm at s=0

    monomials = [0, 1, 2, 3, 4, 5, 6]
    segmodel = [
        # type     len[m]    angle[deg]  PolyB(n=0)   PolyB(n=1)   PolyB(n=2)
        #                   PolyB(n=3)   PolyB(n=4)   PolyB(n=5)   PolyB(n=6)
        ['B1', 0.0020, +0.00644, +0.00e+00, -7.53e-01, -2.97e-01, +7.76e-01,
         -3.78e+01, +7.77e+03, -5.44e+04],
        ['B1', 0.0030, +0.00966, +0.00e+00, -7.56e-01, -2.45e-01, +4.51e-01,
         -3.89e+01, +6.50e+03, -1.57e+04],
        ['B1', 0.0050, +0.01614, +0.00e+00, -7.62e-01, -1.17e-01, -2.34e-01,
         -4.51e+01, +5.95e+03, +7.06e+04],
        ['B1', 0.0050, +0.01620, +0.00e+00, -7.70e-01, -1.50e-02, +5.46e-02,
         -3.70e+01, +5.27e+03, +7.14e+04],
        ['B1', 0.0050, +0.01623, +0.00e+00, -7.74e-01, +3.80e-03, +7.50e-01,
         -2.40e+01, +4.25e+03, +1.20e+05],
        ['B1', 0.0100, +0.03250, +0.00e+00, -7.75e-01, -3.12e-03, +9.79e-01,
         +2.39e+00, +3.53e+03, +1.25e+05],
        ['B1', 0.0400, +0.12976, +0.00e+00, -7.74e-01, +1.95e-02, +1.11e+00,
         +2.39e+01, +3.18e+03, +1.28e+05],
        ['B1', 0.1500, +0.48326, +0.00e+00, -7.73e-01, +5.49e-02, +1.99e+00,
         +4.10e+01, +3.41e+03, +1.45e+05],
        ['B1', 0.1000, +0.32210, +0.00e+00, -7.73e-01, +7.58e-02, +2.68e+00,
         +5.40e+01, +3.46e+03, +1.39e+05],
        ['B1', 0.0500, +0.16186, +0.00e+00, -7.74e-01, +7.84e-03, +1.72e+00,
         +4.94e+01, +3.68e+03, +1.38e+05],
        ['B1', 0.0340, +0.10511, +0.00e+00, -7.77e-01, -1.59e-01, +5.66e+00,
         +3.21e+01, +7.92e+03, -1.37e+04],
        ['B1_EDGE', 0, 0, 0, 0, 0, 0, 0, 0, 0],
        ['B1', 0.0160, +0.03328, +0.00e+00, -4.28e-01, -2.23e+00, +1.60e+01,
         -1.87e+02, +1.74e+04, -3.29e+05],
        ['B1', 0.0400, +0.03267, +0.00e+00, -8.48e-02, -1.96e+00, +7.58e+00,
         -5.17e+01, +5.46e+03, +5.56e+03],
        ['B1', 0.0400, +0.00789, +0.00e+00, -9.10e-03, -4.28e-01, +1.56e+00,
         +2.04e+01, +3.49e+01, +1.22e+03],
        ['B1', 0.0500, +0.00455, -3.81e-06, -9.98e-04, -1.02e-01, +2.07e-01,
         +4.49e+00, -1.54e+01, -6.34e+02],
        ['m_accep', 0, 0, 0, 0, 0, 0, 0, 0, 0],
    ]

    # turns deflection angle error off (convenient for having a nominal model
    # with zero 4d closed orbit)
    for i in range(len(segmodel)):
        segmodel[i][3] = 0.0

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
            element = element_type(fam_name=fam_name, length=segmodel[i][1],
                                   angle=d2r * segmodel[i][2],
                                   angle_in=0, angle_out=0,
                                   gap=0, fint_in=0, fint_out=0,
                                   polynom_a=PolyA, polynom_b=PolyB)
        else:
            element = element_type(fam_name)
        model.append(element)

    # --- adds additional markers ---
    mb1 = segtypes['mb1'][1](segtypes['mb1'][0])
    maccep = segtypes['m_accep'][1](segtypes['m_accep'][0])
    model = model[::-1] + [mb1, maccep] + model

    if simplified:
        le = sum([s[1] for s in segmodel[:12]])
        ang = sum([s[2] for s in segmodel]) * d2r
        k = sum([s[4]*s[1] for s in segmodel])/le
        s = sum([s[5]*s[1] for s in segmodel])/le
        el = _pyaccel.elements.rbend(
            fam_name='B1', length=2*le, angle=2*ang,
            angle_in=0*ang, angle_out=0*ang,
            gap=0, fint_in=0, fint_out=0,
            polynom_a=[0, 0, 0], polynom_b=[0, k, s])
        l2 = sum([s[1] for s in segmodel[12:]])
        dr = _pyaccel.elements.drift('LB1', l2)
        model = [dr, el, dr]

    return model


def dipole_b2(m_accep_fam_name, simplified=False):
    """Segmented B2 dipole model."""
    segtypes = {
        'B2': ('B2', _pyaccel.elements.rbend),
        'B2_EDGE': ('B2_EDGE', _pyaccel.elements.marker),
        'mb2': ('mb2', _pyaccel.elements.marker),
        'm_accep': (m_accep_fam_name, _pyaccel.elements.marker),
    }

    #  FIELDMAP
    #  *** interpolation of fields is now cubic ***
    #  *** more refined segmented model.
    #  *** dipole angle is now in units of degrees
    # --- model polynom_b (rz > 0). units: [m] for length, [rad] for angle
    # and [m],[T] for polynom_b ---

    #  B2 model 08 (3 GeV)
    #  ===================
    #  filename:
    #  2017-05-17_B2_Model08_Sim_X=-63_27mm_Z=-1000_1000mm_Imc=394.1A.txt
    #  trajectory centered in good-field region.
    #  init_rx is set to  7.92 mm at s=0

    monomials = [0, 1, 2, 3, 4, 5, 6]
    segmodel = [
        # type     len[m]    angle[deg]  PolyB(n=0)   PolyB(n=1)   PolyB(n=2)
        #                   PolyB(n=3)   PolyB(n=4)   PolyB(n=5)   PolyB(n=6)
        ['B2', 0.1250, +0.40481, +0.00e+00, -7.74e-01, +4.46e-02, +1.66e+00,
         +3.21e+01, +3.14e+03, +1.33e+05],
        ['B2', 0.0550, +0.17931, +0.00e+00, -7.74e-01, +2.77e-02, +1.44e+00,
         +2.26e+01, +2.92e+03, +1.21e+05],
        ['B2', 0.0100, +0.03263, +0.00e+00, -7.74e-01, +1.78e-02, +1.27e+00,
         -1.80e+01, +4.06e+03, +9.54e+04],
        ['B2', 0.0050, +0.01626, +0.00e+00, -7.67e-01, -1.88e-02, +3.45e-01,
         -3.28e+01, +5.41e+03, +7.86e+03],
        ['B2', 0.0050, +0.01620, +0.00e+00, -7.59e-01, -1.50e-01, +3.96e-01,
         -4.87e+01, +6.49e+03, +4.25e+04],
        ['B2', 0.0050, +0.01617, +0.00e+00, -7.53e-01, -2.68e-01, +1.14e+00,
         -3.73e+01, +7.62e+03, -7.89e+04],
        ['m_accep', 0, 0, 0, 0, 0, 0, 0, 0, 0],
        ['B2', 0.0050, +0.01619, +0.00e+00, -7.56e-01, -1.95e-01, +6.57e-01,
         -4.55e+01, +7.04e+03, +2.61e+03],
        ['B2', 0.0100, +0.03253, +0.00e+00, -7.68e-01, -1.11e-02, +6.49e-01,
         -3.45e+01, +5.44e+03, +3.61e+04],
        ['B2', 0.0100, +0.03265, +0.00e+00, -7.74e-01, +2.23e-02, +1.71e+00,
         -1.24e+00, +3.61e+03, +1.07e+05],
        ['B2', 0.1750, +0.56774, +0.00e+00, -7.73e-01, +8.13e-02, +2.99e+00,
         +5.39e+01, +2.92e+03, +1.23e+05],
        ['B2', 0.1750, +0.56735, +0.00e+00, -7.73e-01, +1.07e-01, +4.38e+00,
         +8.27e+01, +3.27e+03, +1.22e+05],
        ['B2', 0.0200, +0.06336, +0.00e+00, -7.91e-01, -3.03e-02, +8.98e+00,
         +8.71e+01, +7.12e+03, +3.61e+04],
        ['B2', 0.0100, +0.02751, +0.00e+00, -6.82e-01, -2.04e-01, +1.38e+01,
         -1.03e+02, +1.27e+04, -2.77e+05],
        ['B2_EDGE', 0, 0, 0, 0, 0, 0, 0, 0, 0],
        ['B2', 0.0150, +0.02960, +0.00e+00, -3.61e-01, -2.44e+00, +1.92e+01,
         -2.39e+02, +1.75e+04, -2.13e+05],
        ['B2', 0.0200, +0.02204, +0.00e+00, -1.08e-01, -2.48e+00, +1.07e+01,
         -1.61e+02, +7.25e+03, +2.19e+03],
        ['B2', 0.0300, +0.01445, +0.00e+00, -2.59e-02, -1.22e+00, +4.05e+00,
         -8.35e+00, +6.42e+02, +2.43e+04],
        ['B2', 0.0320, +0.00530, +0.00e+00, -5.22e-03, -3.59e-01, +1.00e+00,
         +1.67e+01, -4.09e+01, +3.58e+03],
        ['B2', 0.0325, +0.00410, +6.74e-06, -1.02e-03, -1.49e-01, +2.51e-01,
         +6.75e+00, -1.79e+01, +3.81e+01],
        ['m_accep', 0, 0, 0, 0, 0, 0, 0, 0, 0],
    ]

    # turns deflection angle error off (convenient for having a nominal model
    # with zero 4d closed orbit)
    for i in range(len(segmodel)):
        segmodel[i][3] = 0.0

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
            element = element_type(
                fam_name=fam_name, length=segmodel[i][1],
                angle=d2r * segmodel[i][2],
                angle_in=0, angle_out=0,
                gap=0, fint_in=0, fint_out=0,
                polynom_a=PolyA, polynom_b=PolyB)
        else:
            element = element_type(fam_name)
        model.append(element)

    # --- adds additional markers ---
    mb2 = segtypes['mb2'][1](segtypes['mb2'][0])
    maccep = segtypes['m_accep'][1](segtypes['m_accep'][0])
    model = model[::-1] + [mb2, maccep] + model

    if simplified:
        le = sum([s[1] for s in segmodel[:15]])
        ang = sum([s[2] for s in segmodel]) * d2r
        k = sum([s[4]*s[1] for s in segmodel])/le
        s = sum([s[5]*s[1] for s in segmodel])/le
        el = _pyaccel.elements.rbend(
                fam_name='B2', length=2*le, angle=2*ang,
                angle_in=0*ang, angle_out=0*ang,
                gap=0, fint_in=0, fint_out=0,
                polynom_a=[0, 0, 0], polynom_b=[0, k, s])
        l2 = sum([s[1] for s in segmodel[15:]])
        dr = _pyaccel.elements.drift('LB2', l2)
        model = [dr, el, dr]

    return model


def quadrupole_q14(fam_name, strength, simplified=False):
    """Segmented Q14 dipole model."""
    segtypes = {
        fam_name: (fam_name, _pyaccel.elements.quadrupole),
    }

    # Q14 model
    # =========
    # this (half) model is based on fieldmap
    # '2017-02-24_Q14_Model04_Sim_X=-14_14mm_Z=-500_500mm_Imc=146.6A_Itc=10A.txt'
    monomials = [1, 5, 9, 13]
    segmodel = [
        # type  len[m]   angle[deg]  PolyB(n=1)   PolyB(n=5)   PolyB(n=9)
        #                            PolyB(n=13)
        [fam_name, 0.0700, +0.00000, -4.06e+00, +6.38e+04, -1.45e+13,
         +2.90e+20],
    ]

    # rescale fieldmap data to strength argument
    quadidx = monomials.index(1)
    seg_lens = [segmodel[i][1] for i in range(len(segmodel))]
    model_length = 2 * sum(seg_lens)
    fmap_strength = [2*segmodel[i][3+quadidx]*seg_lens[i]/model_length for i in
                     range(len(segmodel))]
    rescale = [strength / fmap_strength[i] for i in range(len(segmodel))]

    # --- hard-edge 1-segment model ---
    model = []
    i = 0
    fam_name, element_type = segtypes[segmodel[i][0]]
    PolyB = _np.zeros(1+max(monomials))
    for j in range(len(monomials)):
        PolyB[monomials[j]] = segmodel[i][j+3] * rescale[i]
    PolyA = 0 * PolyB
    element = element_type(fam_name=fam_name,
                           length=2*segmodel[i][1], K=PolyB[1])
    element.polynom_a = PolyA
    element.polynom_b = PolyB
    model.append(element)

    if simplified:
        model[0].polynom_a = model[0].polynom_a[:3]
        model[0].polynom_b = model[0].polynom_b[:3]

    return model


def quadrupole_q20(fam_name, strength, simplified=False):
    """Segmented Q20 dipole model."""
    segtypes = {
        fam_name: (fam_name, _pyaccel.elements.quadrupole),
    }

    # Q20 model
    # =========
    # this (half) model is based on fieldmap
    # '2017-02-24_Q20_Model05_Sim_X=-14_14mm_Z=-500_500mm_Imc=
    #  154.66A_Itc=10A.txt'
    monomials = [1, 5, 9, 13]
    segmodel = [
        # type  len[m]   angle[deg]  PolyB(n=1)   PolyB(n=5)   PolyB(n=9)
        #                                                      PolyB(n=13)
        [fam_name, 0.1000, +0.00000, -4.74e+00, +8.41e+04, -1.83e+13,
         +3.47e+20],
    ]

    # rescale fieldmap data to strength argument
    quadidx = monomials.index(1)
    seg_lens = [segmodel[i][1] for i in range(len(segmodel))]
    model_length = 2 * sum(seg_lens)
    fmap_strength = [2*segmodel[i][3+quadidx]*seg_lens[i]/model_length for i in
                     range(len(segmodel))]
    rescale = [strength / fmap_strength[i] for i in range(len(segmodel))]

    # --- hard-edge 1-segment model ---
    model = []
    i = 0
    fam_name, element_type = segtypes[segmodel[i][0]]
    PolyB = _np.zeros(1+max(monomials))
    for j in range(len(monomials)):
        PolyB[monomials[j]] = segmodel[i][j+3] * rescale[i]
    PolyA = 0 * PolyB
    element = element_type(fam_name=fam_name,
                           length=2*segmodel[i][1], K=PolyB[1])
    element.polynom_a = PolyA
    element.polynom_b = PolyB
    model.append(element)

    if simplified:
        model[0].polynom_a = model[0].polynom_a[:3]
        model[0].polynom_b = model[0].polynom_b[:3]

    return model


def quadrupole_q30(fam_name, strength, simplified=False):
    """Segmented Q30 dipole model."""
    segtypes = {
        fam_name: (fam_name, _pyaccel.elements.quadrupole),
    }

    # Q30 model
    # =========
    # this (half) model is based on fieldmap
    # '2017-02-24_Q30_Model06_Sim_X=-14_14mm_Z=-500_500mm_Imc=
    #  153.8A_Itc=10A.txt'
    monomials = [1, 5, 9, 13]
    segmodel = [
        # type  len[m]   angle[deg]  PolyB(n=1)   PolyB(n=5)   PolyB(n=9)
        #                                                      PolyB(n=13)
        [fam_name, 0.1500, +0.00000, -4.75e+00, +1.06e+05, -1.95e+13,
         +3.56e+20],
    ]

    # rescale fieldmap data to strength argument
    quadidx = monomials.index(1)
    seg_lens = [segmodel[i][1] for i in range(len(segmodel))]
    model_length = 2 * sum(seg_lens)
    fmap_strength = [2*segmodel[i][3+quadidx]*seg_lens[i]/model_length for i in
                     range(len(segmodel))]
    rescale = [strength / fmap_strength[i] for i in range(len(segmodel))]

    # --- hard-edge 1-segment model ---
    model = []
    i = 0
    fam_name, element_type = segtypes[segmodel[i][0]]
    PolyB = _np.zeros(1+max(monomials))
    for j in range(len(monomials)):
        PolyB[monomials[j]] = segmodel[i][j+3] * rescale[i]
    PolyA = 0 * PolyB
    element = element_type(fam_name=fam_name,
                           length=2*segmodel[i][1], K=PolyB[1])
    element.polynom_a = PolyA
    element.polynom_b = PolyB
    model.append(element)

    if simplified:
        model[0].polynom_a = model[0].polynom_a[:3]
        model[0].polynom_b = model[0].polynom_b[:3]

    return model
