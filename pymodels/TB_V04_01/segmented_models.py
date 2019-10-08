"""Segmented models of the lattice."""

import math as _math
import numpy as _np
import pyaccel as _pyaccel


def dipole(sign, simplified=False):
    """Segmented BC dipole model."""
    segtypes = {
        'b': ('B', _pyaccel.elements.rbend),
        'b_edge': ('edgeB', _pyaccel.elements.marker),
        'b_pb': ('physB', _pyaccel.elements.marker),
    }

    #  FIELDMAP
    #  trajectory centered in good-field region. init_rx is set to +9.045 mm
    #  *** interpolation of fields is now cubic ***
    #  *** dipole angles were normalized to better close 360 degrees ***
    #  *** more refined segmented model.
    #  *** dipole angle is now in units of degrees
    # --- model polynom_b (rz > 0). units: [m] for length, [rad] for angle and [m],[T] for polynom_b ---
    monomials = [0, 1, 2, 3, 4, 5, 6]
    # dipole model (150MeV)
    # =====================
    # filename: 2018-08-04_TB_Dipole_Model03_Sim_X=-85_85mm_Z=-500_500mm_Imc=249.1A.txt
    segmodel = [
        # --- model polynom_b (rz > 0). units: [m] for length, [rad] for angle and [m^(n-1)] for polynom_b ---
        # type   len[m]  angle[deg]  PolyB(n=0) PolyB(n=1) PolyB(n=2) PolyB(n=3) PolyB(n=4) PolyB(n=5) PolyB(n=6)
        ['b',      0.0800, +3.96552, +0.00e+00, -6.11e-04, -7.42e-02, -2.19e+00, -2.43e+02, -3.43e+04, -2.11e+06],
        ['b',      0.0200, +0.98973, +0.00e+00, -2.15e-02, -2.68e-01, -2.01e+00, -1.63e+02, -8.81e+03, -1.15e+06],
        ['b',      0.0200, +0.93979, +0.00e+00, -6.44e-01, -4.76e+00, -1.42e+01, -7.80e+02, -5.33e+03, -1.42e+06],
        ['b',      0.0200, +0.64484, +0.00e+00, -1.63e+00, -6.59e+00, +2.42e+01, -5.22e+03, +1.82e+04, -2.67e+06],
        ['b_edge', 0, 0, 0, 0, 0, 0, 0, 0, 0],
        ['b',      0.0200, +0.38227, +0.00e+00, -7.75e-01, -1.34e+01, +9.09e+01, -5.95e+03, +3.50e+04, -7.03e+05],
        ['b',      0.0200, +0.24438, +0.00e+00, -3.74e-01, -1.41e+01, +9.51e+01, -2.80e+03, +6.72e+03, +2.36e+05],
        ['b',      0.0300, +0.20469, +0.00e+00, -2.13e-01, -9.21e+00, +5.84e+01, -8.54e+02, -6.30e+02, +1.14e+05],
        ['b',      0.0300, +0.12878, +1.04e-04, -1.38e-01, -6.08e+00, +3.36e+01, -2.08e+02, -8.68e+02, +4.60e+04],
        ['b_pb',   0, 0, 0, 0, 0, 0, 0, 0, 0],
    ]

    d2r = _math.pi/180.0
    for i in range(len(segmodel)):
        segmodel[i][2] = sign * segmodel[i][2]
        # turns deflection angle error off (convenient for having a nominal model with zero 4d closed orbit)
        segmodel[i][3] = 0.0

    # # --- manipule polynomialB ---
    # for i in range(len(segmodel)):
    #     # invert sign of bending angle, if the case.
    #     segmodel[i][2] = sign * segmodel[i][2]
    #     # invert sign of odd-order polynomb, if the case.
    #     for j in range(0, len(monomials)):
    #         segmodel[i][3+j] *= sign**monomials[j]
    #     # turns deflection angle error off
    #     segmodel[i][3] = 0.0

    # --- creates half model ---
    model = []
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
    mb = _pyaccel.elements.marker('mB')
    model = model[::-1] + [mb] + model

    if simplified:
        le = sum([s[1] for s in segmodel[:8]])
        ang1 = sum([s[2] for s in segmodel[:8]]) * d2r
        k = sum([s[4]*s[1] for s in segmodel[:8]])/le
        s = sum([s[5]*s[1] for s in segmodel[:8]])/le
        el = _pyaccel.elements.rbend(fam_name='B', length=2*le, angle=2*ang1,
                                     angle_in=0, angle_out=0,
                                     gap=0, fint_in=0, fint_out=0,
                                     polynom_a=[0, 0, 0], polynom_b=[0, k, s])
        le = sum([s[1] for s in segmodel[9:14]])
        ang2 = sum([s[2] for s in segmodel[9:]]) * d2r
        k = sum([s[4]*s[1] for s in segmodel[9:]])/le
        s = sum([s[5]*s[1] for s in segmodel[9:]])/le
        el_e = _pyaccel.elements.rbend(
            fam_name='B', length=le, angle=ang2,
            angle_in=0, angle_out=0*ang2,
            gap=0, fint_in=0, fint_out=0,
            polynom_a=[0, 0, 0], polynom_b=[0, k, s])
        el_b = _pyaccel.elements.rbend(
            fam_name='B', length=le, angle=ang2,
            angle_in=0*ang2, angle_out=0,
            gap=0, fint_in=0, fint_out=0,
            polynom_a=[0, 0, 0], polynom_b=[0, k, s])
        l2 = sum([s[1] for s in segmodel[14:]])
        dr = _pyaccel.elements.drift('LBC', l2)
        model = [dr, el_b, el, el_e, dr]

    return model


def septum(strengths, nseg=6, use_matrix=True):
    if nseg < 2:
        raise Exception('Number of segments must be >= 2.')
    rbend_sirius = _pyaccel.elements.rbend
    m66 = _pyaccel.elements.matrix
    marker = _pyaccel.elements.marker
    deg_2_rad = _math.pi / 180.0

    # -- bo injection septum --
    dip_nam = 'InjSept'
    matrix_name = 'InjSeptM66'
    dip_len = 0.50
    dip_ang = 21.75 * deg_2_rad
    dip_k = strengths['injsept_k']
    dip_ks = strengths['injsept_ks']
    dip_kl = dip_k * dip_len
    dip_ksl = dip_ks * dip_len

    if not use_matrix:
        polya = [0, -dip_ks, 0]
        polyb = [0, dip_k, 0]
    else:
        polya = [0, 0, 0]
        polyb = [0, 0, 0]

    seg_len = dip_len / nseg
    seg_ang = dip_ang / nseg

    seg_kxl = dip_kl / (nseg - 1)
    seg_kyl = - seg_kxl
    seg_ksxl = dip_ksl / (nseg - 1)
    seg_ksyl = seg_ksxl

    septine = rbend_sirius(
        fam_name=dip_nam, length=seg_len, angle=seg_ang,
        angle_in=dip_ang/2, angle_out=0,
        gap=0, fint_in=0, fint_out=0,
        polynom_a=polya, polynom_b=polyb)
    septins = rbend_sirius(
        fam_name=dip_nam, length=seg_len, angle=seg_ang,
        angle_in=0, angle_out=dip_ang/2,
        gap=0, fint_in=0, fint_out=0,
        polynom_a=polya, polynom_b=polyb)

    matrix = m66(matrix_name, 0)
    matrix.KxL = seg_kxl
    matrix.KyL = seg_kyl
    matrix.KsxL = seg_ksxl
    matrix.KsyL = seg_ksyl

    if use_matrix:
        segs = [matrix, ]
    else:
        segs = []
    element = rbend_sirius(
        fam_name=dip_nam, length=seg_len, angle=seg_ang,
        angle_in=0, angle_out=0,
        gap=0, fint_in=0, fint_out=0,
        polynom_a=polya, polynom_b=polyb)

    if nseg > 2:
        for _ in range(nseg-2):
            segs.append(_pyaccel.elements.Element(element))
            if use_matrix:
                segs.append(_pyaccel.elements.Element(matrix))

    # excluded ch to make it consistent with other codes.
    # the corrector can be implemented in the polynomB:
    bseptin = marker('bInjS')
    eseptin = marker('eInjS')
    model = [bseptin, septine] + segs + [septins, eseptin]
    return model
