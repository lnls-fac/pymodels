"""Segmented models of the lattice."""

import math as _math
import numpy as _np
import pyaccel as _pyaccel


def dipole(sign, simplified=False):
    """Segmented TS dipole model."""
    segtypes = {
        'b': ('B', _pyaccel.elements.rbend),
        'b_edge': ('edgeB', _pyaccel.elements.marker),
        'b_pb': ('physB', _pyaccel.elements.marker),
    }

    # dipole model 2017-08-31
    # =======================
    # filename: 2017-08-31_TS_Dipole_Model01_Sim_X=-85_85mm_Z=-1000_1000mm_Imc=680.1A.txt
    monomials = [0, 1, 2, 3, 4, 5, 6]
    segmodel = [
        # --- model polynom_b (rz > 0). units: [m] for length, [rad] for angle and [m^(n-1)] for polynom_b ---
        # type   len[m]   angle[deg]  PolyB(n=0)   PolyB(n=1)   PolyB(n=2)   PolyB(n=3)   PolyB(n=4)   PolyB(n=5)   PolyB(n=6)
        ['b',      0.1960, +0.80828, +0.00e+00, -1.51e-01, -1.35e+00, -2.92e+00, -1.08e+02, -7.71e+03, -3.84e+05],
        ['b',      0.1920, +0.79616, +0.00e+00, -1.44e-01, -1.33e+00, -2.08e+00, -6.62e+01, -2.56e+03, -2.65e+05],
        ['b',      0.1820, +0.76057, +0.00e+00, -1.32e-01, -1.32e+00, -3.07e-01, -1.16e+02, +1.88e+03, -5.06e+04],
        ['b',      0.0100, +0.03538, +0.00e+00, -1.58e-01, -1.14e+00, +7.26e+00, -3.87e+02, +2.90e+03, -7.20e+04],
        ['b',      0.0100, +0.02550, +0.00e+00, -9.99e-02, -8.58e-01, +1.05e+01, -5.61e+02, +7.09e+03, -2.19e+05],
        ['b_edge', 0,0,0,0,0,0,0,0,0],
        ['b',      0.0130, +0.02274, +0.00e+00, -3.60e-02, -1.10e+00, +1.26e+01, -5.85e+02, +5.36e+03, -1.09e+05],
        ['b',      0.0170, +0.02020, +0.00e+00, -7.26e-03, -1.24e+00, +1.01e+01, -3.70e+02, +8.45e+02, +4.57e+03],
        ['b',      0.0200, +0.01552, +0.00e+00, +1.59e-03, -1.04e+00, +5.18e+00, -1.41e+02, -4.95e+02, +2.08e+04],
        ['b',      0.0300, +0.01276, +0.00e+00, +1.91e-03, -6.16e-01, +1.94e+00, -3.42e+01, -2.37e+02, +6.99e+03],
        ['b',      0.0500, +0.00866, +3.43e-05, +1.04e-03, -2.43e-01, +3.98e-01, -1.23e+00, -5.04e+01, +1.05e+03],
        ['b_pb',   0,0,0,0,0,0,0,0,0],
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
