"""Segmented models of the lattice."""

import math as _math
import numpy as _np
import pyaccel as _pyaccel


def dipole(sign, simplified=False):
    """Segmented BC dipole model."""
    segtypes = {
        'B': ('B', _pyaccel.elements.rbend),
        'B_EDGE': ('B_EDGE', _pyaccel.elements.marker),
    }

    # dipole model 2017-08-25 (150MeV)
    # ================================
    # filename:
    #  2017-08-25_TB_Dipole_Model02_Sim_X=-85_85mm_Z=-500_500mm.txt
    monomials = [0, 1, 2, 3, 4, 5, 6]
    segmodel = [
         # --- model polynom_b (rz > 0). units: [m] for length, [rad] for
         #     angle and [m^(n-1)] for polynom_b ---
         # type   len[m]   angle[deg]  PolyB(n=0)   PolyB(n=1)   PolyB(n=2)
         #                PolyB(n=3)   PolyB(n=4)   PolyB(n=5)   PolyB(n=6)
         ['B', 0.0800, +3.97053, +0.00e+00, -1.38e-04, +8.83e-03, -1.75e-01,
          +5.64e+01, +5.21e+03, -8.50e+05],
         ['B', 0.0200, +0.99101, +0.00e+00, -2.06e-02, -1.98e-01, -2.13e+00,
          -6.78e+00, +2.46e+04, -1.64e+06],
         ['B', 0.0200, +0.94099, +0.00e+00, -6.34e-01, -4.53e+00, -5.76e+00,
          -1.49e+03, +2.90e+04, -1.26e+06],
         ['B', 0.0200, +0.64345, +0.00e+00, -1.56e+00, -7.53e+00, +1.22e+02,
          -6.92e+03, +9.34e+04, -2.64e+06],
         ['B_EDGE', 0, 0, 0, 0, 0, 0, 0, 0, 0],
         ['B', 0.0200, +0.37798, +0.00e+00, -6.24e-01, -1.60e+01, +2.07e+02,
          -6.87e+03, +5.18e+04, -6.33e+05],
         ['B', 0.0200, +0.23850, +0.00e+00, -2.17e-01, -1.62e+01, +1.43e+02,
          -2.70e+03, -3.65e+03, +3.69e+05],
         ['B', 0.0300, +0.19919, +0.00e+00, -9.09e-02, -1.04e+01, +6.57e+01,
          -6.03e+02, -5.99e+03, +1.53e+05],
         ['B', 0.0300, +0.13835, -3.06e-04, -5.07e-02, -7.02e+00, +3.11e+01,
          -4.04e+01, -2.97e+03, +4.56e+04],
    ]

    # --- manipule polynomialB ---
    for i in range(len(segmodel)):
        # invert sign of bending angle, if the case.
        segmodel[i][2] = sign * segmodel[i][2]
        # invert sign of odd-order polynomb, if the case.
        for j in range(0, len(monomials)):
            segmodel[i][3+j] *= sign**monomials[j]
        # turns deflection angle error off
        segmodel[i][3] = 0.0

    # --- creates half model ---
    model = []
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
