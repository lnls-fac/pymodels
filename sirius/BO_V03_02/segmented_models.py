import numpy as _np
import mathphys as _mp
import pyaccel as _pyaccel

rbend_sirius = _pyaccel.elements.rbend
quadrupole   = _pyaccel.elements.quadrupole
sextupole    = _pyaccel.elements.sextupole
marker       = _pyaccel.elements.marker

_d2r = _np.pi /180

def dipole(energy):
    b, b_edge, b_pb  = 1, 2, 3
    # FIELDMAP
    # trajectory centered in good-field region. init_rx is set to +9.045 mm
    # *** interpolation of fields is now cubic ***
    # *** dipole angles were normalized to better close 360 degrees ***
    # *** more refined segmented model.
    # *** dipole angle is now in units of degrees
    #--- model polynom_b (rz > 0). units: [m] for length, [rad] for angle and [m],[T] for polynom_b ---

    # dipole model 2016-11-22 (3GeV)
    # ==============================
    # dipole model09
    # filename: 2016-11-11_BD_Model09_Sim_X=-80_35mm_Z=-1000_1000mm_I=981.778A.txt
    b_model_3GeV = _np.array([
     #--- model polynom_b (rz > 0). units: [m] for length, [rad] for angle and [m^(n-1)] for polynom_b ---
     #type   len[m]   angle[deg]  PolyB(n=0)   PolyB(n=1)   PolyB(n=2)   PolyB(n=3)   PolyB(n=4)   PolyB(n=5)   PolyB(n=6)
     [b,      0.196  ,  +1.15780 ,  +0.00e+00 ,  -2.27e-01 ,  -1.99e+00 ,  -6.44e+00 ,  -3.17e+02 ,  -2.06e+04 ,  -7.40e+05 ],
     [b,      0.192  ,  +1.14328 ,  +0.00e+00 ,  -2.12e-01 ,  -1.93e+00 ,  -3.56e+00 ,  -1.26e+02 ,  -7.10e+03 ,  -4.62e+05 ],
     [b,      0.182  ,  +1.09639 ,  +0.00e+00 ,  -1.86e-01 ,  -1.92e+00 ,  +9.55e-01 ,  -1.99e+02 ,  +3.99e+03 ,  -1.32e+05 ],
     [b,      0.010  ,  +0.05091 ,  +0.00e+00 ,  -2.49e-01 ,  -2.04e+00 ,  +2.78e+01 ,  -9.57e+02 ,  +2.32e+04 ,  -7.17e+05 ],
     [b,      0.010  ,  +0.03671 ,  +0.00e+00 ,  -1.70e-01 ,  -1.48e+00 ,  +3.31e+01 ,  -1.22e+03 ,  +2.41e+04 ,  -6.87e+05 ],
     [b_edge, 0,0,0,0,0,0,0,0,0],
     [b,      0.013  ,  +0.03275 ,  +0.00e+00 ,  -6.19e-02 ,  -1.83e+00 ,  +3.15e+01 ,  -1.04e+03 ,  +1.16e+04 ,  -2.15e+05 ],
     [b,      0.017  ,  +0.02908 ,  +0.00e+00 ,  -1.05e-02 ,  -1.97e+00 ,  +2.21e+01 ,  -5.66e+02 ,  +1.18e+03 ,  +2.15e+04 ],
     [b,      0.020  ,  +0.02233 ,  +0.00e+00 ,  +5.19e-03 ,  -1.60e+00 ,  +1.08e+01 ,  -1.92e+02 ,  -1.26e+03 ,  +3.92e+04 ],
     [b,      0.030  ,  +0.01835 ,  +0.00e+00 ,  +4.78e-03 ,  -9.31e-01 ,  +3.96e+00 ,  -4.29e+01 ,  -5.40e+02 ,  +1.10e+04 ],
     [b,      0.050  ,  +0.01240 ,  +1.13e-06 ,  +2.39e-03 ,  -3.61e-01 ,  +8.09e-01 ,  -3.65e-01 ,  -1.16e+02 ,  +2.07e+03 ],
     [b_pb,   0,0,0,0,0,0,0,0,0]
    ])

    # dipole model 2016-12-05 (150MeV)
    # ================================
    # dipole model09
    # filename: 2016-12-05_BD_Model09_Sim_X=-80_35mm_Z=-1000_1000mm_I=48.92A.txt
    b_model_150MeV = _np.array([
     #--- model polynom_b (rz > 0). units: [m] for length, [rad] for angle and [m^(n-1)] for polynom_b ---
     #type   len[m]   angle[deg]  PolyB(n=0)   PolyB(n=1)   PolyB(n=2)   PolyB(n=3)   PolyB(n=4)   PolyB(n=5)   PolyB(n=6)
     [b,      0.196  ,  +1.15700 ,  +0.00e+00 ,  -2.27e-01 ,  -1.98e+00 ,  -6.39e+00 ,  -3.13e+02 ,  -2.05e+04 ,  -7.33e+05 ],
     [b,      0.192  ,  +1.14267 ,  +0.00e+00 ,  -2.12e-01 ,  -1.93e+00 ,  -3.55e+00 ,  -1.24e+02 ,  -7.08e+03 ,  -4.58e+05 ],
     [b,      0.182  ,  +1.09642 ,  +0.00e+00 ,  -1.86e-01 ,  -1.90e+00 ,  +2.37e-01 ,  -1.77e+02 ,  +3.47e+03 ,  -1.05e+05 ],
     [b,      0.010  ,  +0.05151 ,  +0.00e+00 ,  -2.61e-01 ,  -1.72e+00 ,  +1.17e+01 ,  -6.81e+02 ,  +2.00e+04 ,  +3.53e+05 ],
     [b,      0.010  ,  +0.03715 ,  +0.00e+00 ,  -1.84e-01 ,  -1.12e+00 ,  +2.07e+01 ,  -9.21e+02 ,  +1.95e+04 ,  -3.16e+05 ],
     [b_edge, 0,0,0,0,0,0,0,0,0],
     [b,      0.013  ,  +0.03295 ,  +0.00e+00 ,  -6.79e-02 ,  -1.65e+00 ,  +2.70e+01 ,  -9.40e+02 ,  +1.15e+04 ,  -2.39e+05 ],
     [b,      0.017  ,  +0.02915 ,  +0.00e+00 ,  -1.24e-02 ,  -1.92e+00 ,  +2.15e+01 ,  -5.65e+02 ,  +1.60e+03 ,  +1.10e+04 ],
     [b,      0.020  ,  +0.02235 ,  +0.00e+00 ,  +4.70e-03 ,  -1.59e+00 ,  +1.08e+01 ,  -1.95e+02 ,  -1.21e+03 ,  +3.81e+04 ],
     [b,      0.030  ,  +0.01835 ,  +0.00e+00 ,  +4.67e-03 ,  -9.29e-01 ,  +3.97e+00 ,  -4.33e+01 ,  -5.37e+02 ,  +1.08e+04 ],
     [b,      0.050  ,  +0.01245 ,  +1.74e-05 ,  +2.38e-03 ,  -3.61e-01 ,  +8.08e-01 ,  -3.43e-01 ,  -1.16e+02 ,  +1.97e+03 ],
     [b_pb,   0,0,0,0,0,0,0,0,0]
    ])


    # interpolates multipoles linearly in energy
    b_model = b_model_3GeV
    b_model[:,3:] = b_model_150MeV[:,3:] + (energy - 150e6)/(3e9-150e6) * (b_model_3GeV[:,3:] - b_model_150MeV[:,3:])

    # turns deflection angle error off (convenient for having a nominal model with zero 4d closed orbit)
    b_model[:,3] = 0

    bd = []
    for i in range(b_model.shape[0]):
        if b_model[i,0] == b:
            bd.append(rbend_sirius('B', length=b_model[i,1], angle=_d2r*b_model[i,2], polynom_b=b_model[i,3:]))
        elif b_model[i,0] == b_edge:
            bd.append(marker('edgeB'))
        elif b_model[i,0] == b_pb:
            bd.append(marker('physB'))
        else:
            raise Exception("Bending type not recognized.")
    mb = marker('mB')
    bd = [bd[::-1] , mb, bd]
    b_length_segmented = 2*sum(b_model[:,1])

    return (bd, b_length_segmented)


def sx_sextupole(energy, fam_name, hardedge_SL):
    """ This script build an AT sextupole model based on analysis of a fieldmap generated for a 3D magnetic model
    of the magnet and based on rotating coil measurement data for the constructed magnet.

    Input:

    energy [eV]         : beam energy
    hardedge_SL [1/m^2] : nominal integrated sextupole strength

    Output:

    model            : AT segmented model
    model_length [m] : total model length

    Procedure:

    1. Renormalizes all multipoles of the fieldmap segmented model so that
       its main integrated multipole matches the nominal one.
    2. Takes the rotating coild integrated multipoles and divides them by
       the magnetic rigidity corresponding to the beam energy. This yields
       the normalized integrated multipolar strengths (PolynomB) for the model
    3. Merges the fieldmap and rotating coil data into one segmented structure.
       It does so by making sure that each corresponding fieldmap integrated multipole
       matches the rotating coil integrated multipole. It keeps the
       longitudinal multipole profile of the segmented model."""

    magnet_type = 2

    b = 1

    # FIELDMAP
    # *** interpolation of fields is now cubic ***
    # *** more refined segmented model.
    # *** dipole angle is now in units of degrees
    #--- model polynom_b (rz > 0). units: [m] for length, [rad] for angle and [m],[T] for polynom_b ---
    fmap_monomials = _np.array([0,2,8,14],dtype=int)
    main_mon_fmap_idx = _np.where(fmap_monomials == magnet_type)[0][0]

    # Sextupole model 2017-01-05 (3GeV)
    # =================================
    # sextupole model-03
    # filename: 2017-01-05_BO_Sextupole_Model03_Sim_X=-20_20mm_Z=-300_300mm_Imc=135A.txt
    sx_model_3GeV = _np.array([
    # type  len[m]    angle[deg]  PolyB(n=0)   PolyB(n=2)   PolyB(n=8)   PolyB(n=14)
    [b,      0.0525 ,  +0.00000 ,  -2.38e-06 ,  +1.90e+01 ,  -1.79e+10 ,  -3.25e+20]
    ])

    # Sextupole model 2017-01-05 (150Mev)
    # ===================================
    # sextupole model-03
    # filename: 2017-01-05_BO_Sextupole_Model03_Sim_X=-20_20mm_Z=-300_300mm_Imc=135A.txt
    sx_model_150MeV = _np.array([
    # type  len[m]    angle[deg]  PolyB(n=0)   PolyB(n=2)   PolyB(n=8)   PolyB(n=14)
    [b,      0.0525 ,  +0.00000 ,  -2.38e-06 ,  +1.90e+01 ,  -1.79e+10 ,  -3.25e+20]
    ])

    # interpolates multipoles linearly in energy
    sx_model = sx_model_3GeV;
    sx_model[:,3:] = sx_model_150MeV[:,3:] + (energy - 150e6)/(3e9-150e6) * (sx_model_3GeV[:,3:] - sx_model_150MeV[:,3:])


    # ROTATING COIL MEASUREMENT
    # =========================
    # data based on quadrupole prototype
    # Rescale multipolar profile according to rotating coild measurement
    rcoil_monomials  = _np.array([],dtype=int)
    rcoil_integrated_multipoles = _np.array([],dtype=float)
    # ---------------------------------------------------------------

    fmap_lens = sx_model[:,1]

    # rescale multipoles of the model according to nominal strength value passed as argument
    # --------------------------------------------------------------------------------------
    model_SL = 2*sum(sx_model[:,3+main_mon_fmap_idx] * fmap_lens)
    rescaling = hardedge_SL / model_SL
    sx_model[:,3:] = sx_model[:,3:] * rescaling


    # rescale multipoles of the rotating coild data according to nominal strength value passed as argument
    # ----------------------------------------------------------------------------------------------------
    if len(rcoil_monomials) != 0:
        brho, *_ = _mp.beam_optics.beam_rigidity(energy=energy)
        rcoil_normalized_integrated_multipoles = -rcoil_integrated_multipoles / brho
        rcoil_main_multipole_idx = _np.where(rcoil_monomials == magnet_type)[0][0]
        rescaling = hardedge_SL / rcoil_normalized_integrated_multipoles[rcoil_main_multipole_idx]
        rcoil_normalized_integrated_multipoles = rcoil_normalized_integrated_multipoles * rescaling


    # builds final model with fieldmap and rotating coild measurements
    # ----------------------------------------------------------------
    monomials = _np.unique(_np.hstack([fmap_monomials,rcoil_monomials]))
    sx_modelC = _np.zeros([sx_model.shape[0],len(monomials)+3])
    sx_modelC[:,:3] = sx_model[:,:3]
    for i in range(len(monomials)):
        rcoil_idx = _np.where(rcoil_monomials == monomials[i])[0]
        fmap_idx  = _np.where(fmap_monomials == monomials[i])[0]
        if len(rcoil_idx) == 0:
            # this multipole is not in rotating coil data: does nothing then.
            sx_modelC[:,i+3] = sx_model[:,fmap_idx[0]+3]
        else:
            if len(fmap_idx) == 0:
                # if this multipole is not in fmap model then uses main
                # multipole to build a multipolar profile
                fmap_integrated_multipole = 2*sum(sx_model[:,main_mon_fmap_idx+3] * fmap_lens)
            else:
                fmap_integrated_multipole = 2*sum(sx_model[:,fmap_idx[0]+3] * fmap_lens)
            rescaling = rcoil_normalized_integrated_multipoles[rcoil_idx[0]] / fmap_integrated_multipole
            sx_modelC[:,i+3] = sx_model[:,fmap_idx[0]+3] * rescaling;


    # converts deflection angle from degress to radians
    sx_modelC[:,2] *= _d2r

    # turns deflection angle error off (convenient for having a nominal model with zero 4d closed orbit)
    sel = _np.where(monomials == 0)[0]
    if len(sel):  sx_modelC[:,3+sel[0]] = 0

    sx = []
    for i in range(sx_modelC.shape[0]):
        if sx_modelC[i,0] == b:
            pol_b = _np.zeros(int(max(monomials))+1)
            pol_b[monomials] = sx_modelC[i,3:]
            s = sextupole(fam_name, 2*sx_modelC[i,1], 0) # factor 2 in length for one-segment model
            s.polynom_b=pol_b
            sx.append(s)
        else:
            raise Exception("Sextupole type not recognized.")

    model_length = 2*sum(sx_modelC[:,1])
    return (sx, model_length)


def qd_quadrupole(energy, fam_name, hardedge_KL):
    """ This script build an AT sextupole model based on analysis of a fieldmap generated for a 3D magnetic model
    of the magnet and based on rotating coil measurement data for the constructed magnet.

    Input:

    energy [eV]         : beam energy
    hardedge_SL [1/m^2] : nominal integrated sextupole strength

    Output:

    model            : AT segmented model
    model_length [m] : total model length

    Procedure:

    1. Renormalizes all multipoles of the fieldmap segmented model so that
       its main integrated multipole matches the nominal one.
    2. Takes the rotating coild integrated multipoles and divides them by
       the magnetic rigidity corresponding to the beam energy. This yields
       the normalized integrated multipolar strengths (PolynomB) for the model
    3. Merges the fieldmap and rotating coil data into one segmented structure.
       It does so by making sure that each corresponding fieldmap integrated multipole
       matches the rotating coil integrated multipole. It keeps the
       longitudinal multipole profile of the segmented model."""

    magnet_type = 1

    b = 1

    # FIELDMAP
    # *** interpolation of fields is now cubic ***
    # *** more refined segmented model.
    # *** dipole angle is now in units of degrees
    #--- model polynom_b (rz > 0). units: [m] for length, [rad] for angle and [m],[T] for polynom_b ---
    fmap_monomials = _np.array([1,5,9,13],dtype=int)
    main_mon_fmap_idx = _np.where(fmap_monomials == magnet_type)[0][0]

    # Sextupole model 2017-01-05 (3GeV)
    # =================================
    # sextupole model-03
    # filename: 2017-01-05_BO_Sextupole_Model03_Sim_X=-20_20mm_Z=-300_300mm_Imc=135A.txt
    qd_model_3GeV = _np.array([
    # type  len[m]   angle[deg]  PolyB(n=1)   PolyB(n=5)   PolyB(n=9)   PolyB(n=13)
    [b,     0.050  ,  +0.00000 ,  -5.00e-01 ,  +2.48e+04 ,  -6.87e+10 ,  -3.30e+14]
    ])

    # Sextupole model 2017-01-05 (150Mev)
    # ===================================
    # sextupole model-03
    # filename: 2017-01-05_BO_Sextupole_Model03_Sim_X=-20_20mm_Z=-300_300mm_Imc=135A.txt
    qd_model_150MeV = _np.array([
    # type  len[m]   angle[deg]  PolyB(n=1)   PolyB(n=5)   PolyB(n=9)   PolyB(n=13)
    [b,      0.050  ,  +0.00000 ,  -5.01e-01 ,  +2.49e+04 ,  -6.89e+10 ,  -3.25e+14]
    ])

    # interpolates multipoles linearly in energy
    qd_model = qd_model_3GeV;
    qd_model[:,3:] = qd_model_150MeV[:,3:] + (energy - 150e6)/(3e9-150e6) * (qd_model_3GeV[:,3:] - qd_model_150MeV[:,3:])


    # ROTATING COIL MEASUREMENT
    # =========================
    # data based on quadrupole prototype
    # Rescale multipolar profile according to rotating coild measurement
    rcoil_monomials  = _np.array([],dtype=int)
    rcoil_integrated_multipoles = _np.array([],dtype=float)
    # ---------------------------------------------------------------

    fmap_lens = qd_model[:,1]

    # rescale multipoles of the model according to nominal strength value passed as argument
    # --------------------------------------------------------------------------------------
    model_KL = 2*sum(qd_model[:,3+main_mon_fmap_idx] * fmap_lens)
    rescaling = hardedge_KL / model_KL
    qd_model[:,3:] = qd_model[:,3:] * rescaling


    # rescale multipoles of the rotating coild data according to nominal strength value passed as argument
    # ----------------------------------------------------------------------------------------------------
    if len(rcoil_monomials) != 0:
        brho, *_ = _mp.beam_optics.beam_rigidity(energy=energy)
        rcoil_normalized_integrated_multipoles = -rcoil_integrated_multipoles / brho
        rcoil_main_multipole_idx = _np.where(rcoil_monomials == magnet_type)[0][0]
        rescaling = hardedge_SL / rcoil_normalized_integrated_multipoles[rcoil_main_multipole_idx]
        rcoil_normalized_integrated_multipoles = rcoil_normalized_integrated_multipoles * rescaling


    # builds final model with fieldmap and rotating coild measurements
    # ----------------------------------------------------------------
    monomials = _np.unique(_np.hstack([fmap_monomials,rcoil_monomials]))
    qd_modelC = _np.zeros([qd_model.shape[0],len(monomials)+3])
    qd_modelC[:,:3] = qd_model[:,:3]
    for i in range(len(monomials)):
        rcoil_idx = _np.where(rcoil_monomials == monomials[i])[0]
        fmap_idx  = _np.where(fmap_monomials == monomials[i])[0]
        if len(rcoil_idx) == 0:
            # this multipole is not in rotating coil data: does nothing then.
            qd_modelC[:,i+3] = qd_model[:,fmap_idx[0]+3]
        else:
            if len(fmap_idx) == 0:
                # if this multipole is not in fmap model then uses main
                # multipole to build a multipolar profile
                fmap_integrated_multipole = 2*sum(qd_model[:,main_mon_fmap_idx+3] * fmap_lens)
            else:
                fmap_integrated_multipole = 2*sum(qd_model[:,fmap_idx[0]+3] * fmap_lens)
            rescaling = rcoil_normalized_integrated_multipoles[rcoil_idx[0]] / fmap_integrated_multipole
            qd_modelC[:,i+3] = qd_model[:,fmap_idx[0]+3] * rescaling;


    # converts deflection angle from degress to radians
    qd_modelC[:,2] *= _d2r

    # turns deflection angle error off (convenient for having a nominal model with zero 4d closed orbit)
    sel = _np.where(monomials == 0)[0]
    if len(sel):  qd_modelC[:,3+sel[0]] = 0

    qd = []
    for i in range(qd_modelC.shape[0]):
        if qd_modelC[i,0] == b:
            pol_b = _np.zeros(int(max(monomials))+1)
            pol_b[monomials] = qd_modelC[i,3:]
            q = quadrupole(fam_name, 2*qd_modelC[i,1], 0) # factor 2 in length for one-segment model
            q.polynom_b=pol_b
            qd.append(q)
        else:
            raise Exception("Quadrupole type not recognized.")

    model_length = 2*sum(qd_modelC[:,1])
    return (qd, model_length)


def qf_quadrupole(energy, fam_name, hardedge_KL):
    """ This script build an AT sextupole model based on analysis of a fieldmap generated for a 3D magnetic model
    of the magnet and based on rotating coil measurement data for the constructed magnet.

    Input:

    energy [eV]         : beam energy
    hardedge_SL [1/m^2] : nominal integrated sextupole strength

    Output:

    model            : AT segmented model
    model_length [m] : total model length

    Procedure:

    1. Renormalizes all multipoles of the fieldmap segmented model so that
       its main integrated multipole matches the nominal one.
    2. Takes the rotating coild integrated multipoles and divides them by
       the magnetic rigidity corresponding to the beam energy. This yields
       the normalized integrated multipolar strengths (PolynomB) for the model
    3. Merges the fieldmap and rotating coil data into one segmented structure.
       It does so by making sure that each corresponding fieldmap integrated multipole
       matches the rotating coil integrated multipole. It keeps the
       longitudinal multipole profile of the segmented model."""

    magnet_type = 1

    b = 1

    # FIELDMAP
    # *** interpolation of fields is now cubic ***
    # *** more refined segmented model.
    # *** dipole angle is now in units of degrees
    #--- model polynom_b (rz > 0). units: [m] for length, [rad] for angle and [m],[T] for polynom_b ---
    fmap_monomials = _np.array([1,5,9,13],dtype=int)
    main_mon_fmap_idx = _np.where(fmap_monomials == magnet_type)[0][0]

    # Sextupole model 2017-01-05 (3GeV)
    # =================================
    # sextupole model-03
    # filename: 2017-01-05_BO_Sextupole_Model03_Sim_X=-20_20mm_Z=-300_300mm_Imc=135A.txt
    qf_model_3GeV = _np.array([
    # type  len[m]   angle[deg]  PolyB(n=1)   PolyB(n=5)   PolyB(n=9)   PolyB(n=13)
    [b,     0.114  ,  +0.00000 ,  +1.78e+00 ,  -1.91e+04 ,  +2.37e+11 ,  +4.91e+16]
    ])

    # Sextupole model 2017-01-05 (150Mev)
    # ===================================
    # sextupole model-03
    # filename: 2017-01-05_BO_Sextupole_Model03_Sim_X=-20_20mm_Z=-300_300mm_Imc=135A.txt
    qf_model_150MeV = _np.array([
    # type  len[m]   angle[deg]  PolyB(n=1)   PolyB(n=5)   PolyB(n=9)   PolyB(n=13)
    [b,     0.114  ,  +0.00000 ,  +1.78e+00 ,  -1.91e+04 ,  +2.38e+11 ,  +4.91e+16]
    ])

    # interpolates multipoles linearly in energy
    qf_model = qf_model_3GeV;
    qf_model[:,3:] = qf_model_150MeV[:,3:] + (energy - 150e6)/(3e9-150e6) * (qf_model_3GeV[:,3:] - qf_model_150MeV[:,3:])


    # ROTATING COIL MEASUREMENT
    # =========================
    # data based on quadrupole prototype
    # Rescale multipolar profile according to rotating coild measurement
    rcoil_monomials  = _np.array([1,5,9,13],dtype=int)
    # based on relative [1.0, -1.0e-3, 1.1e-3, 0.08e-3]:
    rcoil_integrated_multipoles = _np.array([1,-1.066222407330279e+04,1.250513244082492e+11,9.696910847302045e+16])
    # ---------------------------------------------------------------

    fmap_lens = qf_model[:,1]

    # rescale multipoles of the model according to nominal strength value passed as argument
    # --------------------------------------------------------------------------------------
    model_KL = 2*sum(qf_model[:,3+main_mon_fmap_idx] * fmap_lens)
    rescaling = hardedge_KL / model_KL
    qf_model[:,3:] = qf_model[:,3:] * rescaling


    # rescale multipoles of the rotating coild data according to nominal strength value passed as argument
    # ----------------------------------------------------------------------------------------------------
    if len(rcoil_monomials) != 0:
        brho, *_ = _mp.beam_optics.beam_rigidity(energy=energy)
        rcoil_normalized_integrated_multipoles = -rcoil_integrated_multipoles / brho
        rcoil_main_multipole_idx = _np.where(rcoil_monomials == magnet_type)[0][0]
        rescaling = hardedge_KL / rcoil_normalized_integrated_multipoles[rcoil_main_multipole_idx]
        rcoil_normalized_integrated_multipoles = rcoil_normalized_integrated_multipoles * rescaling


    # builds final model with fieldmap and rotating coild measurements
    # ----------------------------------------------------------------
    monomials = _np.unique(_np.hstack([fmap_monomials,rcoil_monomials]))
    qf_modelC = _np.zeros([qf_model.shape[0],len(monomials)+3])
    qf_modelC[:,:3] = qf_model[:,:3]
    for i in range(len(monomials)):
        rcoil_idx = _np.where(rcoil_monomials == monomials[i])[0]
        fmap_idx  = _np.where(fmap_monomials == monomials[i])[0]
        if len(rcoil_idx) == 0:
            # this multipole is not in rotating coil data: does nothing then.
            qf_modelC[:,i+3] = qf_model[:,fmap_idx[0]+3]
        else:
            if len(fmap_idx) == 0:
                # if this multipole is not in fmap model then uses main
                # multipole to build a multipolar profile
                fmap_integrated_multipole = 2*sum(qf_model[:,main_mon_fmap_idx+3] * fmap_lens)
            else:
                fmap_integrated_multipole = 2*sum(qf_model[:,fmap_idx[0]+3] * fmap_lens)
            rescaling = rcoil_normalized_integrated_multipoles[rcoil_idx[0]] / fmap_integrated_multipole
            qf_modelC[:,i+3] = qf_model[:,fmap_idx[0]+3] * rescaling;


    # converts deflection angle from degress to radians
    qf_modelC[:,2] *= _d2r

    # turns deflection angle error off (convenient for having a nominal model with zero 4d closed orbit)
    sel = _np.where(monomials == 0)[0]
    if len(sel):  qf_modelC[:,3+sel[0]] = 0

    qf = []
    for i in range(qf_modelC.shape[0]):
        if qf_modelC[i,0] == b:
            pol_b = _np.zeros(int(max(monomials))+1)
            pol_b[monomials] = qf_modelC[i,3:]
            q = quadrupole(fam_name, qf_modelC[i,1], 0)
            q.polynom_b=pol_b
            qf.append(q)
        else:
            raise Exception("Quadrupole type not recognized.")

    model_length = 2*sum(qf_modelC[:,1])
    mqf  = marker('mQF')
    qf   = [qf, mqf, qf];
    return (qf, model_length)
